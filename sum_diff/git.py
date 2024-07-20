import re
import subprocess


def git_current_branch() -> str:
    """
    Get the name of the current Git branch.
    """
    return (
        subprocess.check_output("git rev-parse --abbrev-ref HEAD", shell=True)
        .decode("utf-8")
        .strip()
    )


# Borrowed from https://stackoverflow.com/a/17843908
def git_parent_branch(current_branch: str) -> str | None:
    """
    Find the nearest parent of a Git branch and return its name.
    """
    # Get a textual history of all commits, including remote branches.
    history = (
        subprocess.check_output("git show-branch -a", shell=True)
        .decode("utf-8")
        .strip()
    )

    # Ancestors of the current commit are indicated by a star. Filter out everything else.
    ancestors = [line for line in history.split("\n") if "*" in line]

    # Ignore all the commits in the current branch.
    ancestors = [line for line in ancestors if current_branch not in line]

    if not ancestors:
        return None

    # The first result will be the nearest ancestor branch. Ignore the other results.
    parent_branch_line = ancestors[0]

    # Branch names are displayed [in brackets]. Ignore everything outside the brackets, and the brackets.
    r = re.compile(r"\[(.*?)\]")
    m = r.findall(parent_branch_line)

    if not m:
        return None

    # Sometimes the branch name will include a ~# or ^# to indicate how many commits are between the
    # referenced commit and the branch tip. We don't care. Ignore them.
    branch_name = m[0].replace("~#", "").replace("^#", "")

    return branch_name


MAX_DIFF_LENGTH = 3000


def git_diff_from_parent(parent_branch: str | None) -> str:
    """
    Get the diff of the current branch from its parent branch.
    """
    # Collect files changed between the current branch and its parent.
    command = "git diff --name-only"
    if parent_branch:
        command += f" {parent_branch}.."

    r = subprocess.check_output(command, shell=True, text=True)
    files = r.split("\n")

    # Collect the diff of each file changed and concatenate them.
    diff = ""
    for file in files:
        command = "git diff"
        if parent_branch:
            command += f" {parent_branch}.."
        command += f" -- {file}"

        r = subprocess.check_output(command, shell=True, text=True)
        if len(r) > MAX_DIFF_LENGTH:
            r = r[:MAX_DIFF_LENGTH]
        diff += r

    return diff
