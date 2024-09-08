import pytest
from sum_diff.utils import parse_pr_example, PRExample


@pytest.mark.parametrize(
    "markdown, expected",
    [
        # single line comment
        (
            """
<!-- This is a comment -->
# Title

This section contains the description.
""",
            PRExample(
                title="Title", description="This section contains the description."
            ),
        ),
        # multiline comment
        (
            """
<!--
    This is a comment
-->
# Title

This section contains the description.
""",
            PRExample(
                title="Title", description="This section contains the description."
            ),
        ),
        # multiple comments
        (
            """
<!--
    This is a comment
-->
<!--
    This is another comment
-->
# Title

This section contains the description.
""",
            PRExample(
                title="Title", description="This section contains the description."
            ),
        ),
        # multiple headings
        (
            """
# Title

This section contains the description.

## Section A

This section contains the additional information.

""",
            PRExample(
                title="Title",
                description="""This section contains the description.

## Section A

This section contains the additional information.""",
            ),
        ),
    ],
)
def test_parse_pr_example(markdown: str, expected: PRExample) -> None:
    assert parse_pr_example(markdown) == expected
