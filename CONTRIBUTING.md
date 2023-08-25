# Contributing to Spycular

Thank you for your interest in contributing to Spycular! We value the work of our community and believe that every contribution, no matter how small, enhances the quality and functionality of the project. This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
  - [Setting Up Your Environment](#setting-up-your-environment)
  - [Finding Issues to Work On](#finding-issues-to-work-on)
- [Making a Contribution](#making-a-contribution)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Code Contributions](#code-contributions)
    - [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Community](#community)
- [Acknowledgments](#acknowledgments)

## Code of Conduct

This project adheres to a code of conduct. Please review our [Code of Conduct](CODE_OF_CONDUCT.md) to ensure you follow it while participating.

## Getting Started

### Setting Up Your Environment

1. Fork the repository on GitHub.
2. Clone your fork: `git clone https://github.com/IonesioJunior/Spycular.git`
3. Navigate to the project directory: `cd Spycular`
4. [Any other specific setup instructions.]

### Finding Issues to Work On

If you're new to the project, you might want to start by picking up "good first issues" or "help wanted" tags.

## Making a Contribution

### Reporting Bugs

- Ensure the bug hasn't already been reported by searching the issues.
- If you're unable to find an open issue, [open a new one](https://github.com/IonesioJunior/Spycular/issues/new). Be sure to include a title, clear description, as much relevant information as possible, and a code sample or steps to reproduce the issue.

### Suggesting Enhancements

If you have ideas for improvements or new features, we'd love to hear! Please create an issue describing your suggestion.

### Code Contributions

Once you've identified an issue you'd like to work on:

1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Make your changes.
3. Push the branch to your fork: `git push origin feature/your-feature-name`
4. Submit a Pull Request to the main repository.

#### Pull Request Process

1. Ensure your PR has a descriptive title and detailed description.
2. Link the PR to the issue it resolves (if applicable).
3. Make sure all CI checks pass.
4. Await review. Address any requested changes.
5. Once approved, the maintainer will merge it.

## Style Guidelines

At Spycular, we aim to maintain a consistent and clean codebase. To achieve this, we adhere to certain style conventions and best practices. Below are our guidelines for code contributions:

### General Code Style

1. **Consistency:** Above all, aim for consistency with the existing codebase. When in doubt, see how existing code handles the situation.
2. **Descriptive Naming:** Choose variable, function, and class names that accurately describe their purpose or functionality.

### Python-specific Guidelines

1. **PEP 8:** Adhere to [PEP 8](https://www.python.org/dev/peps/pep-0008/), the style guide for Python code, with the exceptions noted below.
2. **Line Length:** Aim for a maximum line length of 88 characters, which is the default for tools like [Black](https://black.readthedocs.io/en/stable/).
3. **Imports:**
   - Group imports in the following order: standard library, third-party libraries, local/source imports.
   - Use absolute imports over relative ones.
4. **Docstrings:** Use [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#383-functions-and-methods) to document functions, methods, and classes. Ensure public APIs have clear and comprehensive documentation.
5. **Comments:** Comments should be used sparingly, i.e., only when necessary to explain complex pieces of code, decisions that could seem not obvious to other developers, etc. Avoid obvious comments.
6. **Type Annotations:** Use [PEP 484](https://www.python.org/dev/peps/pep-0484/) type hints in function signatures. This helps in static type checking and understanding the expected function inputs and outputs.

### Formatting

1. **Automatic Formatting:** Use [Black](https://black.readthedocs.io/en/stable/) for automatic code formatting. Ensure your code is `Black`ened before submitting.
2. **Linting:** Use tools like [Flake8](https://flake8.pycqa.org/en/latest/) to catch logical errors, undefined variables, or style discrepancies. Resolve all warnings before submitting.

### Testing

1. **Write Tests:** Always accompany your code with tests. We use [pytest](https://docs.pytest.org/en/latest/) for our testing framework.
2. **Coverage:** Aim for 100% test coverage, but it's okay if your PR doesn't achieve this. However, ensure you test critical paths and edge cases.

### Commit Messages

1. **Descriptive Commit Messages:** Write concise yet descriptive commit messages. Start with a verb in the imperative mood, e.g., "Add", "Fix", "Update".
2. **Issue Numbers in Commit:** If your commit pertains to an open issue, please reference the issue number in the commit message.

---

Remember, while these guidelines provide a foundation for contributions, they aren't exhaustive. Always prioritize clarity and simplicity in your code. If you have questions or are unsure about a specific style decision, feel free to ask in the corresponding pull request or issue.

Thank you for helping improve Spycular!
