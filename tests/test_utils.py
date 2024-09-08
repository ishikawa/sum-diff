from sum_diff.utils import parse_pr_example, PRExample


def test_parse_pr_example():
    markdown = """
<!-- This is a comment -->
# Title

This section contains the description.
"""
    expected = PRExample(
        title="Title", description="This section contains the description."
    )

    assert parse_pr_example(markdown) == expected
