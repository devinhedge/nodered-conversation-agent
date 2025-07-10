#!/bin/bash

# Exit on error
set -e

# Update ha-core submodule
echo "Updating ha-core submodule..."
./scripts/update_ha_core.sh

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt
pip install -r requirements_dev.txt

# Install ha-core dependencies
echo "Installing ha-core dependencies..."
pip install --no-deps -r ha-core/requirements.txt
pip install --no-deps -r ha-core/requirements_test.txt

# Install Node-RED
echo "Installing Node-RED..."
npm install -g node-red@3.0.2
npm install -g node-red-contrib-home-assistant-websocket@0.48.0

# Set up pre-commit hooks
echo "Setting up pre-commit hooks..."
pre-commit install

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p config/custom_components

# Create a symlink for the custom component in ha-core
echo "Creating symlink for custom component in ha-core..."
ln -sf "$(pwd)/custom_components/nodered_conversation" "ha-core/homeassistant/components/nodered_conversation"

# Create a symlink for the custom component in config
echo "Creating symlink for custom component in config..."
ln -sf "$(pwd)/custom_components/nodered_conversation" "config/custom_components/nodered_conversation"

echo "Development environment setup complete!"