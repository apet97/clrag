from __future__ import annotations
import os, time, json, typing as T, random, re
from urllib.parse import urljoin, urlparse, parse_qs, urlencode
import httpx
from loguru import logger

def _env_bool(val: str | None) -> bool | None:
    """Parse environment boolean, return None if ambiguous."""
    if val is None:
        return None
    v = val.strip().lower()
    if v in ("1", "true", "yes", "y"):
        return True
    if v in ("0", "false", "no", "n"):
        return False
    return None

# Back-compat: LLM_TIMEOUT deprecated in favor of LLM_TIMEOUT_SECONDS
_timeout_seconds = os.getenv("LLM_TIMEOUT_SECONDS")
_timeout_alias = os.getenv("LLM_TIMEOUT")
if _timeout_alias and not _timeout_seconds:
    logger.warning("LLM_TIMEOUT is deprecated. Use LLM_TIMEOUT_SECONDS instead.")
    DEFAULT_TIMEOUT = float(_timeout_alias)
else:
    DEFAULT_TIMEOUT = float(_timeout_seconds or "30")

RETRIES = int(os.getenv("LLM_RETRIES", "3"))
BACKOFF = float(os.getenv("LLM_BACKOFF", "0.75"))
STREAMING_ENABLED = os.getenv("STREAMING_ENABLED", "false").lower() == "true"

def _validate_config() -> None:
    """Validate LLM configuration on startup. Raises ValueError if invalid."""
    # Note: LLM_BASE_URL should be set in .env; use <INTERNAL_OLLAMA_HOST> for internal instance
    base_url = os.getenv("LLM_BASE_URL", "").strip()
    chat_path = os.getenv("LLM_CHAT_PATH", "").strip()
    tags_path = os.getenv("LLM_TAGS_PATH", "").strip()
    api_type = os.getenv("LLM_API_TYPE", "").strip().lower()
    mock_llm = os.getenv("MOCK_LLM", "false").lower() == "true"

    # Validate API type
    if api_type not in ("ollama", "openai"):
        raise ValueError(f"LLM_API_TYPE must be 'ollama' or 'openai', got: {api_type}")

    # If not in mock mode, validate base URL is set and is http(s)
    if not mock_llm:
        if not base_url:
            raise ValueError("LLM_BASE_URL is required when MOCK_LLM=false")
        if not base_url.startswith(("http://", "https://")):
            raise ValueError(f"LLM_BASE_URL must be http:// or https://, got: {base_url}")

    # Validate paths start with /
    for name, path in [("LLM_CHAT_PATH", chat_path), ("LLM_TAGS_PATH", tags_path)]:
        if path and not path.startswith("/"):
            raise ValueError(f"{name} must start with '/', got: {path}")

    # Validate timeouts are positive
    if DEFAULT_TIMEOUT <= 0:
        raise ValueError(f"LLM_TIMEOUT_SECONDS must be positive, got: {DEFAULT_TIMEOUT}")
    if RETRIES < 0:
        raise ValueError(f"LLM_RETRIES must be non-negative, got: {RETRIES}")
    if BACKOFF <= 0:
        raise ValueError(f"LLM_BACKOFF must be positive, got: {BACKOFF}")

    logger.info("LLM config validation passed")

def _sanitize_url(url: str) -> str:
    """Remove or mask sensitive query parameters from URL for logging."""
    try:
        parsed = urlparse(url)
        if not parsed.query:
            return url
        # Parse query params
        params = parse_qs(parsed.query, keep_blank_values=True)
        # Mask sensitive params
        for sensitive_key in ("token", "key", "api_key", "password", "secret"):
            if sensitive_key in params:
                params[sensitive_key] = ["***"]
        # Reconstruct query string
        sanitized_qs = "&".join(f"{k}={v[0]}" for k, v in params.items())
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{sanitized_qs}" if sanitized_qs else f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    except Exception:
        return url

def _redact_token(text: str) -> str:
    """Redact Bearer token values from log text."""
    return re.sub(r'Bearer\s+[^\s]+', 'Bearer ***', text, flags=re.IGNORECASE)

def _cap_response(text: str, max_len: int = 200) -> str:
    """Cap response body length for logging."""
    if len(text) > max_len:
        return text[:max_len] + f"... ({len(text)-max_len} more bytes)"
    return text

# Module-level HTTP client (reused across instances)
HTTP_CLIENT: httpx.Client | None = None

def _get_http_client() -> httpx.Client:
    """Get or create module-level HTTP client with production-grade config."""
    global HTTP_CLIENT
    if HTTP_CLIENT is None:
        base_url = os.getenv("LLM_BASE_URL", "http://10.127.0.192:11434").strip()
        verify_env = _env_bool(os.getenv("LLM_VERIFY_SSL"))
        # Auto-detect SSL verification: default to True for https://, False for http://
        if verify_env is not None:
            verify = verify_env
        else:
            verify = base_url.startswith("https://")

        # Production-grade timeout and connection pooling
        timeout = httpx.Timeout(connect=5.0, read=DEFAULT_TIMEOUT, write=10.0, pool=5.0)
        limits = httpx.Limits(max_keepalive_connections=10, max_connections=20)

        HTTP_CLIENT = httpx.Client(
            timeout=timeout,
            verify=verify,
            limits=limits,
            follow_redirects=True
        )
    return HTTP_CLIENT

