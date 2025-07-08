#!/bin/bash

# Exit on error
set -e

# Install dependencies
pip install -r requirements.txt
pip install -r requirements_dev.txt

# Set up pre-commit hooks
pre-commit install

# Create necessary directories
mkdir -p config/custom_components

# Create a symlink for the custom component
ln -s "$(pwd)/custom_components/nodered_conversation" "config/custom_components/nodered_conversation"

echo "Development environment setup complete!"