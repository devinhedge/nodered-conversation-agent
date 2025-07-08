"""Test the NodeRed Conversation config flow."""
import sys
import os
from unittest.mock import patch
from typing import Any

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant import config_entries, data_entry_flow
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_NAME
from custom_components.nodered_conversation.const import (
    DOMAIN,
    CONF_NODERED_URL,
    CONF_NODERED_USER,
    CONF_NODERED_PASS,
)
from custom_components.nodered_conversation.config_flow import ConfigFlow, CannotConnect, InvalidAuth

pytest_plugins = ["pytest_asyncio"]

@pytest.fixture(autouse=True)
def bypass_setup_fixture():
    """Prevent setup."""
    with patch("custom_components.nodered_conversation.async_setup_entry", return_value=True):
        yield

@pytest.fixture
def mock_validate_input():
    """Mock the validate_input function."""
    with patch("custom_components.nodered_conversation.config_flow.validate_input") as mock:
        yield mock

@pytest.mark.asyncio
async def test_form(hass: HomeAssistant):
    """Test we get the form."""
    hass = await hass
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert isinstance(result, dict)
    assert result.get("type") == data_entry_flow.FlowResultType.FORM
    assert result.get("errors") is None

    with patch(
        "custom_components.nodered_conversation.config_flow.ConfigFlow.async_step_user",
        return_value={"title": "NodeRed Conversation"},
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_NAME: "Test NodeRed",
                CONF_NODERED_URL: "http://example.com",
                CONF_NODERED_USER: "testuser",
                CONF_NODERED_PASS: "testpass",
            },
        )
        await hass.async_block_till_done()

    assert isinstance(result2, dict)
    assert result2.get("type") == data_entry_flow.FlowResultType.CREATE_ENTRY
    assert result2.get("title") == "NodeRed Conversation"
    assert result2.get("data") == {
        CONF_NAME: "Test NodeRed",
        CONF_NODERED_URL: "http://example.com",
        CONF_NODERED_USER: "testuser",
        CONF_NODERED_PASS: "testpass",
    }

@pytest.mark.asyncio
async def test_form_invalid_auth(hass: HomeAssistant, mock_validate_input):
    """Test we handle invalid auth."""
    hass = await hass
    mock_validate_input.side_effect = InvalidAuth

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_NAME: "Test NodeRed",
            CONF_NODERED_URL: "http://example.com",
            CONF_NODERED_USER: "testuser",
            CONF_NODERED_PASS: "wrongpass",
        },
    )

    assert isinstance(result2, dict)
    assert result2.get("type") == data_entry_flow.FlowResultType.FORM
    assert result2.get("errors") == {"base": "invalid_auth"}

@pytest.mark.asyncio
async def test_form_cannot_connect(hass: HomeAssistant, mock_validate_input):
    """Test we handle cannot connect error."""
    hass = await hass
    mock_validate_input.side_effect = CannotConnect

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_NAME: "Test NodeRed",
            CONF_NODERED_URL: "http://example.com",
            CONF_NODERED_USER: "testuser",
            CONF_NODERED_PASS: "testpass",
        },
    )

    assert isinstance(result2, dict)
    assert result2.get("type") == data_entry_flow.FlowResultType.FORM
    assert result2.get("errors") == {"base": "cannot_connect"}

@pytest.mark.asyncio
async def test_form_unknown_error(hass: HomeAssistant, mock_validate_input):
    """Test we handle unknown errors."""
    hass = await hass
    mock_validate_input.side_effect = Exception("Unknown error")

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_NAME: "Test NodeRed",
            CONF_NODERED_URL: "http://example.com",
            CONF_NODERED_USER: "testuser",
            CONF_NODERED_PASS: "testpass",
        },
    )

    assert isinstance(result2, dict)
    assert result2.get("type") == data_entry_flow.FlowResultType.FORM
    assert result2.get("errors") == {"base": "unknown"}

@pytest.mark.asyncio
async def test_options_flow(hass: HomeAssistant):
    """Test config flow options."""
    hass = await hass
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_NAME: "Test NodeRed",
            CONF_NODERED_URL: "http://example.com",
            CONF_NODERED_USER: "testuser",
            CONF_NODERED_PASS: "testpass",
        },
        options={},
    )
    config_entry.add_to_hass(hass)

    result = await hass.config_entries.options.async_init(config_entry.entry_id)

    assert isinstance(result, dict)
    assert result.get("type") == data_entry_flow.FlowResultType.FORM
    assert result.get("step_id") == "init"

    result2 = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={
            CONF_NODERED_URL: "http://new-example.com",
            CONF_NODERED_USER: "newuser",
            CONF_NODERED_PASS: "newpass",
        },
    )

    assert isinstance(result2, dict)
    assert result2.get("type") == data_entry_flow.FlowResultType.CREATE_ENTRY
    assert config_entry.data == {
        CONF_NAME: "Test NodeRed",
        CONF_NODERED_URL: "http://new-example.com",
        CONF_NODERED_USER: "newuser",
        CONF_NODERED_PASS: "newpass",
    }