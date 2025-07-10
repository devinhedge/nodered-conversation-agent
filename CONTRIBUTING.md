# Contributing to NodeRed Conversation Agent

We welcome contributions to the NodeRed Conversation Agent project! This document provides guidelines for contributing to the project.

## Table of Contents
- [Contributing to NodeRed Conversation Agent](#contributing-to-nodered-conversation-agent)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
  - [Development Environment Setup](#development-environment-setup)
  - [Coding Standards](#coding-standards)
  - [Testing](#testing)
  - [Submitting Changes](#submitting-changes)
  - [Updating Documentation](#updating-documentation)
  - [Questions or Need Help?](#questions-or-need-help)

## Getting Started

1. Fork the repository on GitHub.
2. Clone your fork locally:
   ```
   git clone https://github.com/your-username/nodered-conversation-agent.git
   cd nodered-conversation-agent
   ```

## Development Environment Setup

1. Initialize and update the ha-core submodule:
   ```
   ./scripts/update_ha_core.sh
   ```

2. Set up the development environment:
   ```
   ./scripts/setup_dev_environment.sh
   ```

3. Install development dependencies:
   ```
   pip install -r requirements_dev.txt
   ```

## Coding Standards

- Follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code.
- Use type hints for function arguments and return values.
- Write docstrings for all public functions, classes, and modules.
- Use meaningful variable and function names.
- Keep functions small and focused on a single task.

## Testing

We use pytest for testing. Please ensure that your contributions include appropriate tests and maintain or improve our overall test coverage.

1. Run the full test suite:
   ```
   pytest tests
   ```

2. Run tests with coverage:
   ```
   pytest tests -v --cov=custom_components.nodered_conversation --cov-report=term-missing --cov-report=html
   ```

3. Ensure that your changes don't decrease the overall test coverage. We aim for at least 90% coverage.

4. For more details on our testing strategy, refer to the [Testing Strategy](docs/testing_strategy.md) document.

## Submitting Changes

1. Create a new branch for your feature or bug fix:
   ```
   git checkout -b feature/your-feature-name
   ```

2. Make your changes, following the coding standards described above.

3. Commit your changes:
   ```
   git commit -m "Add a descriptive commit message"
   ```

4. Push to your fork:
   ```
   git push origin feature/your-feature-name
   ```

5. Create a pull request from your fork to the main repository.

6. In your pull request description, explain the changes you've made and any additional context that might be helpful for reviewers.

## Updating Documentation

If your changes affect how users interact with the project, update the relevant documentation:

1. Update the README.md if necessary.
2. Update or add to the documentation in the `docs/` directory.
3. If you've added new features, consider adding usage examples.

## Questions or Need Help?

If you have any questions or need help with the contribution process, please open an issue on GitHub, and we'll be happy to assist you.

Thank you for contributing to the NodeRed Conversation Agent project!