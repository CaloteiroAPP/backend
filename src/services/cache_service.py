import logging
from typing import Any, Callable
from cachetools import TTLCache

_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(name)s - %(message)s')


class CacheService:
    def __init__(self) -> None:
        self.cache = TTLCache(maxsize=1024, ttl=300)

    def get(self, key: str) -> Any | None:
        return self.cache.get(key)

    def set(self, key: str, value: Any) -> None:
        self.cache[key] = value

    # def delete(self, key: str) -> None:
    #     del self.cache[key]

    def get_or_set(self, key: str, fetch_function: Callable[[], Any]) -> Any:
        cached_value = self.get(key)

        if cached_value is None:
            _logger.info(f"Caching value for key: {key}")
            cached_value = fetch_function()
            self.set(key, cached_value)

        return cached_value
