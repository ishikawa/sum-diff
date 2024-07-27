# sum-diff

> Summarize your changes into a concise title and a detailed description.

In this project, we provide a simple command called `sum-diff`. This command automatically generates a concise and clear title and a detailed description from the current branch's differences in a git repository.

## Install

Using `pipx`.

```bash
# download zip
$ unzip sum-diff.zip
$ pipx ./sum-diff

# nightly from GitHub
pipx install git+https://github.com/ishikawa/sum-diff
```

## API key

`sum-diff` uses Anthropic's Claude 3.5 Sonnet to generate output. You need to get API key from [their console](https://console.anthropic.com/) and exporting it via `ANTHROPIC_API_KEY` environment variable.

```bash
$ export ANTHROPIC_API_KEY=sk-ant-...
```

## How to use

After you made some changes in your project and before you're going to create a PR for these changes, run `sum-diff` command to let AI to write title and description of the PR.

```bash
$ sum-diff
```

It takes some seconds, then, prints title and description in standard output. For example:

````
Add `while` statement support to compiler

This PR introduces support for `while` loops in the compiler, enhancing the language's control flow capabilities.

Key changes:
- Add `While` token and parsing logic in `tokenizer.rs`
- Implement `WhileStmt` struct and parsing in `parser.rs`
- Add code generation for `while` loops in `asm.rs`
- Update `LocalVarAllocator` to handle `while` statements in `allocator.rs`
- Add test cases for `while` loops in `test.sh`

The implementation follows the existing pattern for control flow statements, such as `if` statements. The `while` loop consists of a condition and a body, which are evaluated and executed accordingly.

Example of the new `while` loop syntax:

```rust
i = 0;
while (i < 20)
  i = i + 1;
return i;
```

This PR completes the basic control flow structures for the compiler, allowing for more complex program logic to be expressed in the language.
````
