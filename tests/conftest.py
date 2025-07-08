"""Global fixtures for NodeRed Conversation integration tests."""
from unittest.mock import patch

import pytest

pytest_plugins = "pytest_homeassistant_custom_component"

# This fixture is used to prevent HomeAssistant from attempting to create and dismiss persistent
# notifications. These calls would fail without this fixture since the persistent_notification 
# integration is never loaded during a test.
@pytest.fixture(name="skip_notifications", autouse=True)
def skip_notifications_fixture():
    """Skip notification calls."""
    with patch("homeassistant.components.persistent_notification.async_create"), patch(
        "homeassistant.components.persistent_notification.async_dismiss"
    ):
        yield

# This fixture, when used, will result in calls to async_get_data to return None. To have the call
# return a value, we would add the `return_value=<VALUE_TO_RETURN>` parameter to the patch call.
@pytest.fixture(name="bypass_get_data")
def bypass_get_data_fixture():
    """Skip calls to get data from API."""
    with patch("custom_components.nodered_conversation.ConfigFlow._async_get_data"):
        yield

# In this fixture, we are mocking the HomeAssistant's secrets manager to return a fake API key
@pytest.fixture(name="mock_secrets")
def mock_secrets_fixture():
    """Mock HomeAssistant secrets."""
    with patch("homeassistant.util.yaml.load_yaml", return_value={"nodered_api_key": "fake_api_key"}):
        yield