# Git Push Automation
## What is it?
A terminal-based Python tool that handles all the necessary Git commands to push your code to GitHub safely and smoothly. It’s designed to simplify the most common headaches faced by both beginners and seasoned developers using Git.

With this tool, you don’t need to memorize a long list of Git commands or fear making mistakes — it’s got your back.

Handles common issues like:
- Invalid or incomplete Git commands
- Missing or non-Git directories
- Forgetting to add/stage files
- Empty commits / Clean working tree
- Active rebase states
- Merge conflicts
- Detached HEAD state
- Switching or creating branches
- Pulling with rebase before pushing

All you have to do is enter:
- Your GitHub repository name (Create it manully if it does not exist)
- Your local project folder  
- A commit message  

And just like that — your project is up on GitHub!

## Stats

![Version](https://img.shields.io/badge/Version-1.0.1-blue.svg)
![Status](https://img.shields.io/badge/Status-Completed-green.svg)

## File Structure
```bash
📂Git Push Automation
 ┣ 📄 automate.py              # The file that is supposed to be executed to run the program
 ┣ 📄 git.py                   # Contains all utility git commands that prevents unexpected git errors
 ┣ 📄 README.md                # You’re looking at it 😎 (Current version details)
 ┗ 📄 CHANGELOG.md             # Version history
```

## How to Run
- First of all, ensure that the latest version of Python and git are installed.
- Make sure you generate a personal access token (PAT) from GitHub.
- Create a .env file with the following structure:
```bash
GITHUB_USERNAME=your_username
GITHUB_TOKEN=your_pat
BASE_PROJECTS_PATH=C:/Your/Path/To/Coding/Projects
```
- To start the application, run the `automate.py` file.

## Inspiration
I built this tool because pushing code with Git used to feel like a boss battle - especially when I was just starting out. Typos, forgotten stages, pull issues, rebase confusion — it was a lot.

So instead of wrestling with Git every time, I created a Python script that could handle it all for me. Now it’s smooth, error-proof, and beginner-friendly. Plus, it helps you focus more on building and less on debugging your Git workflow.

## Contribution
Feel free to make an edit or change to this project to improve its stability. You may do so by first pulling a request or an issue to talk about it. Lets make Git a little less scary! All are welcome!
