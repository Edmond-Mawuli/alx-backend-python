#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test that public_repos returns the expected list of repo names
        and that get_json is called with the correct URL.
        """
        org_payload, repos_payload = TEST_PAYLOAD[0]
        expected_repos = [repo["name"] for repo in repos_payload]

        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock,
            return_value=org_payload["repos_url"]
        ):
            client = GithubOrgClient("google")
            mock_get_json.return_value = repos_payload

            self.assertEqual(client.public_repos(), expected_repos)
            mock_get_json.assert_called_once_with(org_payload["repos_url"])

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test that has_license correctly checks if a repo
        has a given license key.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.has_license(repo, license_key), expected)


if __name__ == "__main__":
    unittest.main()
