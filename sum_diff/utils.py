from dataclasses import dataclass
import re


@dataclass
class PRExample:
    title: str
    description: str


def parse_pr_example(markdown: str) -> PRExample:
    """
    Parses a PR example from a Markdown-formatted string.

    - Removes html comments like <!-- comment -->
    - Splits the h1 title and the remaining content
    - Removes leading and trailing whitespace from the title and description
    """
    # Remove html comments
    markdown = re.sub(r"<!--.*?-->", "", markdown, flags=re.DOTALL)

    # Split the title and description
    title, description = re.split(r"\n+", markdown.strip(), maxsplit=1)

    # Remove leading `#` from the title
    title = re.sub(r"^#+\s*", "", title)

    # Remove leading and trailing whitespace from the title and description
    return PRExample(title.strip(), description.strip())
