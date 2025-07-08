# NodeRed Conversation

## Introduction

This is a complete fork and refactor of the initial work of @roblandry with his [Node-RED Conversation Custom Component](https://github.com/roblandry/nodered_conversation).

This HACS Integration for Home Assistant creates a NodeRed Conversation Agent (modified from OpenAI conversation agent). This integration sends conversations to and from Node-RED to be used with LocalAI, any OpenAI v1 API endpoint, n8n, or OpenRouter.

## Status

This integration is now in a more stable beta version with significant improvements in security, error handling, and code quality. While it's more robust, it's still subject to changes. Contributions to improve and enhance the integration are welcome!

## Installation

### HACS Installation (Recommended)

1. Ensure that [HACS](https://hacs.xyz/) is installed in your Home Assistant instance.
2. In the HACS panel, go to "Integrations" and click the "+" button.
3. Search for "NodeRed Conversation" and select it.
4. Click "Install" and wait for the installation to complete.
5. Restart Home Assistant.

### Manual Installation

If you prefer to install manually:

1. Clone this repository or download the custom component files.
2. Place the `custom_components/nodered_conversation` directory in your Home Assistant `custom_components` folder.
3. Restart Home Assistant.

## Configuration

1. Add the NodeRed Conversation integration through the Home Assistant UI:
   - Navigate to Configuration > Integrations > Add Integration
   - Search for "NodeRed Conversation" and select it
   - Enter the URL for your Node-RED instance (e.g., `https://192.168.1.1:1880/endpoint/gpt`)
   - Provide a username and password for authentication with the Node-RED flow
2. Select the new Conversation agent:
   - Go to Settings > Voice Assistants > Home Assistant > Conversation agent
   - Choose "NodeRed Conversation" from the list
3. Import the `nodered_sample_flow.json` into your Node-RED instance.
4. Update the authentication node in the Node-RED flow with the username and password you set in step 1.

### Configuration for AI Providers

- **For OpenAI:** (not tested)
  - Enter your API key for OpenAI
  - Remove the line for the URL in the Node-RED flow
- **For LocalAI:**
  - The API key doesn't matter, but you need to add the URL or IP address of your LocalAI server

## Usage

Once installed and configured, you can use the NodeRed Conversation agent in various ways:

1. Through the Home Assistant UI:
   - Go to Developer Tools > Conversation
   - Type your message and send it

2. Via voice commands if you have voice assistants configured

3. Through service calls in automations or scripts:

   ```yaml
   service: conversation.process
   data:
     text: "Your message here"
   ```

4. Using the Conversation integration in Lovelace cards

## Development

First setup of a proper Home Assistant Development Environment based on [the Home Assistant way](https://developers.home-assistant.io/docs/development_environment).

TODO: Fill this in.

### Running tests

To run the tests, use the following command:

```bash
pytest tests
```

For tests with coverage reporting:

```bash
pytest tests -v --cov=custom_components.nodered_conversation --cov-report=term-missing --cov-report=html
```

```bash
pytest tests -v --cov=custom_components.nodered_conversation --cov-report=term-missing --cov-report=html
```

This will run the tests, display a coverage report in the terminal, and generate an HTML coverage report in the `htmlcov` directory.

To view the HTML coverage report, open the `htmlcov/index.html` file in your web browser.

## Recent Changes

- Enhanced error handling and logging throughout the integration
- Improved input validation in the config flow
- Implemented secure handling of user credentials
- Added SSL verification warning when disabled
- Improved code structure and readability
- Removed hardcoded default values
- Updated the `manifest.json` file to point to this README for documentation
- Expanded test coverage for NodeRedAgent and config flow
- Improved installation and development instructions in this README
- Added HACS installation instructions

## Offline Reference Documentation for AI Agents

This project includes an offline copy of the HACS documentation for reference, primarily intended for AI Agents to use while coding. You can find it in the `docs/x-reference/` directory.

### Updating the Offline Documentation

To keep the offline documentation up-to-date, use the provided zsh script:

```bash
./docs/x-reference/update_docs.zsh
```

This script clones the latest HACS documentation from the official GitHub repository and updates the local copy in the `docs/x-reference/` directory.

## Contributing

Contributions are welcome! If you'd like to help improve this integration, please fork the repository and submit a pull request with your changes. Be sure to follow the existing code style, add tests for new functionality, and update documentation as necessary.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
