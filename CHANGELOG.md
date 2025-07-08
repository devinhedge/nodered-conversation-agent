# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-07-08

### Added
- Comprehensive error handling and logging throughout the integration
- SSL verification warning when disabled
- Expanded test coverage for NodeRedAgent and config flow

### Changed
- Improved input validation in the config flow
- Enhanced security for handling user credentials
- Removed hardcoded default values
- Updated `manifest.json` to point to README.md for documentation
- Improved code structure and readability

### Fixed
- Addressed potential security vulnerabilities

## [0.0.1] - 2025-07-01

### Added
- Initial release of NodeRed Conversation integration
- Basic functionality for sending conversations to and from Node-RED
- Support for LocalAI and OpenAI providers
- Config flow for easy setup through Home Assistant UI