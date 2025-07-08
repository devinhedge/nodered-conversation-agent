"""Tests for the repository_structure_validator module."""

import os
import sys
import pytest
import json
from unittest.mock import patch, MagicMock
from pathlib import Path

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

from custom_components.nodered_conversation.repository_structure_validator import (
    check_custom_components_directory,
    verify_single_integration_subdirectory,
    validate_integration_domain_name_match,
    confirm_integration_files_location
)

class MockFilesystem:
    """Mock filesystem for testing purposes."""

    def __init__(self, tmp_path: Path):
        """Initialize the mock filesystem."""
        self.root = tmp_path
        self.custom_components_dir = self.root / "custom_components"
        self.custom_components_dir.mkdir()

    def create_integration_dir(self, name: str) -> Path:
        """Create an integration directory."""
        integration_dir = self.custom_components_dir / name
        integration_dir.mkdir()
        return integration_dir

    def create_file(self, path: str, content: str = "") -> None:
        """Create a file with the given content."""
        file_path = self.root / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)

    def remove_file(self, path: str) -> None:
        """Remove a file if it exists."""
        file_path = self.root / path
        if file_path.exists():
            file_path.unlink()

@pytest.fixture
def mock_filesystem(tmp_path):
    """Create a mock filesystem structure."""
    return MockFilesystem(tmp_path)

class BaseRepositoryStructureTest:
    """Base class for repository structure tests."""

    @pytest.fixture(autouse=True)
    def setup_method(self, mock_filesystem):
        """Set up the test environment."""
        self.mock_fs = mock_filesystem
        self.patcher = patch('os.getcwd', return_value=str(self.mock_fs.root))
        self.patcher.start()

    def teardown_method(self):
        """Tear down the test environment."""
        self.patcher.stop()

class TestCustomComponentsDirectory(BaseRepositoryStructureTest):
    """Tests for the check_custom_components_directory function."""

    def test_check_custom_components_directory_exists(self):
        """Test when the custom_components directory exists."""
        assert check_custom_components_directory() is True

    def test_check_custom_components_directory_not_exists(self):
        """Test when the custom_components directory does not exist."""
        self.mock_fs.custom_components_dir.rmdir()
        assert check_custom_components_directory() is False

    def test_check_custom_components_directory_error(self):
        """Test when there's an error accessing the filesystem."""
        with patch('os.path.isdir', side_effect=OSError("Mock OSError")):
            assert check_custom_components_directory() is False

    @pytest.mark.parametrize("dir_exists", [True, False])
    def test_check_custom_components_directory_parametrized(self, dir_exists):
        """Parametrized test for different directory existence scenarios."""
        if not dir_exists:
            self.mock_fs.custom_components_dir.rmdir()
        assert check_custom_components_directory() is dir_exists

class TestSingleIntegrationSubdirectory(BaseRepositoryStructureTest):
    """Tests for the verify_single_integration_subdirectory function."""

    def test_verify_single_integration_subdirectory_success(self):
        """Test when there's exactly one subdirectory in custom_components."""
        self.mock_fs.create_integration_dir("my_integration")
        assert verify_single_integration_subdirectory() is True

    def test_verify_single_integration_subdirectory_no_subdirectory(self):
        """Test when there are no subdirectories in custom_components."""
        assert verify_single_integration_subdirectory() is False

    def test_verify_single_integration_subdirectory_multiple_subdirectories(self):
        """Test when there are multiple subdirectories in custom_components."""
        self.mock_fs.create_integration_dir("integration1")
        self.mock_fs.create_integration_dir("integration2")
        assert verify_single_integration_subdirectory() is False

    def test_verify_single_integration_subdirectory_error(self):
        """Test when there's an error accessing the filesystem."""
        with patch('os.listdir', side_effect=OSError("Mock OSError")):
            assert verify_single_integration_subdirectory() is False

    @pytest.mark.parametrize("num_subdirs,expected", [(0, False), (1, True), (2, False)])
    def test_verify_single_integration_subdirectory_parametrized(self, num_subdirs, expected):
        """Parametrized test for different numbers of subdirectories."""
        for i in range(num_subdirs):
            self.mock_fs.create_integration_dir(f"integration{i+1}")
        assert verify_single_integration_subdirectory() is expected

