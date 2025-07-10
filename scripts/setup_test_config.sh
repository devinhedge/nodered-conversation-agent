#!/bin/bash

# Script to set up test configuration for nodered_conversation component

# Ensure we're in the project root
cd "$(dirname "$0")/.." || exit

# Create test config directory in ha-core if it doesn't exist
mkdir -p ha-core/tests/test_config

# Copy test configuration file
cp tests/test_config/configuration.yaml ha-core/tests/test_config/

# Copy custom component to ha-core custom_components directory
mkdir -p ha-core/homeassistant/components/nodered_conversation
cp -r custom_components/nodered_conversation/* ha-core/homeassistant/components/nodered_conversation/

echo "Test configuration and custom component copied to ha-core test environment."