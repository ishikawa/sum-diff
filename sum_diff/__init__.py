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
You are tasked with writing a Pull Request (PR) title and description based on a git branch name and
a code diff. Follow these instructions carefully to complete the task.
"""

USER_PROMPT = """
First, here is the git branch name:
<branch_name>
{{branch_name}}
</branch_name>

Now, here is the code diff:
<code_diff>
{{diff}}
</code_diff>

Analyze the branch name:
1. Look for keywords or patterns that indicate the purpose of the changes (e.g., "feature", "bugfix", "hotfix", "refactor").
2. Identify any ticket or issue numbers if present.
3. Note any specific components or areas of the codebase mentioned.

Review the code diff:
1. Identify the files that have been modified, added, or deleted.
2. Understand the main changes and their purpose.
3. Look for any significant additions or removals of functionality.
4. Note any changes to dependencies or configuration files.

Writing the PR title:
1. Keep it concise (50-70 characters if possible).
2. Start with a capital letter and use present tense.
3. Summarize the main purpose of the changes.
4. Include the ticket or issue number if present in the branch name.

Composing the PR description:
1. Provide a brief overview of the changes (1-2 sentences).
2. List the main components or areas affected.
3. Explain the reason for the changes and their impact.
4. Mention any important implementation details.
5. Include any necessary instructions for testing or deployment.
6. Add any relevant links or references.

Output your response in the following format:
<pr_title>
Your PR title here
</pr_title>

<pr_description>
Your PR description here
</pr_description>

Remember to base your PR title and description solely on the information provided in the branch name
and code diff. Do not include any external information or assumptions beyond what is given.
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
