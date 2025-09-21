#!/usr/bin/env python3
"""Integration tests for GithubOrgClient"""

import unittest
from unittest.mock import patch, MagicMock
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @patch("client.requests.get")
    def test_public_repos(self, mock_get):
        """Test public_repos returns expected repos list"""
        # Mock org response
        mock_org_resp = MagicMock()
        mock_org_resp.json.return_value = org_payload

        # Mock repos response
        mock_repos_resp = MagicMock()
        mock_repos_resp.json.return_value = repos_payload

        # requests.get should return org_payload first, then repos_payload
        mock_get.side_effect = [mock_org_resp, mock_repos_resp]

        client = GithubOrgClient("google")
        result = client.public_repos()

        self.assertEqual(result, expected_repos)

    @patch("client.requests.get")
    def test_public_repos_with_license(self, mock_get):
        """Test public_repos filters repos by license"""
        # Mock org response
        mock_org_resp = MagicMock()
        mock_org_resp.json.return_value = org_payload

        # Mock repos response
        mock_repos_resp = MagicMock()
        mock_repos_resp.json.return_value = repos_payload

        mock_get.side_effect = [mock_org_resp, mock_repos_resp]

        client = GithubOrgClient("google")
        result = client.public_repos(license="apache-2.0")

        self.assertEqual(result, apache2_repos)


if __name__ == "__main__":
    unittest.main()
