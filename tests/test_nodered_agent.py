"""Tests for the NodeRedAgent class."""
import pytest
from unittest.mock import patch, MagicMock, call
import aiohttp

# Mock Home Assistant and custom component imports
class HomeAssistantError(Exception):
    """Mock HomeAssistantError."""

ERROR_CANNOT_CONNECT = "cannot_connect"
ERROR_INVALID_AUTH = "invalid_auth"

# Import the NodeRedAgent class
from custom_components.nodered_conversation import NodeRedAgent

@pytest.fixture
def mock_hass() -> MagicMock:
    """Create a mock Home Assistant instance."""
    return MagicMock()

@pytest.fixture
def mock_config_entry() -> MagicMock:
    """Create a mock config entry."""
    return MagicMock()

def test_nodered_agent_init(mock_hass: MagicMock, mock_config_entry: MagicMock):
    """Test NodeRedAgent initialization."""
    agent = NodeRedAgent(mock_hass, mock_config_entry)
    assert agent.hass == mock_hass
    assert agent.entry == mock_config_entry
    assert isinstance(agent.history, dict)

def test_nodered_agent_supported_languages():
    """Test supported_languages property."""
    agent = NodeRedAgent(MagicMock(), MagicMock())
    assert agent.supported_languages == "*"

@pytest.mark.asyncio
async def test_nodered_agent_async_process(mock_hass: MagicMock, mock_config_entry: MagicMock):
    """Test async_process method."""
    agent = NodeRedAgent(mock_hass, mock_config_entry)
    
    mock_config_entry.data = {
        "nodered_url": "http://test.url",
        "nodered_user": "testuser",
        "nodered_pass": "testpass"
    }
    
    with patch.object(agent, 'call_post_request', return_value='{"finish_reason": "success", "message": {"content": "Test response"}}'):
        result = await agent.async_process(MagicMock(text="Test input", conversation_id=None))
    
    assert result.response.speech["plain"]["speech"] == "Test response"
    assert result.conversation_id is not None

@pytest.mark.asyncio
async def test_nodered_agent_async_process_error_handling(mock_hass: MagicMock, mock_config_entry: MagicMock):
    """Test async_process method error handling."""
    agent = NodeRedAgent(mock_hass, mock_config_entry)
    
    mock_config_entry.data = {
        "nodered_url": "http://test.url",
        "nodered_user": "testuser",
        "nodered_pass": "testpass"
    }
    
    with patch.object(agent, 'call_post_request', side_effect=HomeAssistantError(ERROR_CANNOT_CONNECT)):
        with pytest.raises(HomeAssistantError) as exc_info:
            await agent.async_process(MagicMock(text="Test input", conversation_id=None))
        assert str(exc_info.value) == ERROR_CANNOT_CONNECT

@pytest.mark.asyncio
async def test_nodered_agent_call_post_request_ssl_warning(mock_hass: MagicMock, mock_config_entry: MagicMock, caplog):
    """Test call_post_request method with SSL verification disabled."""
    agent = NodeRedAgent(mock_hass, mock_config_entry)
    
    mock_response = MagicMock()
    mock_response.text.return_value = '{"finish_reason": "success", "message": {"content": "Test response"}}'
    mock_response.raise_for_status.return_value = None
    
    with patch('aiohttp.ClientSession') as mock_session:
        mock_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response
        await agent.call_post_request("http://test.url", "test_auth", {})
    
    assert "SSL verification is disabled. This is not recommended for production use." in caplog.text

@pytest.mark.asyncio
async def test_nodered_agent_call_post_request_connection_error(mock_hass: MagicMock, mock_config_entry: MagicMock):
    """Test call_post_request method with connection error."""
    agent = NodeRedAgent(mock_hass, mock_config_entry)
    
    with patch('aiohttp.ClientSession') as mock_session:
        mock_session.return_value.__aenter__.return_value.post.side_effect = aiohttp.ClientError()
        with pytest.raises(HomeAssistantError) as exc_info:
            await agent.call_post_request("http://test.url", "test_auth", {})
        assert str(exc_info.value) == ERROR_CANNOT_CONNECT

@pytest.mark.asyncio
async def test_nodered_agent_async_process_empty_response(mock_hass: MagicMock, mock_config_entry: MagicMock):
    """Test async_process method with empty response."""
    agent = NodeRedAgent(mock_hass, mock_config_entry)
    
    mock_config_entry.data = {
        "nodered_url": "http://test.url",
        "nodered_user": "testuser",
        "nodered_pass": "testpass"
    }
    
    with patch.object(agent, 'call_post_request', return_value='{}'):
        result = await agent.async_process(MagicMock(text="Test input", conversation_id=None))
    
    assert result.response.speech["plain"]["speech"] == ""
    assert result.conversation_id is not None

@pytest.mark.asyncio
async def test_nodered_agent_async_process_malformed_response(mock_hass: MagicMock, mock_config_entry: MagicMock):
    """Test async_process method with malformed response."""
    agent = NodeRedAgent(mock_hass, mock_config_entry)
    
    mock_config_entry.data = {
        "nodered_url": "http://test.url",
        "nodered_user": "testuser",
        "nodered_pass": "testpass"
    }
    
    with patch.object(agent, 'call_post_request', return_value='{"invalid": "response"}'):
        result = await agent.async_process(MagicMock(text="Test input", conversation_id=None))
    
    assert result.response.speech["plain"]["speech"] == ""
    assert result.conversation_id is not None

# Add more tests as needed for other methods and edge cases