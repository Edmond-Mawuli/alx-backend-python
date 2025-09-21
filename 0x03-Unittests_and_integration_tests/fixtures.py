#!/usr/bin/env python3
"""Fixtures for unit tests"""

org_payload = {
    "login": "google",
    "id": 1,
    "repos_url": "https://api.github.com/orgs/google/repos"
}

repos_payload = [
    {"id": 1, "name": "repo1"},
    {"id": 2, "name": "repo2"},
    {"id": 3, "name": "repo3"},
]

expected_repos = ["repo1", "repo2", "repo3"]
