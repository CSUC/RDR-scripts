# Parameters (fill these in before running)
TOKEN = "your_api_token_here"
DOI = "doi:10.34810/dataXXX"
TARGET_ALIAS = "your_target_alias_here"  # e.g., csuc or ub

# ----------------------
# Install required packages
import subprocess
import sys

def install_packages():
    """Install or update required Python packages."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "-q"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyDataverse", "requests", "-q"])
    print("Libraries downloaded or updated successfully.")

# ----------------------
# Move dataset function
import requests
from pyDataverse.api import NativeApi

def move_dataset(api_token, persistent_id, alias):
    """
    Move a dataset to a different dataverse.

    Args:
        api_token (str): API token for authentication.
        persistent_id (str): Persistent identifier (DOI) of the dataset.
        alias (str): Alias of the target dataverse.
    """
    server_url = 'https://dataverse.csuc.cat'
    headers = {"X-Dataverse-key": api_token}

    # Get dataset ID
    dataset_url = f"{server_url}/api/datasets/:persistentId/?persistentId={persistent_id}"
    response = requests.get(dataset_url, headers=headers)

    if response.status_code != 200:
        print(" Failed to retrieve dataset information.")
        return

    data = response.json().get('data', {})
    dataset_id = data.get('id')

    if not dataset_id:
        print(" Dataset ID not found in API response.")
        return

    # Move dataset
    move_url = f"{server_url}/api/datasets/{dataset_id}/move/{alias}"
    move_response = requests.post(move_url, headers=headers)

    if move_response.status_code == 200:
        print(" Dataset move operation successful.")
    else:
        print(f" Dataset move operation failed. Response: {move_response.text}")

# ----------------------
# Execute
if __name__ == "__main__":
    install_packages()
    
    if not TOKEN or not DOI or not TARGET_ALIAS:
        print(" Please fill in the TOKEN, DOI, and TARGET_ALIAS at the top of the script.")
    else:
        move_dataset(TOKEN, DOI, TARGET_ALIAS)
