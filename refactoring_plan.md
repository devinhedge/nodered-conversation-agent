# NodeRed Conversation Agent Refactoring Plan

## 1. Repository and File Structure Changes

### Current File Structure

```text
.
├── .coveragerc
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── README.md
├── requirements.txt
├── TODO.md
└── custom_components/
    └── nodered_conversation/
        ├── __init__.py
        ├── config_flow.py
        ├── const.py
        ├── manifest.json
        ├── requirements.txt
        ├── services.yaml
        ├── strings.json
        └── translations/
            └── en.json
```

### Target File Structure (HACS-compatible with IaC)

```text
.
├── .github/
│   ├── workflows/
│   │   ├── hassfest.yaml
│   │   ├── validate.yaml
│   │   ├── release.yaml
│   │   └── dev.yaml
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       └── feature_request.md
├── custom_components/
│   └── nodered_conversation/
│       ├── __init__.py
│       ├── config_flow.py
│       ├── const.py
│       ├── manifest.json
│       ├── services.yaml
│       ├── strings.json
│       └── translations/
│           └── en.json
├── tests/
│   ├── conftest.py
│   ├── test_init.py
│   └── test_config_flow.py
├── .devcontainer/
│   ├── configuration.yaml
│   ├── Dockerfile
│   └── devcontainer.json
├── .vscode/
│   └── tasks.json
├── scripts/
│   ├── setup_dev_environment.sh
│   └── run_tests.sh
├── .gitignore
├── .pre-commit-config.yaml
├── CHANGELOG.md
├── hacs.json
├── LICENSE
├── README.md
├── requirements.txt
└── requirements_dev.txt
```

### Necessary Changes

1. Create `.github/workflows/` directory with `hassfest.yaml`, `validate.yaml`, and `release.yaml` workflow files.
2. Add `.github/ISSUE_TEMPLATE/` directory with `bug_report.md` and `feature_request.md` templates.
3. Move and expand the `tests/` directory to the root of the project.
4. Create a `.devcontainer/` directory with necessary files for local development setup.
5. Add a `.vscode/` directory with tasks for common development actions.
6. Create a `scripts/` directory for development and testing helper scripts.
7. Create `hacs.json` in the root directory.
8. Create `.pre-commit-config.yaml` in the root directory.
9. Split requirements into `requirements.txt` and `requirements_dev.txt`.
10. Remove `TODO.md` and `.coveragerc` from the root directory.
11. Update `.gitignore` to include HACS-specific and development environment entries.
12. Create `.github/workflows/dev.yaml` for the development workflow.

## 2. Infrastructure as Code (IaC) Implementation

### Local Development Environment

1. Create a `.devcontainer/` directory with:
   - `Dockerfile`: Define the development container image.
   - `devcontainer.json`: Configure VS Code development container settings.
   - `configuration.yaml`: Sample Home Assistant configuration for testing.

2. Add `scripts/setup_dev_environment.sh` to automate the setup of the local development environment.

3. Create `.vscode/tasks.json` to define common development tasks (e.g., running tests, linting).

### GitHub Actions Workflows

1. Implement `.github/workflows/hassfest.yaml` for validating the integration with Home Assistant standards.
2. Implement `.github/workflows/validate.yaml` for HACS validation and additional checks.
3. Keep `.github/workflows/release.yaml` for automating the release process.
4. Implement `.github/workflows/dev.yaml` for the development workflow:
   - Trigger on pushes to the `dev` branch
   - Check code style
   - Perform automated code review
   - Run unit tests
   - Automatically push to `int` branch if tests pass
   - Create issues for code review findings without stopping the build

### Issue Templates

1. Create `.github/ISSUE_TEMPLATE/bug_report.md` for standardized bug reporting.
2. Create `.github/ISSUE_TEMPLATE/feature_request.md` for standardized feature requests.

### Pre-commit Configuration

1. Create `.pre-commit-config.yaml` to define pre-commit hooks for code quality checks.

## 3. Code Refactoring

### __init__.py

1. Remove pylint comments and update import statements to use relative imports.
2. Implement proper error handling and logging throughout the file.
3. Refactor the `NodeRedAgent` class to follow HACS best practices.
4. Implement type hinting consistently throughout the file.

### config_flow.py

1. Review and update the config flow implementation to ensure it follows HACS standards.
2. Implement proper error handling and validation for user inputs.

### const.py

1. Review and update constant definitions to ensure they follow HACS naming conventions.

### manifest.json

1. Update the `version` field to use semantic versioning (e.g., "1.0.0").
2. Add an `issue_tracker` field with the URL to the GitHub issues page.
3. Update the `documentation` field to point to the GitHub repository's README.md.

## 4. HACS Compliance

### hacs.json

Create a new `hacs.json` file in the root directory with the following content:

```json
{
  "name": "NodeRed Conversation",
  "render_readme": true,
  "domains": ["conversation"],
  "homeassistant": "2023.3.0"
}
```

## 5. Documentation

### README.md

1. Update the installation instructions to reflect HACS installation method.
2. Add a badge for HACS default repository status.
3. Include clear usage instructions and examples.
4. Add a "Development" section with instructions for setting up the local development environment.
5. Update the "Contributing" section to include HACS-specific guidelines.

### CHANGELOG.md

1. Ensure the changelog follows the Keep a Changelog format.
2. Add an entry for the HACS compatibility update and infrastructure improvements.

## 6. Testing Plan

1. Expand the existing test suite in the `tests/` directory.
2. Implement unit tests for all major functions and classes.
3. Add integration tests to ensure the component works correctly with Home Assistant.
4. Implement test coverage reporting and aim for at least 90% coverage.
5. Create `scripts/run_tests.sh` to simplify running the full test suite locally.

## 7. Version Control and Release Strategy

1. Update the version number in `manifest.json` to reflect the HACS-compatible release (e.g., "1.0.0").
2. Create a new GitHub release with a tag matching the version number.
3. Include detailed release notes in the GitHub release, referencing the CHANGELOG.md.
4. Implement a Git branching strategy (e.g., GitFlow) for future development.

## 8. Development Workflow

### dev.yaml Workflow

Create a new `.github/workflows/dev.yaml` file with the following functionality:

1. Trigger:
   - On push to the `dev` branch

2. Jobs:
   a. Code Style Check:
      - Use tools like flake8, black, or pylint to check code style
      - Report any style violations

   b. Automated Code Review:
      - Utilize a tool like CodeQL or SonarCloud for automated code review
      - Create GitHub issues for any findings
      - Do not fail the workflow based on review results

   c. Unit Tests:
      - Set up the test environment
      - Run all unit tests
      - Report test results

   d. Push to Integration:
      - If all unit tests pass, automatically push the code to the `int` branch

3. Issue Creation:
   - Implement a step to create GitHub issues for any code style violations or code review findings
   - Use GitHub API or a GitHub Action to create issues

4. Notifications:
   - Set up notifications for workflow success or failure
   - Notify relevant team members of new issues created

This workflow will ensure that all code pushed to the `dev` branch is automatically checked, tested, and integrated, while also creating trackable issues for any findings that need to be addressed.

## Implementation Steps

1. Repository and File Structure Changes
2. Infrastructure as Code Implementation
3. Code Refactoring
4. HACS Compliance
5. Documentation Updates
6. Testing Implementation
7. Version Control and Release Setup
8. Development Workflow Setup
   - Create and configure the dev.yaml workflow
   - Set up necessary secrets and permissions for the workflow
   - Test the workflow to ensure it functions as expected

After completing these steps, including the new development workflow, submit the integration to HACS for review and inclusion in the default repositories.
