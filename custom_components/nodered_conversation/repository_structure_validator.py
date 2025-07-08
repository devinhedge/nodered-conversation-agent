"""Module for validating the repository structure of a HACS integration."""

import os
import sys
import json
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


def verify_single_integration_subdirectory() -> bool:
    """
    Verify that there's only one subdirectory under /custom_components/.

    This function checks if there's exactly one subdirectory within the
    /custom_components/ directory, which is expected for a HACS integration.

    Returns:
        bool: True if there's exactly one subdirectory, False otherwise.

    Raises:
        OSError: If there's an error accessing the file system.
    """
    try:
        repo_root: str = os.getcwd()
        custom_components_path: str = os.path.join(repo_root, 'custom_components')
        
        if not os.path.isdir(custom_components_path):
            print("Error: /custom_components/ directory does not exist.")
            return False
        
        subdirectories: List[str] = [d for d in os.listdir(custom_components_path) 
                                     if os.path.isdir(os.path.join(custom_components_path, d))]
        
        if len(subdirectories) == 1:
            return True
        elif len(subdirectories) == 0:
            print("Error: No subdirectories found in /custom_components/.")
            return False
        else:
            print(f"Error: Multiple subdirectories found in /custom_components/: {', '.join(subdirectories)}")
            return False
    
    except OSError as error:
        print(f"Error accessing the /custom_components/ directory: {error}")
        return False


def validate_integration_domain_name_match() -> bool:
    """
    Validate that the integration's domain name matches its directory name.

    This function checks if the name of the single subdirectory under /custom_components/
    matches the integration's domain name as specified in the manifest.json file.

    Returns:
        bool: True if the names match, False otherwise.

    Raises:
        OSError: If there's an error accessing the file system.
        json.JSONDecodeError: If there's an error parsing the manifest.json file.
    """
    try:
        repo_root: str = os.getcwd()
        custom_components_path: str = os.path.join(repo_root, 'custom_components')
        
        # Get the name of the single subdirectory
        subdirectories: List[str] = [d for d in os.listdir(custom_components_path) 
                                     if os.path.isdir(os.path.join(custom_components_path, d))]
        if len(subdirectories) != 1:
            print("Error: Expected exactly one subdirectory in /custom_components/.")
            return False
        
        directory_name: str = subdirectories[0]
        
        # Check if manifest.json exists
        manifest_path: str = os.path.join(custom_components_path, directory_name, 'manifest.json')
        if not os.path.isfile(manifest_path):
            print(f"Error: manifest.json not found in {os.path.join(custom_components_path, directory_name)}")
            return False
        
        # Extract the integration's domain name from manifest.json
        with open(manifest_path, 'r') as manifest_file:
            manifest_data: dict = json.load(manifest_file)
        
        domain_name: Optional[str] = manifest_data.get('domain')
        
        if domain_name is None:
            print("Error: 'domain' field not found in manifest.json.")
            return False
        
        if not isinstance(domain_name, str):
            print(f"Error: 'domain' field in manifest.json is not a string. Found type: {type(domain_name)}")
            return False
        
        # Compare the directory name with the domain name
        if directory_name == domain_name:
            return True
        else:
            print(f"Error: Directory name '{directory_name}' does not match domain name '{domain_name}' in manifest.json.")
            return False
    
    except OSError as error:
        print(f"Error accessing the file system: {error}")
        return False
    except json.JSONDecodeError as error:
        print(f"Error parsing manifest.json: {error}")
        return False


def confirm_integration_files_location() -> bool:
    """
    Confirm that all integration files are located in the correct subdirectory.

    This function checks if all essential integration files are present in the
    single subdirectory under /custom_components/ and that no integration-related
    files exist outside this subdirectory.

    Returns:
        bool: True if all files are correctly located, False otherwise.

    Raises:
        OSError: If there's an error accessing the file system.
    """
    try:
        repo_root: str = os.getcwd()
        custom_components_path: str = os.path.join(repo_root, 'custom_components')
        
        # Get the name of the single subdirectory
        subdirectories: List[str] = [d for d in os.listdir(custom_components_path) 
                                     if os.path.isdir(os.path.join(custom_components_path, d))]
        if len(subdirectories) != 1:
            print("Error: Expected exactly one subdirectory in /custom_components/.")
            return False
        
        integration_dir: str = subdirectories[0]
        integration_path: str = os.path.join(custom_components_path, integration_dir)
        
        # List of essential files
        essential_files: List[str] = ['__init__.py', 'manifest.json', 'config_flow.py']
        
        # Check for essential files
        missing_files: List[str] = [file for file in essential_files if not os.path.isfile(os.path.join(integration_path, file))]
        if missing_files:
            print(f"Error: Missing essential files in {integration_path}: {', '.join(missing_files)}")
            return False
        
        # Check for misplaced files
        misplaced_files: List[str] = []
        for root, _, files in os.walk(repo_root):
            if root != integration_path and root.startswith(custom_components_path):
                for file in files:
                    if file.endswith('.py') or file in ['manifest.json', 'config_flow.py']:
                        misplaced_files.append(os.path.join(root, file))
        
        if misplaced_files:
            print("Error: Found integration-related files outside the integration directory:")
            for file in misplaced_files:
                print(f"  - {file}")
            return False
        
        return True
    
    except OSError as error:
        print(f"Error accessing the file system: {error}")
        return False


def validate_hacs_integration() -> bool:
    """
    Validate the structure of a HACS integration.

    This function performs a series of checks to validate the structure
    of a HACS integration, including verifying the existence of required
    directories and the presence of a single integration subdirectory.

    Returns:
        bool: True if all checks pass, False otherwise.
    """
    checks: List[Tuple[str, bool]] = [
        ("Custom Components Directory", check_custom_components_directory()),
        ("Single Integration Subdirectory", verify_single_integration_subdirectory()),
        ("Integration Domain Name Match", validate_integration_domain_name_match()),
        ("Integration Files Location", confirm_integration_files_location()),
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