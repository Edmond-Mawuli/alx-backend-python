#!/usr/bin/env python3
"""Fixtures for GithubOrgClient integration tests"""

org_payload = {"login": "org_name", "repos_url": "http://example.com/repos"}
repos_payload = [{"name": "repo1"}, {"name": "repo2"}, {"name": "apache2"}]
expected_repos = ["repo1", "repo2", "apache2"]
apache2_repos = ["apache2"]
