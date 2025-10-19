from __future__ import annotations
import os, time, json, typing as T
import httpx
from loguru import logger

DEFAULT_TIMEOUT = float(os.getenv("LLM_TIMEOUT", "60"))
RETRIES = int(os.getenv("LLM_RETRIES", "3"))
BACKOFF = float(os.getenv("LLM_BACKOFF", "0.75"))

class LLMClient:
    def __init__(self) -> None:
        self.api_type = os.getenv("LLM_API_TYPE", "ollama").strip().lower()
        self.endpoint = os.getenv("LLM_ENDPOINT", "").strip()
        self.model = os.getenv("LLM_MODEL", "gpt-oss20b").strip()
        self.verify_ssl = os.getenv("LLM_VERIFY_SSL", "false").lower() == "true"
        self.mock = os.getenv("MOCK_LLM", "false").lower() == "true"
        if not self.endpoint and not self.mock:
            raise RuntimeError("LLM_ENDPOINT is required when MOCK_LLM=false")

    def chat(self, messages: list[dict], max_tokens: int = 800, temperature: float = 0.2, stream: bool = False) -> str:
        if self.mock:
            # Fabricate concise, grounded response for offline dev
            ctx = "\n".join(m["content"] for m in messages if m["role"] == "user")[:1200]
            return f"{ctx.splitlines()[-1]}\n\n[1]\n\nSources:\n[1] See provided context."

        if self.api_type == "ollama":
            payload = {"model": self.model, "messages": messages, "stream": False}
            return self._post_json(self.endpoint, payload)
        elif self.api_type == "openai":
            url = self.endpoint.rstrip("/") + "/v1/chat/completions"
            payload = {"model": self.model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens, "stream": False}
            headers = {}
            key = os.getenv("OPENAI_API_KEY", "").strip()
            if key:
                headers["Authorization"] = f"Bearer {key}"
            return self._post_json(url, payload, headers=headers)
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
