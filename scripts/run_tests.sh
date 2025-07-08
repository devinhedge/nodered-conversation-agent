#!/bin/bash

# Exit on error
set -e

# Run pytest with coverage
pytest tests -v --cov=custom_components.nodered_conversation --cov-report=term-missing

# Run flake8
flake8 custom_components tests

# Run mypy
mypy custom_components

echo "All tests and checks completed successfully!"