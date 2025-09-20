#!/usr/bin/env python3
"""Unit tests for utils.py functions"""

import unittest
from unittest.mock import patch
from parameterized import parameterized, param
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map function"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map: dict, path: tuple, expected):
        """Test access_nested_map returns expected value"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map: dict, path: tuple):
        """Test access_nested_map raises KeyError for missing key"""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), path[-1])


class TestGetJson(unittest.TestCase):
    """Unit tests for get_json function"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url: str, test_payload: dict):
        """Test get_json returns expected payload"""
        from utils import requests
        mock_resp = unittest.mock.Mock()
        mock_resp.json.return_value = test_payload
        with patch("utils.requests.get", return_value=mock_resp) as mock_get:
            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test memoize decorator"""

    def test_memoize(self):
        """Test that memoize caches a method call"""

        class TestClass:
            """Test class for memoize decorator"""

            def a_method(self) -> int:
                """Return a fixed integer"""
                return 42

            @memoize
            def a_property(self) -> int:
                """Return the result of a_method, memoized"""
                return self.a_method()

        test_obj = TestClass()
        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            result1 = test_obj.a_property
            result2 = test_obj.a_property
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()
