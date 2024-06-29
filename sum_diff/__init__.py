import os
import click
from dotenv import load_dotenv
from sum_diff.git import (
    git_current_branch,
    git_parent_branch,
    git_diff_from_parent,
    git_logs_from_parent,
)

load_dotenv(".env")

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


@click.command()
def main():
    current_branch = git_current_branch()
    parent_branch = git_parent_branch(current_branch)
    diff = git_diff_from_parent(parent_branch)
    logs = git_logs_from_parent(parent_branch)
    print(diff)
    print(logs)
