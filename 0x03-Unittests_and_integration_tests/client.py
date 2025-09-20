#!/usr/bin/env python3
"""GithubOrgClient module"""

import requests
from typing import List, Dict, Optional
from utils import memoize, get_json


class GithubOrgClient:
    """Client for fetching data from GitHub organizations"""

    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name: str) -> None:
        """Initialize client with org name"""
        self._org_name = org_name

    @memoize
    def org(self) -> Dict:
        """Return organization info"""
        return get_json(self.ORG_URL.format(org=self._org_name))

    @property
    def _public_repos_url(self) -> str:
        """Return the URL of the org's public repos"""
        return self.org["repos_url"]

    def public_repos(self, license: Optional[str] = None) -> List[str]:
        """Return list of repo names, optionally filtered by license"""
        repos = get_json(self._public_repos_url)
        names = [repo["name"] for repo in repos]

        if license is None:
            return names

        return [
            repo["name"] for repo in repos
            if self.has_license(repo, license)
        ]

    @staticmethod
    def has_license(repo: Dict, license_key: str) -> bool:
        """Check if repo has given license"""
        return repo.get("license", {}).get("key") == license_key
