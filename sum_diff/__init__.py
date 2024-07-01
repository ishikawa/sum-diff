import os
import click

from dotenv import load_dotenv
import anthropic


from sum_diff.git import (
    git_current_branch,
    git_parent_branch,
    git_diff_from_parent,
)

load_dotenv(".env")

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

# Prompt library documentation
# https://docs.anthropic.com/en/prompt-library/code-clarifier
#
# Pull request best practices
# https://blog.pragmaticengineer.com/pull-request-or-diff-best-practices/
SYSTEM_PROMPT = """
You are a software engineer who has been asked to explain code changes. Your task is to explain them
in a concise title and description. The goal is to help the reviewer understand what the code does
and why it was changed.

You will be provided with:

- The branch name
- Diff of the changes

and ou need to explain code changes in a concise title and description.

Follow these steps to generate an appropriate title and description:

1. Read the _Branch name_ to understand the context of the changes.
2. Read the _Diff_ to understand how the changes were made. Extracting some key points to generate a title and description.
3. Generate an appropriate title and description following the guidelines below.

## Guidelines for clear and concise title

### Starting the title with uppercase and the first word being a verb in present tense.

- GOOD: "Change Swiss tax calculation for new regulation"
- NOT GOOD: "changed Swiss tax calculation for new regulation"
- NOT GOOD: "Ability to calculate Swiss tax for new regulation"

### Keep the title short, but expressive enough to signal what the reviewer can expect.

Let's say you're working on an accounting software and there is a new business requirement on how to
calculate tax for Switzerland.

- GOOD: A title like "Changes for Swiss tax calculation" is concise.
- GOOD: A title like "Change for tax calculation in Switzerland for new regulation" is still
  concise, with more context.
- BAD: A title like "Adding new tax parameters" or "Change tax logic" are overly generic and won't
  help reviewers.
- BAD: "Changes for calculation" is too generic.
- NOT GOOD: "TaxInternals structure update and CalculateEffectiveRate changes in case of Swiss
  country code" is too detailed and should be in the description, not the title.
- NOT GOOD: "Change tax calculation for Swiss businesses in the TX bracket effective from 2019
  following new regulations" is too verbose.

## Output Format

- Don't surround title with quotes
- Enclose programming language elements in backticks (e.g., `if`, `while`).
"""

USER_PROMPT = """
## Branch name

{branch_name}

## Diff

{diff}
"""


@click.command()
def main():
    current_branch = git_current_branch()
    parent_branch = git_parent_branch(current_branch)
    diff = git_diff_from_parent(parent_branch)
    # print(current_branch)
    # print(parent_branch)
    # print(diff)

    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key=ANTHROPIC_API_KEY,
    )

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        temperature=0,
        system=SYSTEM_PROMPT.format(branch_name=current_branch, diff=diff),
        messages=[
            {
                "role": "user",
                "content": USER_PROMPT.format(branch_name=current_branch, diff=diff),
            },
        ],
    )

    for c in message.content:
        if c.type == "text":
            print(c.text)
