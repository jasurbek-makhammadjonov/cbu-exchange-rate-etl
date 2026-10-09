"""Extract: download official exchange rates from the Central Bank of Uzbekistan (CBU)."""
import logging
import requests

BASE_URL = "https://cbu.uz/ru/arkhiv-kursov-valyut/json"
log = logging.getLogger(__name__)


def fetch_rates(date: str | None = None, timeout: int = 30) -> list[dict]:
    """Return raw CBU rates as a list of dicts. `date` format: YYYY-MM-DD (None = latest)."""
    url = f"{BASE_URL}/all/{date}/" if date else f"{BASE_URL}/"
    log.info("Fetching %s", url)
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.json()
