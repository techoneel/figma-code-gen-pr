# GitHub PR Automation Service

import requests
import os

GITHUB_API = "https://api.github.com"

class GitHubService:
    def __init__(self, token: str, repo: str):
        self.token = token
        self.repo = repo
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        }

    def create_branch(self, branch_name: str, base: str = "main"):
        ref_url = f"{GITHUB_API}/repos/{self.repo}/git/ref/heads/{base}"
        base_ref = requests.get(ref_url, headers=self.headers).json()
        sha = base_ref["object"]["sha"]

        create_ref_url = f"{GITHUB_API}/repos/{self.repo}/git/refs"
        data = {
            "ref": f"refs/heads/{branch_name}",
            "sha": sha
        }
        requests.post(create_ref_url, headers=self.headers, json=data)

    def create_file(self, path: str, content: str, message: str, branch: str):
        url = f"{GITHUB_API}/repos/{self.repo}/contents/{path}"
        data = {
            "message": message,
            "content": content.encode("utf-8").decode("utf-8"),
            "branch": branch
        }
        requests.put(url, headers=self.headers, json=data)

    def create_pr(self, title: str, body: str, head: str, base: str = "main"):
        url = f"{GITHUB_API}/repos/{self.repo}/pulls"
        data = {
            "title": title,
            "body": body,
            "head": head,
            "base": base
        }
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()
