# -*- coding: utf-8 -*-


import itertools as itt
import logging
import os
from subprocess import CalledProcessError, check_output
from typing import Any, Dict, Iterable, Mapping, Optional, Set

import more_itertools
import pystow
import requests

logger = logging.getLogger(__name__)
HERE = os.path.dirname(os.path.abspath(__file__))
MAIN_BRANCH = "main"


def has_token() -> bool:
    """Check if there is a github token available."""
    return pystow.get_config("github", "token") is not None


def get_headers(token: Optional[str] = None, accept: str = "application/vnd.github.v3+json"):
    """Get github headers."""
    headers = {
        "Accept": accept,
    }
    token = pystow.get_config("github", "token", passthrough=token)
    if token:
        headers["Authorization"] = f"token {token}"
    return headers


def requests_get(
    path: str, token: Optional[str] = None, params: Optional[Mapping[str, Any]] = None
):
    """Send a get request to the GitHub API."""
    path = path.lstrip("/")
    return requests.get(
        f"https://api.github.com/{path}",
        headers=get_headers(token=token),
        params=params,
    ).json()


def get_stargazers(owner, repo):
    # https://docs.github.com/en/rest/activity/starring?apiVersion=2022-11-28
    path = f"repos/{owner}/{repo}/stargazers"
    page = 1
    r = requests_get(path, params={"per_page": 100, "page": page})