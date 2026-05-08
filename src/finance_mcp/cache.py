import time
from typing import Any, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")


class TTLCache:
    def __init__(self, ttl: float):
        self.ttl = ttl
        self._cache: dict[str, tuple[float, Any]] = {}

    def get(self, key: str) -> Any | None:
        if key in self._cache:
            timestamp, value = self._cache[key]
            if time.time() - timestamp <= self.ttl:
                return value
            else:
                del self._cache[key]
        return None

    def set(self, key: str, value: Any) -> None:
        self._cache[key] = (time.time(), value)


# Shared instances
quote_cache = TTLCache(ttl=60.0)
fundamentals_cache = TTLCache(ttl=3600.0)
