# Thalia Bot

Just a simple Discord bot to tell a random programming joke :D

Use [this link](https://discord.com/api/oauth2/authorize?client_id=990877632235208784&permissions=277025396800&scope=bot%20applications.commands) to add this bot to your Discord channel!

## Usages

`tell-geek-joke` Send a random programming joke

`setup-daily-joke` The bot will send a joke everyday

`help` Display the list of commands and their usages

---

## Dev Setup

A complete guild to setup your development environment :D

### Requirements

`python` version `3.9` or higher.

Make sure you also already installed `pip` and `venv` for your Python.

### Setup Automation

Try run the `bin/setup.py` script to automate your setup. If things work out, you can start development immeidately :)

If the auto-setup fails, continue with the manual setup instructions.

### Create Virtual Environment

Start by creating your isolated Python environment with `venv`:

```bash
python3 -m venv .venv
```
In this case, `.venv` is the name of the directory containing your Python executable and other files. You can name it anything you want, but `.venv` is the most common name.

### Install Packages

You will notice there are 2 files named `requirements-dev.txt` and `requirements.txt`. These files contain the name of the `pip` packages.

`requirements-dev.txt` contains the packages needed to enhance developer's experience. While `requirements.txt` contains the packages needed for the application to run.

Install all of these by running:

```bash
pip install -r requirements-dev.txt
pip install -r requirements.txt
```

### Pre-commit

Inorder to make sure the codebase is clean and the style is consistent between many developers, we use a few lint tools to detect and auto-fix (if possible). These can be found in `.pre-commit-config.yaml`.
These lint tools will be run when you commit your code and you can only successfully commit if . You can also run it without commiting: `pre-commit run --all-files`

### You're good to write your code now! :)
