# Testing Strategy for NodeRed Conversation Agent

## Overview

This document outlines the testing strategy for the NodeRed Conversation Agent custom component for Home Assistant. Our goal is to ensure high-quality, reliable software through comprehensive testing at various levels.

## Testing Levels

### 1. Unit Testing

- **Tool**: Pytest
- **Scope**: Individual functions and methods
- **Location**: `tests/` directory (excluding `integration/`)
- **Key Points**:
  - Test each function in isolation
  - Use mocking to simulate dependencies
  - Aim for high code coverage (>90%)

### 2. Integration Testing

- **Tool**: Pytest with Home Assistant test framework
- **Scope**: Component interactions within Home Assistant
- **Location**: `tests/integration/` directory
- **Key Points**:
  - Test component setup, unload, and reload
  - Verify conversation agent registration
  - Test conversation processing
  - Ensure proper error handling

### 3. API Testing

- **Tool**: Pytest with aiohttp mocking
- **Scope**: NodeRed endpoint interactions
- **Location**: `tests/test_api.py`
- **Key Points**:
  - Test both VoiceAssist and Assist classes
  - Verify correct handling of various API responses
  - Test error conditions and edge cases

### 4. End-to-End Testing (To be implemented)

- **Tool**: To be determined (e.g., Selenium, Cypress)
- **Scope**: Full user interactions through the Home Assistant UI
- **Location**: To be determined
- **Key Points**:
  - Simulate real user interactions
  - Test integration with Home Assistant frontend
  - Verify end-to-end functionality of the conversation agent

## Test Environment

- Use `tests/test_config/configuration.yaml` for a consistent test configuration
- Utilize `scripts/setup_test_config.sh` to set up the test environment within ha-core

## Continuous Integration

- **Tool**: GitHub Actions
- **Location**: `.github/workflows/ci.yml`
- **Key Points**:
  - Run all tests on each push and pull request
  - Enforce code style with flake8, black, and isort
  - Generate and upload test coverage reports

## Coverage Goals

- Aim for at least 90% code coverage
- Use `.coveragerc` to configure coverage settings
- Regularly review and improve test coverage

## Best Practices

1. Write tests before or alongside feature development (TDD/BDD approach)
2. Keep tests independent and idempotent
3. Use descriptive test names that explain the expected behavior
4. Regularly update tests as the codebase evolves
5. Use parameterized tests for testing multiple scenarios efficiently

## Maintenance

- Review and update this testing strategy regularly
- Adjust testing approaches based on project needs and new best practices
- Encourage all contributors to write and maintain tests for their code