def close_http_client() -> None:
    """Called by FastAPI on shutdown."""
    global HTTP_CLIENT
    try:
        if HTTP_CLIENT is not None:
            HTTP_CLIENT.close()
    finally:
        HTTP_CLIENT = None

class LLMClient:
    def __init__(self) -> None:
        # Validate configuration early (on first instantiation)
        _validate_config()

        self.api_type = os.getenv("LLM_API_TYPE", "ollama").strip().lower()
        # Default to localhost for dev; use LLM_BASE_URL env for production/internal hosts
        self.base_url = os.getenv("LLM_BASE_URL", "http://localhost:11434").strip()
        self.chat_path = os.getenv("LLM_CHAT_PATH", "/api/chat").strip()
        self.tags_path = os.getenv("LLM_TAGS_PATH", "/api/tags").strip()
        self.model = os.getenv("LLM_MODEL", "gpt-oss:20b").strip()
        self.mock = os.getenv("MOCK_LLM", "false").lower() == "true"

        # Build resolved URLs
        self.chat_url = self._build_url(self.chat_path)
        self.tags_url = self._build_url(self.tags_path)

    def _build_url(self, path: str) -> str:
        """Build full URL from base and path using urljoin."""
        base = self.base_url.rstrip("/")
        path_part = path.lstrip("/")
        return urljoin(base + "/", path_part)

    def _post_json(self, url: str, payload: dict, headers: dict | None = None) -> str:
        """POST with retries, exponential backoff with jitter, and auth. Returns response text or raises."""
        headers = {"Content-Type": "application/json", **(headers or {})}

        # Add Bearer token if configured
        bearer_token = os.getenv("LLM_BEARER_TOKEN", "").strip()
        if bearer_token:
            headers["Authorization"] = f"Bearer {bearer_token}"

        delay = BACKOFF
        last_error: Exception | None = None
        sanitized_url = _sanitize_url(url)

        for attempt in range(1, RETRIES + 1):
            try:
                resp = _get_http_client().post(url, json=payload, headers=headers)
                # Treat 5xx as retryable; skip retry logic for 4xx
                if 500 <= resp.status_code < 600:
                    raise httpx.HTTPStatusError(
                        f"server {resp.status_code}",
                        request=resp.request,
                        response=resp,
                    )
                resp.raise_for_status()
                return resp.text
            except (httpx.TimeoutException, httpx.ConnectError) as e:
                # Retry on network timeouts and connection errors
                last_error = e
                if attempt == RETRIES:
                    break
                # Jittered exponential backoff
                jitter = random.uniform(0.0, 0.1 * delay)
                sleep_time = delay + jitter
                logger.debug(f"LLM POST attempt {attempt}/{RETRIES} failed to {sanitized_url}: {type(e).__name__}; backing off {sleep_time:.2f}s")
                time.sleep(sleep_time)
                delay *= 2
            except Exception as e:
                last_error = e
                if attempt == RETRIES:
                    break
                # Jittered exponential backoff for other errors
                jitter = random.uniform(0.0, 0.1 * delay)
                sleep_time = delay + jitter
                logger.debug(f"LLM POST attempt {attempt}/{RETRIES} failed to {sanitized_url}: {type(e).__name__}; backing off {sleep_time:.2f}s")
                time.sleep(sleep_time)
                delay *= 2

        raise RuntimeError(f"LLM POST failed after {RETRIES} attempts: {last_error}")

    def health_check(self) -> dict[str, T.Any]:
        """Check LLM endpoint health. Returns {'ok': bool, 'details': str}."""
        if self.mock:
            return {"ok": True, "details": "mock mode"}

        try:
            # Use module-level HTTP client
            resp = _get_http_client().get(self.tags_url)
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
            # Check if streaming is requested and enabled
            if stream and STREAMING_ENABLED:
                payload = {"model": self.model, "messages": messages, "stream": True}
                chunks = []
                try:
                    with _get_http_client().stream("POST", self.chat_url, json=payload) as resp:
                        for line in resp.iter_lines():
                            if not line:
                                continue
                            try:
                                obj = json.loads(line)
                                msg = obj.get("message", {})
                                if isinstance(msg, dict):
                                    part = msg.get("content", "")
                                    if isinstance(part, str):
                                        chunks.append(part)
                                if obj.get("done"):
                                    break
                            except json.JSONDecodeError:
                                continue
                    return "".join(chunks)
                except Exception as e:
                    logger.warning(f"Streaming failed, falling back to non-streaming: {e}")

            # Non-streaming (default)
            payload = {"model": self.model, "messages": messages, "stream": False}
            text = self._post_json(self.chat_url, payload)
            # Parse Ollama response: {"message": {"role":"assistant","content":"..."}}
            try:
                data = json.loads(text)
                if "message" in data and isinstance(data["message"], dict):
                    return data["message"].get("content", "").strip()
            except json.JSONDecodeError:
                pass
            return text

        elif self.api_type == "openai":
            payload = {"model": self.model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens, "stream": False}
            headers = {}
            key = os.getenv("OPENAI_API_KEY", "").strip()
            if key:
                headers["Authorization"] = f"Bearer {key}"
            text = self._post_json(self.chat_url, payload, headers=headers)
            # Parse OpenAI response: {"choices":[{"message":{"content":"..."}}]}
            try:
                data = json.loads(text)
                if "choices" in data and data["choices"]:
                    return data["choices"][0]["message"]["content"].strip()
            except json.JSONDecodeError:
                pass
            return text
        else:
            raise RuntimeError(f"Unsupported LLM_API_TYPE: {self.api_type}")

