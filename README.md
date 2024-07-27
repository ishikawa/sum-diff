# sum-diff

> Summarize your changes into a concise title and a detailed description.

`sum-diff` is a simple command-line tool that automatically generates a concise title and a detailed description by analyzing the current git branch, including:

- Branch name
- Code changes (`git diff`)

## Installation

Install using `pipx`:

```bash
# Download and unzip
$ unzip sum-diff.zip
$ pipx install ./sum-diff

# Install nightly from GitHub
$ pipx install git+https://github.com/ishikawa/sum-diff
```

## API Key

`sum-diff` uses Anthropic's Claude 3.5 Sonnet to generate the output. Obtain an API key from [Anthropic's console](https://console.anthropic.com/) and set it as an environment variable:

```bash
$ export ANTHROPIC_API_KEY=sk-ant-...
```

## Usage

After making changes to your project and before creating a PR, run the `sum-diff` command to have the AI generate a title and description for your PR.

```bash
$ sum-diff
```

The command will take a few seconds to process and then output the title and description. For example:

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
