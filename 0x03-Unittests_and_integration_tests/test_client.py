#!/usr/bin/env python3
"""
Unit tests for the `client` module.
Covers integration with the GitHub API using mocked responses.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for the GithubOrgClient class."""

    @patch('client.get_json', return_value=org_payload)
    def test_org(self, mock_get_json):
        """
        Test that `org` returns the correct payload
        and calls get_json with the right URL.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.org, org_payload)
        mock_get_json.assert_called_once_with("https://api.github.com/orgs/google")

    def test_public_repos_url(self):
        """
        Test that `_public_repos_url` returns the correct URL.
        """
        with patch.object(
            GithubOrgClient,
            'org',
            new_callable=PropertyMock,
            return_value=org_payload
        ):
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url,
                             org_payload["repos_url"])

    @patch('client.get_json', return_value=repos_payload)
    def test_public_repos(self, mock_get_json):
        """
        Test that `public_repos` returns the expected list of repos
        and that get_json is called with the repos_url.
        """
        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock,
            return_value="https://api.github.com/orgs/google/repos"
        ):
            client = GithubOrgClient("google")
            self.assertEqual(client.public_repos(), expected_repos)
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/google/repos"
            )

    @parameterized.expand([
        ("google", apache2_repos, "license", "apache-2.0", True),
        ("google", apache2_repos, "license", "mit", False),
    ])
    def test_has_license(self, name, repo, key, license_key, expected):
        """
        Test that `has_license` correctly determines if a repo
        has the specified license.
        """
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )
