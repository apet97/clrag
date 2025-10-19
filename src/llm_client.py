from __future__ import annotations
import os, time, json, typing as T
from urllib.parse import urljoin
import httpx
from loguru import logger

DEFAULT_TIMEOUT = float(os.getenv("LLM_TIMEOUT_SECONDS", "30"))
RETRIES = int(os.getenv("LLM_RETRIES", "3"))
BACKOFF = float(os.getenv("LLM_BACKOFF", "0.75"))

class LLMClient:
    def __init__(self) -> None:
        self.api_type = os.getenv("LLM_API_TYPE", "ollama").strip().lower()
        self.base_url = os.getenv("LLM_BASE_URL", "http://10.127.0.192:11434").strip()
        self.chat_path = os.getenv("LLM_CHAT_PATH", "/api/chat").strip()
        self.tags_path = os.getenv("LLM_TAGS_PATH", "/api/tags").strip()
        self.model = os.getenv("LLM_MODEL", "gpt-oss20b").strip()
        self.verify_ssl = os.getenv("LLM_VERIFY_SSL", "false").lower() == "true"
        self.mock = os.getenv("MOCK_LLM", "false").lower() == "true"

        # Build resolved URLs
        self.chat_url = self._build_url(self.chat_path)
        self.tags_url = self._build_url(self.tags_path)

        if not self.base_url and not self.mock:
            raise RuntimeError("LLM_BASE_URL is required when MOCK_LLM=false")

    def _build_url(self, path: str) -> str:
        """Build full URL from base and path using urljoin."""
        base = self.base_url.rstrip("/")
        path_part = path.lstrip("/")
        return urljoin(base + "/", path_part)

    def health_check(self) -> dict[str, T.Any]:
        """Check LLM endpoint health. Returns {'ok': bool, 'details': str}."""
        if self.mock:
            return {"ok": True, "details": "mock mode"}

        try:
            client = httpx.Client(timeout=DEFAULT_TIMEOUT, verify=self.verify_ssl)

            # Try to fetch tags/models list
            resp = client.get(self.tags_url)
            if resp.status_code == 404:
                return {
                    "ok": False,
                    "details": f"404 on {self.tags_url} - endpoint not exposed (UI-only URL?)",
                }
            if resp.status_code == 403:
                return {
                    "ok": False,
                    "details": f"403 on {self.tags_url} - forbidden (check auth, VPN, firewall)",
                }
            if resp.status_code != 200:
                return {
                    "ok": False,
                    "details": f"HTTP {resp.status_code} on {self.tags_url}",
                }

            # Verify JSON and contains models/tags
            data = resp.json()
            if isinstance(data, dict):
                if "models" in data or "tags" in data:
                    return {"ok": True, "details": f"OK: {self.api_type} at {self.base_url}"}
            elif isinstance(data, list) and len(data) > 0:
                return {"ok": True, "details": f"OK: {self.api_type} at {self.base_url}"}

            return {"ok": False, "details": f"Unexpected response from {self.tags_url}"}

        except Exception as e:
            return {"ok": False, "details": f"Error contacting {self.tags_url}: {str(e)}"}

    def chat(self, messages: list[dict], max_tokens: int = 800, temperature: float = 0.2, stream: bool = False) -> str:
        if self.mock:
            # Fabricate concise, grounded response for offline dev
            ctx = "\n".join(m["content"] for m in messages if m["role"] == "user")[:1200]
            return f"{ctx.splitlines()[-1]}\n\n[1]\n\nSources:\n[1] See provided context."

        if self.api_type == "ollama":
            payload = {"model": self.model, "messages": messages, "stream": False}
            return self._post_json(self.chat_url, payload)
        elif self.api_type == "openai":
            payload = {"model": self.model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens, "stream": False}
            headers = {}
            key = os.getenv("OPENAI_API_KEY", "").strip()
            if key:
                headers["Authorization"] = f"Bearer {key}"
            return self._post_json(self.chat_url, payload, headers=headers)
        else:
            raise RuntimeError(f"Unsupported LLM_API_TYPE: {self.api_type}")

    def _post_json(self, url: str, payload: dict, headers: dict | None = None) -> str:
        headers = {"Content-Type": "application/json", **(headers or {})}
        attempt = 0
        last_err = None
        while attempt < RETRIES:
            try:
                client = httpx.Client(timeout=DEFAULT_TIMEOUT, verify=self.verify_ssl)
                resp = client.post(url, headers=headers, json=payload)
                resp.raise_for_status()
                data = resp.json()
                # Ollama: {'message': {'role':'assistant','content':'...'}} or stream chunks
                if "message" in data and isinstance(data["message"], dict):
                    return data["message"].get("content", "").strip()
                # OpenAI: {'choices':[{'message':{'content':'...'}}]}
                if "choices" in data and data["choices"]:
                    return data["choices"][0]["message"]["content"].strip()
                # Fallback to raw text
                return json.dumps(data)[:4096]
            except Exception as e:
                last_err = e
                attempt += 1
                sleep = BACKOFF * attempt
                logger.warning(f"LLM POST error (attempt {attempt}/{RETRIES}): {e}; backing off {sleep:.2f}s")
                time.sleep(sleep)
        raise RuntimeError(f"LLM request failed after {RETRIES} attempts: {last_err}")
