#!/usr/bin/env python3
"""Client for interacting with GitHub API"""

from typing import List
from utils import get_json, memoize

class GithubOrgClient:
    """GitHub Organization Client"""

    def __init__(self, org_name: str) -> None:
        self.org_name = org_name

    def org(self) -> dict:
        """Return organization JSON from GitHub API"""
        return get_json(f"https://api.github.com/orgs/{self.org_name}")

    @memoize
    def _public_repos_url(self) -> str:
        """Return URL for public repos"""
        return self.org().get("repos_url", "")

    def public_repos(self) -> List[str]:
        """Return list of public repo names"""
        return [repo["name"] for repo in get_json(self._public_repos_url)]

    @staticmethod
    def has_license(repo: dict, license_key: str) -> bool:
        """Return True if repo has a specific license"""
        return repo.get("license", {}).get("key") == license_key