class TestIntegrationFilesLocation(BaseRepositoryStructureTest):
    """Tests for the confirm_integration_files_location function."""

    def test_confirm_integration_files_location_success(self):
        """Test when all integration files are in the correct location."""
        integration_dir = self.mock_fs.create_integration_dir("my_integration")
        for file in ["__init__.py", "manifest.json", "config_flow.py"]:
            self.mock_fs.create_file(f"custom_components/my_integration/{file}")
        assert confirm_integration_files_location() is True

    def test_confirm_integration_files_location_missing_file(self):
        """Test when an essential file is missing."""
        integration_dir = self.mock_fs.create_integration_dir("my_integration")
        self.mock_fs.create_file("custom_components/my_integration/__init__.py")
        self.mock_fs.create_file("custom_components/my_integration/manifest.json")
        assert confirm_integration_files_location() is False

    def test_confirm_integration_files_location_misplaced_file(self):
        """Test when an integration file is misplaced."""
        integration_dir = self.mock_fs.create_integration_dir("my_integration")
        for file in ["__init__.py", "manifest.json", "config_flow.py"]:
            self.mock_fs.create_file(f"custom_components/my_integration/{file}")
        self.mock_fs.create_file("custom_components/misplaced.py")
        assert confirm_integration_files_location() is False

    def test_confirm_integration_files_location_error(self):
        """Test when there's an error accessing the filesystem."""
        with patch('os.walk', side_effect=OSError("Mock OSError")):
            assert confirm_integration_files_location() is False

    @pytest.mark.parametrize("files,expected", [
        (["__init__.py", "manifest.json", "config_flow.py"], True),
        (["__init__.py", "manifest.json"], False),
        (["__init__.py", "manifest.json", "config_flow.py", "extra.py"], True),
    ])
    def test_confirm_integration_files_location_parametrized(self, files, expected):
        """Parametrized test for different file configurations."""
        integration_dir = self.mock_fs.create_integration_dir("my_integration")
        for file in files:
            self.mock_fs.create_file(f"custom_components/my_integration/{file}")
        assert confirm_integration_files_location() is expected

class TestIntegrationDomainNameMatch(BaseRepositoryStructureTest):
    """Tests for the validate_integration_domain_name_match function."""

    def test_validate_integration_domain_name_match_success(self):
        """Test when directory name matches domain name in manifest.json."""
        integration_dir = self.mock_fs.create_integration_dir("my_integration")
        manifest_content = json.dumps({"domain": "my_integration"})
        self.mock_fs.create_file("custom_components/my_integration/manifest.json", manifest_content)
        assert validate_integration_domain_name_match() is True

    def test_validate_integration_domain_name_match_mismatch(self):
        """Test when directory name doesn't match domain name in manifest.json."""
        integration_dir = self.mock_fs.create_integration_dir("my_integration")
        manifest_content = json.dumps({"domain": "different_name"})
        self.mock_fs.create_file("custom_components/my_integration/manifest.json", manifest_content)
        assert validate_integration_domain_name_match() is False

    def test_validate_integration_domain_name_match_missing_manifest(self):
        """Test when manifest.json is missing."""
        self.mock_fs.create_integration_dir("my_integration")
        assert validate_integration_domain_name_match() is False

    def test_validate_integration_domain_name_match_invalid_manifest(self):
        """Test when manifest.json is invalid."""
        integration_dir = self.mock_fs.create_integration_dir("my_integration")
        self.mock_fs.create_file("custom_components/my_integration/manifest.json", "invalid json")
        assert validate_integration_domain_name_match() is False

    def test_validate_integration_domain_name_match_missing_domain(self):
        """Test when domain key is missing in manifest.json."""
        integration_dir = self.mock_fs.create_integration_dir("my_integration")
        manifest_content = json.dumps({"name": "My Integration"})
        self.mock_fs.create_file("custom_components/my_integration/manifest.json", manifest_content)
        assert validate_integration_domain_name_match() is False

    def test_validate_integration_domain_name_match_error(self):
        """Test when there's an error accessing the filesystem."""
        with patch('os.listdir', side_effect=OSError("Mock OSError")):
            assert validate_integration_domain_name_match() is False

if __name__ == "__main__":
    pytest.main(["-v", "--cov=custom_components.nodered_conversation", "--cov-report=term-missing", "--cov-report=html"])