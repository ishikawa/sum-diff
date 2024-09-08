import pytest
from sum_diff.utils import parse_pr_example, PrExample


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
            PrExample(
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
            PrExample(
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
            PrExample(
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
            PrExample(
                title="Title",
                description="""This section contains the description.

## Section A

This section contains the additional information.""",
            ),
        ),
    ],
)
def test_parse_pr_example(markdown: str, expected: PrExample) -> None:
    assert parse_pr_example(markdown) == expected
