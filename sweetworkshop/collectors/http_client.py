# collectors/http_client.py
import time
import logging
import requests
from dataclasses import dataclass
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

log = logging.getLogger("collector")

@dataclass
class HttpConfig:
    timeout: int = 25
    min_interval_sec: float = 0.35  # простий rate-limit між запитами

class HttpClient:
    def __init__(self, cfg: HttpConfig | None = None):
        self.cfg = cfg or HttpConfig()
        self._last_ts = 0.0
        self.session = requests.Session()

    def _throttle(self):
        dt = time.time() - self._last_ts
        if dt < self.cfg.min_interval_sec:
            time.sleep(self.cfg.min_interval_sec - dt)
        self._last_ts = time.time()

    @retry(
        reraise=True,
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=1, min=1, max=12),
        retry=retry_if_exception_type(requests.RequestException),
    )
    def get_json(self, url: str, params: dict | None = None, headers: dict | None = None) -> dict:
        self._throttle()
        log.info("GET %s", url)
        r = self.session.get(url, params=params, headers=headers, timeout=self.cfg.timeout)
        r.raise_for_status()
        return r.json()

    @retry(
        reraise=True,
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=1, min=1, max=12),
        retry=retry_if_exception_type(requests.RequestException),
    )
    def download_file(self, url: str) -> bytes:
        self._throttle()
        log.info("DOWNLOAD %s", url)
        r = self.session.get(url, timeout=self.cfg.timeout)
        r.raise_for_status()
        return r.content
