import os
from os import path
import re
import click
import xml.etree.ElementTree as ET

from dotenv import load_dotenv
import anthropic


from sum_diff.git import (
    git_current_branch,
    git_parent_branch,
    git_diff_from_parent,
)
from sum_diff.utils import parse_pr_example

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
## Input

First, here is the git branch name:
<branch_name>
{branch_name}
</branch_name>

Now, here is the code diff:
<code_diff>
{diff}
</code_diff>

## Analysis

### Analyze the branch name:
1. Look for keywords or patterns that indicate the purpose of the changes (e.g., "work", "fix",
"feature", "bugfix", "hotfix", "refactor").
2. Identify any ticket or issue numbers if present.
3. Note any specific components or areas of the codebase mentioned.

### Review the code diff:
1. Identify the files that have been modified, added, or deleted.
2. Understand the main changes and their purpose.
3. Look for any significant additions or removals of functionality.
4. Note any changes to dependencies or configuration files.

## Writing the PR title:
1. Keep it concise (50-70 characters if possible).
2. Start with a capital letter and use present tense.
3. Summarize the main purpose of the changes.
4. Include the ticket or issue number if present in the branch name.
5. Use backticks (`) to enclose programming language keywords, identifiers, library class names, or
constants that would benefit from being highlighted.

## Composing the PR description:
1. Provide a brief overview of the changes (1-2 sentences).
2. List the main components or areas affected.
3. Explain the reason for the changes and their impact.
4. Mention any important implementation details.
5. Add any relevant links or references.
6. Use backticks (`) to enclose programming language keywords, identifiers, library class names, or
constants that would benefit from being highlighted.
7. When appropriate, include code examples using Markdown code blocks (```). Provide an explanation
of the intent and content of the code example.

## Output

Format your response in the following way:

<pr_title>
Your PR title here
</pr_title>

<pr_description>
Your PR description here
</pr_description>

Remember to base your PR title and description solely on the information provided in the branch name
and code diff. Do not include any external information or assumptions beyond what is given.

**IMPORTANT**:

- Output should be in {lang}.
"""


@click.command()
# 言語を選択するオプション。デフォルトは英語であり、日本語を選択することもできる。
@click.option(
    "--lang",
    "-l",
    type=click.Choice(["en", "ja"], case_sensitive=False),
    default="en",
    help="Choose the language for the output.",
)
def main(lang):
    output_lang = "Japanese" if lang == "ja" else "English"

    # Git operations
    current_branch = git_current_branch()
    parent_branch = git_parent_branch(current_branch)
    diff = git_diff_from_parent(parent_branch)
    # print(current_branch)
    # print(parent_branch)
    # print(diff)

    # Read example outputs for few shots learning from the directory "examples/"
    examples_dir = path.join(path.dirname(__file__), "examples")
    examples = []

    for filename in os.listdir(examples_dir):
        if filename.endswith(".md"):
            with open(path.join(examples_dir, filename)) as f:
                examples.append(parse_pr_example(f.read()))

    # print(examples)

    # Construct the user prompt
    user_prompt = USER_PROMPT.format(
        branch_name=current_branch, diff=diff, lang=output_lang
    ).strip()

    for i, example in enumerate(examples):
        user_prompt += f"\n\n## Example Output ({i+1})\n\n"
        user_prompt += f"<pr_title>\n{example.title}\n</pr_title>\n\n"
        user_prompt += f"<pr_description>\n{example.description}\n</pr_description>"

    # print(user_prompt)

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
                "content": USER_PROMPT.format(
                    branch_name=current_branch, diff=diff, lang=output_lang
                ),
            },
            {"role": "assistant", "content": "<response><pr_title>"},
        ],
    )

    # --- Make text into xml
    xml_text = "\n".join(
        ["<response><pr_title>"] + [m.text for m in message.content if m.type == "text"]
    ).strip()

    # escape special characters
    xml_text = xml_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # unescape tags
    xml_text = re.sub(
        r"&lt;(/?)(response|pr_title|pr_description|)&gt;", r"<\1\2>", xml_text
    )

    # print(xml_text)

    # --- Parse XML
    try:
        # print("```")
        # print(xml_text)
        # print("```")
        root = ET.fromstring(xml_text)

        if (pr_title := root.find("pr_title")) is not None:
            if text := pr_title.text:
                print(text.strip())
                print()

        if (pr_description := root.find("pr_description")) is not None:
            if text := pr_description.text:
                print(text.strip())
    except ET.ParseError as e:
        click.secho(f"Error parsing XML: {e}", fg="red")
        click.secho(xml_text, fg="red")
