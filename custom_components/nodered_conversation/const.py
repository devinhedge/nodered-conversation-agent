"""Constants for the NodeRed Conversation integration."""

DOMAIN = "nodered_conversation"
NAME = "NodeRed Conversation"
VERSION = "0.1.0"

CONF_NODERED_URL = "nodered_url"
CONF_NODERED_USER = "nodered_user"
CONF_NODERED_PASS = "nodered_pass"

DEFAULT_NODERED_URL = "https://noderedip:1880/endpoint/gpt"

# Service constants
SERVICE_PROCESS_CONVERSATION = "process_conversation"
ATTR_MESSAGE = "message"

# Error messages
ERROR_CANNOT_CONNECT = "cannot_connect"
ERROR_INVALID_AUTH = "invalid_auth"
ERROR_UNKNOWN = "unknown"
ERROR_INVALID_URL = "invalid_url"