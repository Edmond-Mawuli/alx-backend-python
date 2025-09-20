#!/usr/bin/env python3
"""Fixtures for integration and unit tests"""

org_payload = {
    "login": "test",
    "id": 1,
    "repos_url": "https://api.github.com/orgs/test/repos"
}

repos_payload = [
    {"id": 101, "name": "repo1", "license": {"key": "mit"}},
    {"id": 102, "name": "repo2", "license": {"key": "apache-2.0"}},
    {"id": 103, "name": "repo3", "license": {"key": "gpl-3.0"}},
]

# List of just the repo names
expected_repos = ["repo1", "repo2", "repo3"]

# Filtered repos with apache2 license
apache2_repos = ["repo2"]
