from dataclasses import dataclass
import re


@dataclass
class PrExample:
    title: str
    description: str


def parse_pr_example(markdown: str) -> PrExample:
    """
    Parses a PR example from a Markdown-formatted string.

    - Removes html comments like <!-- comment -->
    - Splits the h1 title and the remaining content
    - Removes leading and trailing whitespace from the title and description
    """
    # Remove html comments
    markdown = re.sub(r"<!--.*?-->", "", markdown, flags=re.DOTALL)

    # Split the title and description.
    #
    # The title is the first line which starts with `# `
    # The description is everything after the title
    title = ""
    lines: list[str] = []
    for line in markdown.splitlines():
        if line.startswith("# ") and not title:
            title = line
        else:
            lines.append(line)

    description = "\n".join(lines)

    # Remove leading `#` from the title
    title = re.sub(r"^#+\s*", "", title)

    # Remove leading and trailing whitespace from the title and description
    return PrExample(title.strip(), description.strip())
