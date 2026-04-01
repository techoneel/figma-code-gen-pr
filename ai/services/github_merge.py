# GitHub Auto Merge Service

import requests

class GitHubMergeService:
    def __init__(self, token: str, repo: str):
        self.token = token
        self.repo = repo
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        }

    def merge_pr(self, pr_number: int):
        url = f"https://api.github.com/repos/{self.repo}/pulls/{pr_number}/merge"
        response = requests.put(url, headers=self.headers)
        return response.json()
