# Converting Node-RED Conversation Agent to HACS Integration

This comprehensive guide walks you through converting the Node-RED Conversation Agent custom component into a HACS (Home Assistant Community Store) integration.

## Overview

The Home Assistant Community Store (HACS) is a custom integration that provides a UI to manage custom elements in Home Assistant. Converting your custom component to be HACS-compatible makes it easier for users to install, update, and manage your integration.

## Prerequisites

- Existing Home Assistant custom component (Node-RED Conversation Agent)
- GitHub repository with public access
- GitHub account for authentication
- Basic knowledge of YAML and JSON file formats

## Step-by-Step Conversion Process

### Step 1: Verify Repository Structure

Ensure your repository follows the correct structure for HACS integrations:

```text
ROOT_OF_THE_REPO/
├── custom_components/
│   └── nodered_conversation/
│       ├── __init__.py
│       ├── manifest.json
│       ├── config_flow.py (recommended)
│       └── [other integration files]
├── hacs.json (NEW - required for HACS)
├── README.md (required)
├── info.md (optional)
└── .github/
    └── workflows/
        ├── validate.yml (recommended)
        └── hassfest.yml (recommended)
```

**Key Requirements:**

- Only one integration per repository
- Integration files must be in `custom_components/{domain}/`
- Repository must be public on GitHub

### Step 2: Create hacs.json File

Create a `hacs.json` file in the root of your repository:

```json
{
  "name": "Node-RED Conversation Agent",
  "content_in_root": false,
  "zip_release": false,
  "hide_default_branch": false,
  "homeassistant": "2023.8.0",
  "domains": ["conversation"],
  "country": [],
  "render_readme": false
}
```

**Key Fields Explained:**

- `name`: Display name in HACS UI
- `homeassistant`: Minimum Home Assistant version required
- `domains`: List of Home Assistant domains this integration provides
- `render_readme`: Set to true if you don't have info.md

### Step 3: Update manifest.json

Ensure your `custom_components/nodered_conversation/manifest.json` includes all required fields:

```json
{
  "domain": "nodered_conversation",
  "name": "Node-RED Conversation Agent",
  "version": "1.0.0",
  "documentation": "https://github.com/devinhedge/nodered-conversation-agent",
  "issue_tracker": "https://github.com/devinhedge/nodered-conversation-agent/issues",
  "dependencies": [],
  "codeowners": ["@devinhedge"],
  "config_flow": true,
  "iot_class": "local_push",
  "integration_type": "service"
}
```

**Required Fields for HACS:**

- `domain`: Must match directory name
- `name`: Human-readable integration name
- `version`: Semantic version (required for custom components)
- `documentation`: Link to integration documentation
- `issue_tracker`: Link to GitHub issues page
- `codeowners`: GitHub usernames responsible for the code

### Step 4: Add GitHub Repository Metadata

#### Repository Description

Add a clear, concise description to your GitHub repository that explains the integration's purpose.

#### Repository Topics

Add relevant topics to your GitHub repository for better discoverability:

- `home-assistant`
- `custom-component`
- `node-red`
- `conversation-agent`
- `hacs`

### Step 5: Create GitHub Workflows (Recommended)

#### HACS Validation Workflow

Create `.github/workflows/validate.yml`:

```yaml
name: Validate

on:
  push:
  pull_request:
  schedule:
    - cron: "0 0 * * *"

jobs:
  validate:
    runs-on: "ubuntu-latest"
    steps:
      - uses: "actions/checkout@v3"
      - name: HACS validation
        uses: "hacs/action@main"
        with:
          category: "integration"
```

#### Hassfest Validation Workflow

Create `.github/workflows/hassfest.yml`:

```yaml
name: Hassfest

on:
  push:
  pull_request:
  schedule:
    - cron: "0 0 * * *"

jobs:
  validate:
    runs-on: "ubuntu-latest"
    steps:
      - name: "Checkout the repository"
        uses: "actions/checkout@v3"
      - name: "Run hassfest validation"
        uses: "home-assistant/actions/hassfest@master"
```

### Step 6: Improve Documentation

#### Update README.md

Ensure your README includes:

- Clear installation instructions for both HACS and manual installation
- Configuration examples
- Troubleshooting information
- Node-RED flow setup instructions

#### Create info.md (Optional)

For a richer HACS experience, create an `info.md` file with:

- Detailed feature descriptions
- Screenshots or examples
- Configuration options
- Links to related resources

### Step 7: Add Home Assistant Brands (Required for UI Integration)

Submit branding assets to the Home Assistant Brands repository:

1. Fork the [home-assistant/brands](https://github.com/home-assistant/brands) repository
2. Create a folder: `custom_integrations/nodered_conversation/`
3. Add required assets:
   - `icon.png`: 128x128px square icon
   - `logo.png`: Landscape logo respecting brand aspect ratio

### Step 8: Create GitHub Releases (Recommended)

Create tagged releases for better version management:

1. Use semantic versioning (e.g., v1.0.0, v1.1.0)
2. Include release notes describing changes
3. HACS will present users with version selection options

### Step 9: Test as Custom Repository

Before official submission, test your integration:

1. In HACS, click the "..." menu → "Custom repositories"
2. Add your repository URL
3. Select "Integration" as the type
4. Test installation and functionality

### Step 10: Submit to HACS Default Repositories (Optional)

For inclusion in HACS default repositories:

1. Ensure all validation workflows pass
2. Create a pull request to [hacs/default](https://github.com/hacs/default)
3. Add your repository to the appropriate integration file
4. Follow the submission guidelines

## Common Issues and Solutions

### Repository Structure Not Compliant

- Ensure `custom_components/{domain}/` structure is correct
- Check that `hacs.json` exists in repository root
- Verify `manifest.json` contains all required fields

### Validation Failures

- Run HACS validation locally before pushing
- Check Home Assistant version compatibility
- Ensure all required fields are present in manifest

### Missing Dependencies

- List all Python package requirements in `manifest.json`
- Test with fresh Home Assistant installation
- Document any external service dependencies

## Best Practices

### Code Quality

- Follow Home Assistant coding standards
- Add type hints where possible
- Include proper error handling
- Add logging for debugging

### User Experience

- Implement config flow for UI-based setup
- Provide clear error messages
- Include comprehensive documentation
- Add translations for different languages

### Maintenance

- Keep dependencies up to date
- Test with latest Home Assistant versions
- Respond to user issues promptly
- Follow semantic versioning for releases

## Additional Resources

- [HACS Documentation](https://hacs.xyz/docs/)
- [Home Assistant Developer Docs](https://developers.home-assistant.io/)
- [Integration Blueprint Template](https://github.com/ludeeus/integration_blueprint)
- [Home Assistant Brands Repository](https://github.com/home-assistant/brands)
- [HACS Default Repositories](https://github.com/hacs/default)

## Conclusion

Converting your Node-RED Conversation Agent to a HACS integration involves several steps, but the result is a much better user experience. Users can easily discover, install, and update your integration through the HACS interface, leading to wider adoption and easier maintenance.

Remember to test thoroughly and follow Home Assistant community guidelines throughout the process. The investment in making your integration HACS-compatible will pay off in terms of user satisfaction and community adoption.
