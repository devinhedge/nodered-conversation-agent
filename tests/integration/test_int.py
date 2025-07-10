"""Integration tests for the NodeRed Conversation integration."""
from unittest.mock import patch, AsyncMock
from homeassistant.setup import async_setup_component
from homeassistant.helpers import intent
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.nodered_conversation import DOMAIN

async def test_setup_unload_and_reload_entry(hass):
    """Test entry setup and unload."""
    # Define some mock config data
    config_data = {
        "url": "http://localhost:1880",
        "username": "test_user",
        "password": "test_password",
    }

    # Create a mock entry and add it to hass
    entry = MockConfigEntry(domain=DOMAIN, data=config_data)
    entry.add_to_hass(hass)

    # Set up the entry and assert that the setup was successful
    with patch("custom_components.nodered_conversation.NodeRedAgent"):
        assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()

    # Check that the entry is loaded
    assert len(hass.data[DOMAIN]) == 1

    # Reload the entry
    await hass.config_entries.async_reload(entry.entry_id)
    await hass.async_block_till_done()

    # Check that the entry is still loaded after reload
    assert len(hass.data[DOMAIN]) == 1

    # Unload the entry
    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()

    # Check that the entry has been unloaded
    assert DOMAIN not in hass.data

async def test_conversation_agent_registration(hass):
    """Test that the conversation agent is registered correctly."""
    config_data = {
        "url": "http://localhost:1880",
        "username": "test_user",
        "password": "test_password",
    }
    entry = MockConfigEntry(domain=DOMAIN, data=config_data)
    entry.add_to_hass(hass)

    with patch("custom_components.nodered_conversation.NodeRedAgent") as mock_agent:
        assert await async_setup_component(hass, DOMAIN, {})
        await hass.async_block_till_done()

        # Check that the agent was registered
        assert len(hass.data["conversation_agent"].agents) == 1
        assert isinstance(hass.data["conversation_agent"].agents[0], mock_agent.return_value)

async def test_conversation_processing(hass):
    """Test that conversation requests are processed correctly."""
    config_data = {
        "url": "http://localhost:1880",
        "username": "test_user",
        "password": "test_password",
    }
    entry = MockConfigEntry(domain=DOMAIN, data=config_data)
    entry.add_to_hass(hass)

    mock_process = AsyncMock(return_value=intent.IntentResponse(language="en"))
    with patch("custom_components.nodered_conversation.NodeRedAgent.async_process", new=mock_process):
        assert await async_setup_component(hass, DOMAIN, {})
        await hass.async_block_till_done()

        # Process a conversation request
        result = await hass.services.async_call(
            "conversation", "process", {"text": "Turn on the lights"}, blocking=True, return_response=True
        )

        # Check that our mock process method was called
        mock_process.assert_called_once()
        assert isinstance(result, intent.IntentResponse)

async def test_conversation_error_handling(hass):
    """Test error handling in conversation processing."""
    config_data = {
        "url": "http://localhost:1880",
        "username": "test_user",
        "password": "test_password",
    }
    entry = MockConfigEntry(domain=DOMAIN, data=config_data)
    entry.add_to_hass(hass)

    mock_process = AsyncMock(side_effect=Exception("Test error"))
    with patch("custom_components.nodered_conversation.NodeRedAgent.async_process", new=mock_process):
        assert await async_setup_component(hass, DOMAIN, {})
        await hass.async_block_till_done()

        # Process a conversation request
        result = await hass.services.async_call(
            "conversation", "process", {"text": "Turn on the lights"}, blocking=True, return_response=True
        )

        # Check that our mock process method was called and an error response was returned
        mock_process.assert_called_once()
        assert isinstance(result, intent.IntentResponse)
        assert result.response_type == intent.IntentResponseType.ERROR
        assert "Test error" in result.speech["plain"]["speech"]
