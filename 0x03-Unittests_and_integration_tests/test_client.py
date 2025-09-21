#!/usr/bin/env python3
"""
Unit and integration tests for the GithubOrgClient class.
"""

import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for the GithubOrgClient class."""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected, mock_get_json):
        """Test that GithubOrgClient.org returns correct payload."""
        mock_get_json.return_value = expected
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test that _public_repos_url returns repos_url from org payload."""
        with patch.object(
            GithubOrgClient,
            'org',
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = org_payload
            client = GithubOrgClient("google")
            self.assertEqual(
                client._public_repos_url,
                org_payload["repos_url"]
            )

    @patch('client.get_json', return_value=repos_payload)
    def test_public_repos(self, mock_get_json):
        """
        Test that public_repos returns expected repo names
        and calls get_json with repos_url.
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
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns correct boolean."""
        client = GithubOrgClient("google")
        self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class([
    {"org_payload": org_payload,
     "repos_payload": repos_payload,
     "expected_repos": expected_repos,
     "apache2_repos": apache2_repos}
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient using payload fixtures."""

    @classmethod
    def setUpClass(cls):
        """Set up patchers for get_json and requests.get."""
        cls.get_patcher = patch('client.get_json', return_value=repos_payload)
        cls.mock_get_json = cls.get_patcher.start()

        cls.req_patcher = patch('requests.get')
        cls.mock_requests = cls.req_patcher.start()
        mock_response = MagicMock()
        mock_response.json.return_value = org_payload
        cls.mock_requests.return_value = mock_response

    @classmethod
    def tearDownClass(cls):
        """Stop all patchers."""
        cls.get_patcher.stop()
        cls.req_patcher.stop()

    def test_public_repos_integration(self):
        """Integration test for public_repos method."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test for public_repos filtered by license."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


if __name__ == "__main__":
    unittest.main()
