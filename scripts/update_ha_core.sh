#!/bin/bash

# Initialize the submodule if it hasn't been initialized yet
git submodule init

# Update the submodule to the latest commit on the tracked branch
git submodule update --remote --merge

echo "ha-core submodule updated successfully"