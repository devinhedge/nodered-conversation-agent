# Project Setup Instructions

## Updating .gitignore

The `.gitignore` file has been updated to exclude ha-core specific files and include additional Python and testing ignores.

## Initializing and Updating ha-core Submodule

A script named `update_ha_core.sh` has been created in the `./scripts` folder to manage the ha-core submodule. To use it:

1. Make the script executable:
   ```bash
   chmod +x ./scripts/update_ha_core.sh
   ```

2. Run the script to initialize and update the submodule:
   ```bash
   ./scripts/update_ha_core.sh
   ```

Run this script whenever you need to update the ha-core submodule.

## Next Steps

1. Modify the custom component to work within the ha-core structure for testing.
2. Update the development environment setup process.
3. Modify Dockerfile.dev to use ha-core submodule for development and testing.
4. Update .devcontainer/devcontainer.json to reflect the new structure.
