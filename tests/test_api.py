"""API tests for the NodeRed Conversation integration."""
import pytest
from unittest.mock import patch, MagicMock
import aiohttp
from homeassistant.core import HomeAssistant
from custom_components.nodered_conversation.voice_assist import VoiceAssist
from custom_components.nodered_conversation.assist import Assist

@pytest.fixture
def mock_hass():
    """Create a mock Home Assistant instance."""
    return MagicMock(spec=HomeAssistant)

@pytest.fixture
def mock_session():
    """Create a mock aiohttp ClientSession."""
    return MagicMock(spec=aiohttp.ClientSession)

@pytest.mark.asyncio
async def test_voice_assist_api_call(mock_hass, mock_session):
    """Test API call for voice assist."""
    voice_assist = VoiceAssist(mock_hass)
    with patch('aiohttp.ClientSession', return_value=mock_session):
        mock_response = MagicMock()
        mock_response.text.return_value = "API response"
        mock_response.raise_for_status = MagicMock()
        mock_session.post.return_value.__aenter__.return_value = mock_response

        result = await voice_assist.process_voice_command("Turn on the lights")
        
        assert result == "API response"
        mock_session.post.assert_called_once()
        mock_response.raise_for_status.assert_called_once()

@pytest.mark.asyncio
async def test_assist_api_call(mock_hass, mock_session):
    """Test API call for assist."""
    assist = Assist(mock_hass)
    with patch('aiohttp.ClientSession', return_value=mock_session):
        mock_response = MagicMock()
        mock_response.text.return_value = "API response"
        mock_response.raise_for_status = MagicMock()
        mock_session.post.return_value.__aenter__.return_value = mock_response

        result = await assist.process_command("What's the weather?")
        
        assert result == "API response"
        mock_session.post.assert_called_once()
        mock_response.raise_for_status.assert_called_once()

@pytest.mark.asyncio
async def test_api_error_handling(mock_hass, mock_session):
    """Test error handling for API calls."""
    voice_assist = VoiceAssist(mock_hass)
    with patch('aiohttp.ClientSession', return_value=mock_session):
        mock_session.post.side_effect = aiohttp.ClientError("Connection error")

        result = await voice_assist.process_voice_command("Turn on the lights")
        
        assert "Error processing voice command" in result
        mock_session.post.assert_called_once()

# Add more API test cases as needed