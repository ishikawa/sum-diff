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

# Pull request best practices
# https://blog.pragmaticengineer.com/pull-request-or-diff-best-practices/
SYSTEM_PROMPT = """
You are a software engineer who has been asked to explain your changes.

You will be provided with:

1. Brief description of the changes (Most important)
2. Commit messages
3. Diff of the changes

and you need to explain them in a short and concise title ONLY.

## Guidelines for clear and concise title:

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
- NOT GOOD: "TaxInternals structure update and CalculateEffectiveRate changes in case of Swiss
  country code" is too detailed and should be in the description, not the title.
- NOT GOOD: "Change tax calculation for Swiss businesses in the TX bracket effective from 2019
  following new regulations" is too verbose.

## Output Format

- Don't surround title with quotes
- Enclose programming language elements in backticks (e.g., `if`, `while`).

So your brief description of the changes is:
"""

USER_PROMPT = """
## Brief description of the changes

プロトタイプを実装した。

## Commit messages

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
        # model="gpt-4o",
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": USER_PROMPT.format(logs=logs, diff=diff),
            },
        ],
        temperature=0.0,
    )

    print(completion.choices[0].message.content)
