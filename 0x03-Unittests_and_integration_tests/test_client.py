#!/usr/bin/env python3
"""
Unittests for client.py module
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        test_instance = GithubOrgClient(org_name)
        test_instance.org
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the right URL"""
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock,
        ) as mock_org:
            payload = {"repos_url": "https://api.github.com/orgs/test/repos"}
            mock_org.return_value = payload

            client = GithubOrgClient("test")
            self.assertEqual(client._public_repos_url, payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns correct list of repos"""
        test_payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = test_payload

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
        ) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/test/repos"

            client = GithubOrgClient("test")
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test/repos"
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean"""
        client = GithubOrgClient("test")
        self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class([
    {"org_payload": TEST_PAYLOAD[0],
     "repos_payload": TEST_PAYLOAD[1],
     "expected_repos": TEST_PAYLOAD[2],
     "apache2_repos": TEST_PAYLOAD[3]},
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests with fixtures"""

    @classmethod
    def setUpClass(cls):
        """Set up mock for requests.get"""
        config = {"return_value.json.side_effect": [
            cls.org_payload, cls.repos_payload,
            cls.org_payload, cls.repos_payload,
        ]}
        cls.get_patcher = patch("requests.get", **config)
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Stop patcher after tests"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test for public_repos"""
        client = GithubOrgClient("test")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test for public_repos filtering by license"""
        client = GithubOrgClient("test")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
