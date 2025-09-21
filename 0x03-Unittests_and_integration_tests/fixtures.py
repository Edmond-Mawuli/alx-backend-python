#!/usr/bin/env python3
"""
Fixtures module containing payloads for unit and integration tests.
"""

# Payload returned for the organization endpoint
org_payload = {
    "login": "google",
    "repos_url": "https://api.github.com/orgs/google/repos",
    "id": 1342004,
}

# Payload returned for the repos endpoint
repos_payload = [
    {
        "id": 7697149,
        "name": "episodes.dart",
        "owner": {"login": "google", "id": 1342004},
        "private": False,
        "license": {"key": "apache-2.0", "name": "Apache License 2.0"},
    },
    {
        "id": 7776515,
        "name": "cpp-netlib",
        "owner": {"login": "google", "id": 1342004},
        "private": False,
    },
]

# Expected list of repo names
expected_repos = ["episodes.dart", "cpp-netlib"]

# Subset of repos licensed under Apache 2.0
apache2_repos = ["episodes.dart"]
