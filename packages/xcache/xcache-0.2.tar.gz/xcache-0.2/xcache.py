# -*- coding: utf-8 -*-
from contextlib import contextmanager
from functools import lru_cache as _lru_cache, wraps
from threading import local

__version__ = '0.2'
__version_info__ = (0, 2)
__all__ = ['cached', 'cache_gen', 'clean_caches']


_thread_local = local()
_thread_local._ref = type('DefaultRef', (object,), {})()


def cache_gen(ref_gen, cache_impl=_lru_cache):
    def ref_cache(*cache_args, **cache_kwargs):
        def decorating_function(user_function):
            @wraps(user_function)
            def decorated_function(*args, **kwargs):
                return _get_function()(*args, **kwargs)

            def cache_info():
                """Report cache statistics"""
                return _get_function().cache_info()

            def cache_clear():
                """Clear the cache and cache statistics"""
                return _get_function().cache_clear()

            def _get_function():
                ref = ref_gen()
                if not ref:
                    return user_function
                if not hasattr(ref, '_lru_caches'):
                    ref._lru_caches = {}
                if user_function not in ref._lru_caches:
                    ref._lru_caches[user_function] = cache_impl(*cache_args, **cache_kwargs)(user_function)
                return ref._lru_caches[user_function]

            decorated_function.cache_info = cache_info
            decorated_function.cache_clear = cache_clear

            return decorated_function
        return decorating_function
    return ref_cache


cached = cache_gen(lambda: _thread_local._ref)


@contextmanager
def clean_caches(ref=None):
    old_ref = _thread_local._ref
    if ref:
        _thread_local._ref = ref
    _thread_local._ref._lru_caches = {}
    try:
        yield ref
    finally:
        _thread_local._ref._lru_caches = {}
        _thread_local._ref = old_ref
