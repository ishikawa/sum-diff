import os
import click

from dotenv import load_dotenv
from openai import OpenAI

from sum_diff.git import (
    git_current_branch,
    git_parent_branch,
    git_diff_from_parent,
    git_logs_from_parent,
)

load_dotenv(".env")

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

SYSTEM_PROMPT = """
You are a software engineer who has been asked to explain your changes in a short title.
You will be provided with commit messages and a diff of the changes, and you need to explain them in a way that is easy to understand.
"""

USER_PROMPT = """
## Commit Messages

{logs}

## Diff

{diff}
"""


@click.command()
def main():
    current_branch = git_current_branch()
    parent_branch = git_parent_branch(current_branch)
    diff = git_diff_from_parent(parent_branch)
    logs = git_logs_from_parent(parent_branch)
    print(diff)
    print(logs)

    client = OpenAI(api_key=OPENAI_API_KEY)

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": USER_PROMPT.format(logs=logs, diff=diff),
            },
        ],
    )

    print(completion.choices[0].message.content)
