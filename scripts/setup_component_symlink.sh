#!/bin/bash

# Ensure the ha-core submodule is up to date
./scripts/update_ha_core.sh

# Create the symlink
mkdir -p ./ha-core/homeassistant/components/nodered_conversation
ln -sf $(pwd)/custom_components/nodered_conversation ./ha-core/homeassistant/components/nodered_conversation

echo "Symlink for nodered_conversation component created successfully"