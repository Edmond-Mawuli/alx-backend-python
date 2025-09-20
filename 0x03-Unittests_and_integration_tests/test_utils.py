#!/usr/bin/env python3
"""Unit tests for utils.py"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
import utils


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map function"""

    def test_access_nested_map(self):
        """Test access_nested_map with simple paths (no decorator for Task 0)"""
        self.assertEqual(utils.access_nested_map({"a": 1}, ("a",)), 1)
        self.assertEqual(utils.access_nested_map({"a": {"b": 2}}, ("a",)),
                         {"b": 2})
        self.assertEqual(utils.access_nested_map({"a": {"b": 2}}, ("a", "b")),
                         2)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test access_nested_map raises KeyError for missing key"""
        with self.assertRaises(KeyError) as ctx:
            utils.access_nested_map(nested_map, path)
        # KeyError string for missing key is quoted, e.g. "'b'"
        self.assertEqual(str(ctx.exception), f"'{path[-1]}'")


class TestGetJson(unittest.TestCase):
    """Unit tests for get_json"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """Test get_json returns expected payload (requests.get mocked)"""
        with patch("utils.requests.get") as mock_get:
            mock_resp = Mock()
            mock_resp.json.return_value = test_payload
            mock_get.return_value = mock_resp

            result = utils.get_json(test_url)

            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Unit tests for memoize decorator"""

    def test_memoize(self):
        """Test that memoize caches the result of a method"""

        class TestClass:
            def a_method(self):
                return 42

            @utils.memoize
            def a_property(self):
                return self.a_method()

        obj = TestClass()
        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            # Calling twice should return same result, but wrapped method called once
            res1 = obj.a_property
            res2 = obj.a_property

            self.assertEqual(res1, 42)
            self.assertEqual(res2, 42)
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
