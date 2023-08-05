try:
    from django.core.cache import caches
except ImportError:
    from django.core.cache import get_cache
from impediments import get_impediments as _get_impediments

from .conf import settings


def get_impediments():
    backend = settings.IMPEDIMENTS_CACHE_BACKEND_NAME
    cache_key = settings.IMPEDIMENTS_CACHE_KEY
    timeout = settings.IMPEDIMENTS_CACHE_TIMEOUT

    try:
        cache = caches[backend]
    except NameError:
        cache = get_cache(backend)
    impediments = cache.get(cache_key)

    if impediments is None:
        impediments = _get_impediments()
        cache.set(cache_key, impediments, timeout=timeout)

    return impediments
