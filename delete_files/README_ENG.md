[![ca](https://img.shields.io/badge/lang-ca-blue.svg)](https://github.com/CSUC/RDR-scripts/blob/main/delete_files/README.md)
[![en](https://img.shields.io/badge/lang-en-green.svg)](https://github.com/CSUC/RDR-scripts/blob/main/delete_files/README_ENG.md)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CSUC/RDR-scripts/blob/main/delete_files/delete_files_script.ipynb)

# Script to delete files from a dataset in Dataverse

For any questions regarding the code, please contact rdr-contacte@csuc.cat

## Description

This script is designed to interact with the Research Data Repository (https://dataverse.csuc.cat/) and allows users to delete files from a Dataverse dataset identified by a DOI.

The script uses the `pyDataverse` library to retrieve dataset information and the `requests` library to execute file deletion requests through the Dataverse API.

Users can choose whether they want to delete:

- all files in the dataset
- files from a specific folder
- files from a specific subfolder

Before deleting files, the script displays a preview of the selected files and requires explicit confirmation by typing `Yes`.

## Requirements

- Python 3.x
- `pyDataverse` library
- `requests` library
- `pandas` library
- `ipywidgets` library
- A Dataverse API token with sufficient permissions to modify the dataset

## Usage

1. **Input Parameters**:
    - DOI: Digital Object Identifier (DOI) of the dataset.
    - Token: Authentication token to access the Dataverse repository.

2. **Configuration**:
    - Initializes the base URL of the Dataverse instance.
    - Authenticates the API using the provided token.

3. **Reading dataset files**:
    - Retrieves the metadata of the specified dataset.
    - Extracts the list of available files.
    - Displays the file identifier, filename, and folder/subfolder location.

4. **Selecting files to delete**:
    - Allows users to choose between deleting all dataset files or only files from a specific folder/subfolder.
    - Displays a dropdown menu with the available folders.

5. **Confirmation**:
    - Displays the selected files before deletion.
    - Requires the user to type exactly `Yes` to confirm.
    - If the user does not type `Yes`, the operation is cancelled.

6. **Deleting files**:
    - Sends a `DELETE` request to the Dataverse API for each selected file.
    - Displays a summary of successfully deleted files and possible errors.

## File Structure

- `delete_dataset_files_script.ipynb`: Main script used to select and delete files from a dataset.
- `README.md`: Script documentation in Catalan.
- `README_ENG.md`: Script documentation in English.

## Example Usage

```python
# Enter your API token
API_TOKEN = "YOUR_API_TOKEN"

# Enter the dataset DOI
DOI = "doi:10.34810/data2432"
