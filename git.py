import os
import subprocess
import requests
from colorama import init, Fore, Style

class Git:
    """ A class to handle internal Git operations. """

    def __init__(self, username: str, token: str):
        self.username = username
        self.token = token

    def is_github_page(self, repo_name: str) -> bool:
        """ Returns True if the passed repo name exists on GitHub."""
        url = f"https://api.github.com/repos/{self.username}/{repo_name}"
        headers = {"Authorization": f"token {self.token}"}
        response = requests.get(url, headers=headers)
        return response.status_code == 200 # 200 = Page exists

    @staticmethod
    def is_git_repo() -> bool:
        """ Returns True if the given path is a Git repository. """
        result = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], capture_output=True)
        return result.returncode == 0
    @staticmethod
    def get_branches() -> list[str]:
        """ Returns True if the passed branch name exists in the current repository. """
        branches = subprocess.run(["git", "branch"], capture_output=True, text=True).stdout.splitlines()
        branches = [branch.strip("* ").strip() for branch in branches]
        return branches

    @staticmethod
    def is_rebasing() -> bool:
        """ Returns True if the current repository is in a rebase state. """
        git_dir = os.path.join(os.getcwd(), ".git")
        rebase_paths = [
            "rebase-apply",
            "rebase-merge",
        ]
        return any(os.path.exists(os.path.join(git_dir, path)) for path in rebase_paths)

def prompt_input(prompt: str) -> str:
    """ Helper function to prompt user input with a custom style. """
    return input(prompt + Fore.CYAN + "\n>>> " + Style.RESET_ALL)

if __name__ == "__main__":
    init(autoreset=True)
    print(Fore.RED + Style.BRIGHT + "ERROR: Attempt to run git.py directly. This file is not meant to be executed.")
    print(Fore.MAGENTA + Style.BRIGHT + "HELP: Run automate.py instead to use git automation features.")

    print()
    prompt_input("Press something to exit")
