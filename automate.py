import os
import subprocess
from dotenv import load_dotenv
from colorama import init, Fore, Style
from pathlib import Path

from git import Git

class Automate:
    """ Automates Git push task. """

    def __init__(self):
        init(autoreset=True)
        self.fetch_credentials()
        self.git_agent = Git(self.username, self.token)

        self.welcome()
        self.connect_to_git_page()
        
    def fetch_credentials(self):
        """ Fetch GitHub credentials from enviroment variables. """
        load_dotenv()
        self.username = os.getenv("GITHUB_USERNAME")
        self.token = os.getenv("GITHUB_TOKEN")
    
    def welcome(self):
        """ Display a welcome message. """
        print("Git Push Automation Tool [v1.0.0]")
        print()
        if self.username is None or self.token is None:
            print(Fore.RED + Style.BRIGHT + "ERROR: GitHub credentials not found.")
            print(Fore.MAGENTA + Style.BRIGHT + "HELP: Ensure you have a .env file with GITHUB_USERNAME and GITHUB_TOKEN set.")
        else:
            print("Welcome! Let's push a project into your GitHub profile!")
            print("Just to make sure,", Fore.CYAN + self.username, "is the username of your profile.")
        print()
    
    def connect_to_git_page(self):
        repo_name = prompt_input("Enter GitHub repositary name")
        print("Finding repository on GitHub...")
        if self.git_agent.is_github_page(repo_name):
            repo_path = f"https://github.com/{self.username}/{repo_name}"
            print(Fore.GREEN + Style.BRIGHT + f"SUCCESS: Repository has been found on GitHub!")
            print()
            self.push_to_github(repo_name, repo_path)
        else:
            print(Fore.RED + Style.BRIGHT + f"ERROR: Desired repository does not exist on GitHub.")
            print(Fore.MAGENTA + Style.BRIGHT + f"HELP: Consider creating a GitHub page first, or check that the repository name is correct.")

    def push_to_github(self, repo_name: str, repo_path: str):
        """ Push the project to GitHub. """
        remote_url = f"https://{self.username}:{self.token}@github.com/{self.username}/{repo_name}.git"
        project_folder = prompt_input("Enter the name of your desired project folder")

        # Step 1: Change directory to desired project folder
        base_projects_path = os.getenv("BASE_PROJECTS_PATH")
        if base_projects_path is None:
            print(Fore.RED + Style.BRIGHT + "ERROR: Unable to fetch parent path (for absolute path).")
            print(Fore.MAGENTA + Style.BRIGHT + "HELP: Ensure you have a .env file with BASE_PROJECTS_PATH set to your projects directory.")
            return
        dirs = Path(base_projects_path).iterdir()
        for path in dirs:
            project_path = f"{path}/{project_folder}"
            try:
                os.chdir(project_path) # Change directory to passed path
                break
            except FileNotFoundError:
                continue
        else:
            print(Fore.RED + Style.BRIGHT + f"ERROR: {project_folder} cannot be found.")
            print(Fore.MAGENTA + Style.BRIGHT + "HELP: Ensure the project folder exists in the path specified. Possibly even the path.")
            return
        
        # Step 2: Initialise git repository if not already done
        print("Init status: ", end="")
        if not Git.is_git_repo():
            subprocess.run(["git", "init"], check=True)
            print("New git repository initialised.")
        else:
            print("Already a git repository.")
        
        # Step 3: Pull changes from remote if it exists
        should_stage_later = True  # flag to control final staging

        if Git.is_rebasing():
            print(Fore.YELLOW + "WARNING: A rebase is currently in progress.")

            while True:
                print()
                choice = prompt_input("Do you want to (c)ontinue, (a)bort, or (s)kip rebase handling for now? [c/a/s]").lower()

                if choice == "c":
                    print("Staging resolved changes...")
                    subprocess.run(["git", "add", "."], check=True)
                    subprocess.run(["git", "rebase", "--continue"], check=True)
                    print("Rebase continued successfully.")
                    should_stage_later = False  # already staged
                    break

                elif choice == "a":
                    subprocess.run(["git", "rebase", "--abort"], check=True)
                    print("Rebase aborted.")
                    print("Pulling latest changes from remote...")
                    subprocess.run(["git", "pull", "origin", "main", "--rebase"], check=True)
                    break

                elif choice == "s":
                    print("Skipping rebase handling. Rebase still active.")
                    break
        else:
            # No rebase active — safe to pull
            print("Pulling latest changes from remote...")
            subprocess.run(["git", "pull", "origin", "main", "--rebase"], check=True)
            print("Pulled latest changes successfully.")

        # Only stage if not already done
        if should_stage_later:
            print("Staging all local changes...")
            subprocess.run(["git", "add", "."], check=True)

        # Step 4: Commit changes
        print("Commiting changes...")
        result = subprocess.run(["git", "diff", "--cached", "--quiet"])
        if result.returncode != 0:
            commit_msg = prompt_input("Enter commit message (default: Initial commit)") or "Initial commit"
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        else:
            print("No changes to commit. Working tree is clean.")
        
        # Step 5: Set remote URL
        subprocess.run(["git", "remote", "remove", "origin"], check=False)
        subprocess.run(["git", "remote", "add", "origin", remote_url], check=True)

        # Step 6: Push changes to GitHub in main branch
        result = subprocess.run(["git", "symbolic-ref", "--short", "HEAD"], capture_output=True, text=True)
        
        if result.returncode != 0: # Detached HEAD state
            if "main" in Git.get_branches():
                subprocess.run(["git", "checkout", "main"], check=True)
            else:
                subprocess.run(["git", "checkout", "-b", "main"], check=True)
        else:
            current_branch = result.stdout.strip()
            if current_branch != "main":
                if "main" in Git.get_branches():   
                    subprocess.run(["git", "checkout", "main"], check=True)
                else:
                    subprocess.run(["git", "branch", "-M", "main"], check=True)  # Ensure main branch
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
        
        print()
        print(Fore.GREEN + Style.BRIGHT + "SUCCESS: Pushed your project into GitHub!")
        print("Open this link (Ctrl + Click) to view your commit:", repo_path, sep="\t\t")

def prompt_input(prompt: str) -> str:
    """ Helper function to prompt user input with a custom style. """
    return input(prompt + Fore.CYAN + "\n>>> " + Style.RESET_ALL)

if __name__ == "__main__":
    Automate()
    
    print()
    prompt_input("Press something to exit")