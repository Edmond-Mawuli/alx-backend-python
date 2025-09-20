#!/usr/bin/env python3
"""Utility functions: access_nested_map, get_json, memoize"""

from typing import Any, Callable
import requests
from functools import wraps

def access_nested_map(nested_map: dict, path: tuple) -> Any:
    """Access a nested map using a sequence of keys"""
    current = nested_map
    for key in path:
        current = current[key]
    return current

def get_json(url: str) -> dict:
    """Get JSON content from a URL"""
    response = requests.get(url)
    return response.json()

def memoize(func: Callable) -> property:
    """Memoize a method: cache the result"""
    attr_name = "_memoized_" + func.__name__

    @property
    @wraps(func)
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)
    return wrapper
