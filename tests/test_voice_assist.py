"""Unit tests for the voice assist module of the NodeRed Conversation integration."""
import pytest
from unittest.mock import patch, MagicMock
from homeassistant.core import HomeAssistant
from custom_components.nodered_conversation.voice_assist import VoiceAssist

@pytest.fixture
def mock_hass():
    """Create a mock Home Assistant instance."""
    return MagicMock(spec=HomeAssistant)

@pytest.fixture
def voice_assist(mock_hass):
    """Create a VoiceAssist instance for testing."""
    return VoiceAssist(mock_hass)

def test_voice_assist_initialization(voice_assist):
    """Test that the VoiceAssist class initializes correctly."""
    assert isinstance(voice_assist, VoiceAssist)
    assert voice_assist.hass is not None

@pytest.mark.asyncio
async def test_process_voice_command(voice_assist, mock_hass):
    """Test processing a voice command."""
    with patch('custom_components.nodered_conversation.voice_assist.VoiceAssist._send_to_nodered') as mock_send:
        mock_send.return_value = "Lights turned on"
        result = await voice_assist.process_voice_command("Turn on the lights")
        assert result == "Lights turned on"
        mock_send.assert_called_once_with("Turn on the lights")

@pytest.mark.asyncio
async def test_process_voice_command_error(voice_assist, mock_hass):
    """Test error handling when processing a voice command."""
    with patch('custom_components.nodered_conversation.voice_assist.VoiceAssist._send_to_nodered') as mock_send:
        mock_send.side_effect = Exception("Connection error")
        result = await voice_assist.process_voice_command("Turn on the lights")
        assert "Error processing voice command" in result

@pytest.mark.asyncio
async def test_process_empty_command(voice_assist, mock_hass):
    """Test processing an empty voice command."""
    result = await voice_assist.process_voice_command("")
    assert "Error processing voice command" in result

@pytest.mark.asyncio
async def test_process_long_command(voice_assist, mock_hass):
    """Test processing a very long voice command."""
    long_command = "Turn on the lights " * 100  # Create a very long command
    with patch('custom_components.nodered_conversation.voice_assist.VoiceAssist._send_to_nodered') as mock_send:
        mock_send.return_value = "Command processed"
        result = await voice_assist.process_voice_command(long_command)
        assert result == "Command processed"
        mock_send.assert_called_once_with(long_command)

@pytest.mark.asyncio
async def test_process_special_characters(voice_assist, mock_hass):
    """Test processing a voice command with special characters."""
    special_command = "Turn on the lights in room #1 & room #2"
    with patch('custom_components.nodered_conversation.voice_assist.VoiceAssist._send_to_nodered') as mock_send:
        mock_send.return_value = "Command processed"
        result = await voice_assist.process_voice_command(special_command)
        assert result == "Command processed"
        mock_send.assert_called_once_with(special_command)

# The rest of the file should remain unchanged
