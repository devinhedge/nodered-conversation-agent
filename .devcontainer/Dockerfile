# Use the official Home Assistant development container as a base
FROM ghcr.io/home-assistant/devcontainer:latest

# Install any additional dependencies
RUN pip3 install --no-cache-dir pytest pytest-cov flake8 mypy

# Set the working directory
WORKDIR /workspaces/nodered-conversation-agent

# Clone the HACS repository
RUN git clone -b main --single-branch --depth 1 https://github.com/hacs/integration /workspaces/hacs

# Install HACS
RUN mkdir -p /config/custom_components/hacs && \
    cp -r /workspaces/hacs/custom_components/hacs /config/custom_components/

# Set up the command to run when the container starts
CMD ["python3", "-m", "homeassistant", "--config", "/config"]