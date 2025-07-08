"""Module for validating the repository structure of a HACS integration."""

import os
import sys
from typing import Optional, List, Tuple


def check_custom_components_directory() -> bool:
    """
    Check for the existence of the /custom_components/ directory.

    This function verifies if the /custom_components/ directory exists in the
    current working directory, which is assumed to be the root of the repository.

    Returns:
        bool: True if the directory exists, False otherwise.

    Raises:
        OSError: If there's an error accessing the file system.
    """
    try:
        repo_root: str = os.getcwd()
        custom_components_path: str = os.path.join(repo_root, 'custom_components')
        return os.path.isdir(custom_components_path)
    except OSError as error:
        print(f"Error accessing the repository structure: {error}")
        return False


def validate_hacs_integration() -> bool:
    """
    Validate the structure of a HACS integration.

    This function performs a series of checks to validate the structure
    of a HACS integration, including verifying the existence of required
    directories.

    Returns:
        bool: True if all checks pass, False otherwise.
    """
    checks: List[Tuple[str, bool]] = [
        ("Custom Components Directory", check_custom_components_directory()),
        # Add other checks here as needed
    ]

    all_passed = True
    for check_name, result in checks:
        print(f"{check_name}: {'Pass' if result else 'Fail'}")
        if not result:
            all_passed = False

    return all_passed


if __name__ == "__main__":
    try:
        validation_result = validate_hacs_integration()
        sys.exit(0 if validation_result else 1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(2)