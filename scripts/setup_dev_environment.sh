#!/bin/bash

# Exit on error
set -e

# Function to log messages
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Function to handle errors
handle_error() {
    log "Error occurred in line $1"
    exit 1
}

# Set up error handling
trap 'handle_error $LINENO' ERR

log "Starting development environment setup..."

# Update ha-core submodule
log "Updating ha-core submodule..."
./scripts/update_ha_core.sh

# Create and activate virtual environment
log "Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install ha-core dependencies first
log "Installing ha-core dependencies..."
pip install --verbose -r ha-core/requirements.txt
pip install --verbose -r ha-core/requirements_test.txt

# Install project dependencies
log "Installing project dependencies..."
pip install --verbose -r requirements.txt
pip install --verbose -r requirements_dev.txt

# Install Node-RED
log "Installing Node-RED..."
npm install -g node-red@3.0.2
npm install -g node-red-contrib-home-assistant-websocket@0.48.0

# Set up pre-commit hooks
log "Setting up pre-commit hooks..."
pre-commit install

# Create necessary directories
log "Creating necessary directories..."
mkdir -p config/custom_components

# Create a symlink for the custom component in ha-core
log "Creating symlink for custom component in ha-core..."
ln -sf "$(pwd)/custom_components/nodered_conversation" "ha-core/homeassistant/components/nodered_conversation"

# Create a symlink for the custom component in config
log "Creating symlink for custom component in config..."
ln -sf "$(pwd)/custom_components/nodered_conversation" "config/custom_components/nodered_conversation"

log "Development environment setup complete!"