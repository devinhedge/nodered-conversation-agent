# All of the outstanding tasks for the nodered conversation integration

## Dev Container Configuration Plan

- [ ] Review and update .devcontainer/devcontainer.json file
  - [ ] Update "image" field to use "ghcr.io/home-assistant/devcontainer:stable"
  - [ ] Remove "dockerFile" and "context" fields
  - [ ] Update "postCreateCommand" to include necessary setup steps
    ```json
    "postCreateCommand": "pip install -r requirements.txt -r requirements_dev.txt && mkdir -p /config/custom_components/nodered_conversation && cp -r /workspaces/nodered-conversation-agent/custom_components/nodered_conversation/* /config/custom_components/nodered_conversation/"
    ```
  - [ ] Verify and update VS Code extensions and settings (current settings seem correct)
- [ ] Update .devcontainer/Dockerfile
  - [ ] Remove existing Dockerfile content
  - [ ] Add a comment explaining that we're using a pre-built image instead
- [ ] Verify and update dependencies
  - [ ] Review requirements.txt and requirements_dev.txt files
  - [ ] Update postCreateCommand in devcontainer.json to install dependencies
- [ ] Review and update .devcontainer/configuration.yaml if necessary
  - [ ] Ensure it includes minimal configuration for development
  - [ ] Verify HACS configuration
- [ ] Update .gitignore file
  - [ ] Add entries to exclude unnecessary files and directories
- [ ] Test the updated dev container configuration
  - [ ] Rebuild and start the dev container
  - [ ] Verify that Home Assistant starts correctly
  - [ ] Test basic functionality
- [ ] Document the changes
  - [ ] Update README.md with new setup instructions
  - [ ] Add a section about the development environment

Here's a detailed plan to accomplish our task:

## From the [initial repository](https://github.com/roblandry/nodered_conversation)

- [ ] Implement red coloring for error messages
- [ ] Further improve Config Flow/Options functionality
- [ ] Expand test coverage
- [ ] Add support for additional AI providers

Update Repository Structure:

- [ ] Ensure the integration is in the correct directory (custom_components/nodered_conversation)

  - [ ] Verify the current directory structure:

    - [ ] Confirm that all necessary files are present in the custom_components/nodered_conversation/ directory
    - [ ] Check for any misplaced files or directories

  - [ ] Document the current directory structure"

    - [ ] Create or update documentation to reflect the correct file locations
    - [ ] Include a directory tree in the documentation for easy reference

  - [ ] Implement a directory structure validation check:

    - [ ] Create a script or test that verifies the correct directory structure
    - [ ] Include this check in the project's CI/CD pipeline

  - [ ] Review and update related configuration files:

    - [ ] Ensure that any references to the integration's location in configuration files are correct
    - [ ] Update the HACS configuration file (if applicable) to reflect the correct directory structure

  - [ ] Create a guide for contributors:

    - [ ] Develop guidelines for maintaining the correct directory structure
    - [ ] Include this information in the project's contributing documentation

- [ ] Verify that the directory name matches the integration domain (nodered_conversation)

Update manifest.json:

- [ ] Add "requirements" field (if any external libraries are needed)
- [ ] Update "documentation" URL to point to the correct documentation
- [ ] Ensure "version" follows semantic versioning (e.g., "1.0.0" instead of "0.0.1")

Create info.md:

- [ ] Create an info.md file in the root directory
- [ ] Include a brief description of the integration
- [ ] Add any specific setup instructions or configuration options

Create hacs.json:

- [ ] Create a hacs.json file in the root directory
- [ ] Include relevant HACS-specific configuration options

Update README.md:

- [ ] Improve installation instructions
- [ ] Add a section about HACS installation
- [ ] Include more detailed usage instructions
- [ ] Add a section about configuration options

Implement Error Handling and Logging:

- [ ] Review existing error handling in init.py and other files
- [ ] Implement consistent error handling across all functions
- [ ] Add appropriate logging statements (DEBUG, INFO, WARNING, ERROR)
- [ ] Create a custom logger for the integration

Create Tests:

- [ ] Develop unit tests for the integration
- [ ] Ensure tests cover error handling and logging scenarios

Update Version Control:

- [ ] Set up GitHub releases for versioning
- [ ] Create a CHANGELOG.md file to track changes
