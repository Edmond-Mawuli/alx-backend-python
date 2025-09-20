#!/usr/bin/env python3
"""Unit tests for utils.py"""

import unittest
from parameterized import parameterized
from unittest.mock import patch
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map function"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns expected results"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that access_nested_map raises KeyError for invalid paths"""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test cases for get_json function"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test get_json returns expected result with mocked requests.get"""
        mock_get.return_value.json.return_value = test_payload

        result = get_json(test_url)
        self.assertEqual(result, test_payload)

        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Test cases for memoize decorator"""

    def test_memoize(self):
        """Test that memoize caches method result"""
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(
            TestClass,
            "a_method",
            return_value=42
        ) as mock_method:
            obj = TestClass()
            # First call should use a_method
            self.assertEqual(obj.a_property, 42)
            # Second call should not call a_method again
            self.assertEqual(obj.a_property, 42)

            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
