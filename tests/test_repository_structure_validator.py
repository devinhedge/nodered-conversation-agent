"""Tests for the repository_structure_validator module."""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Mock the homeassistant module
sys.modules['homeassistant'] = MagicMock()
sys.modules['homeassistant.components'] = MagicMock()
sys.modules['homeassistant.components.conversation'] = MagicMock()
sys.modules['homeassistant.config_entries'] = MagicMock()
sys.modules['homeassistant.const'] = MagicMock()
sys.modules['homeassistant.core'] = MagicMock()
sys.modules['homeassistant.helpers'] = MagicMock()
sys.modules['homeassistant.util'] = MagicMock()

from custom_components.nodered_conversation.repository_structure_validator import check_custom_components_directory


@pytest.fixture
def mock_filesystem(tmp_path):
    """Create a mock filesystem structure."""
    custom_components_dir = tmp_path / "custom_components"
    custom_components_dir.mkdir()
    return tmp_path


def test_check_custom_components_directory_exists(mock_filesystem):
    """Test when the custom_components directory exists."""
    with patch('os.getcwd', return_value=str(mock_filesystem)):
        assert check_custom_components_directory() is True


def test_check_custom_components_directory_not_exists(tmp_path):
    """Test when the custom_components directory does not exist."""
    with patch('os.getcwd', return_value=str(tmp_path)):
        assert check_custom_components_directory() is False


def test_check_custom_components_directory_error():
    """Test when there's an error accessing the filesystem."""
    with patch('os.getcwd', side_effect=OSError("Mock OSError")):
        assert check_custom_components_directory() is False


@pytest.mark.parametrize("dir_exists", [True, False])
def test_check_custom_components_directory_parametrized(mock_filesystem, dir_exists):
    """Parametrized test for different directory existence scenarios."""
    if not dir_exists:
        os.rmdir(mock_filesystem / "custom_components")
    
    with patch('os.getcwd', return_value=str(mock_filesystem)):
        assert check_custom_components_directory() is dir_exists