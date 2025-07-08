#!/bin/zsh

# Set the output directory
OUTPUT_DIR="$(dirname "$0")"

# URL of the HACS documentation repository
REPO_URL="https://github.com/hacs/documentation.git"

# Create a temporary directory for cloning
TEMP_DIR=$(mktemp -d)

echo "Updating HACS documentation in $OUTPUT_DIR"

# Clone the repository
git clone --depth 1 $REPO_URL $TEMP_DIR

# Copy the relevant documentation files
cp -R $TEMP_DIR/source/docs/* $OUTPUT_DIR

# Clean up
rm -rf $TEMP_DIR

echo "Documentation update complete."