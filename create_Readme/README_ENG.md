[![ca](https://img.shields.io/badge/lang-ca-blue.svg)](https://github.com/CSUC/RDR-scripts/blob/main/create_Readme/README.md)
[![en](https://img.shields.io/badge/lang-en-green.svg)](https://github.com/CSUC/RDR-scripts/blob/main/create_Readme/README_ENG.md)
# Script to create a Readme file for a dataset in Dataverse
For any queries regarding the code, contact rdr-contacte@csuc.cat

## Overview
This script is designed to interact with Dataverse repositories, specifically for exporting metadata from datasets identified by Digital Object Identifiers (DOIs). It utilizes the pyDataverse library to access and retrieve metadata, which can then be used to generate a README file providing detailed information about the datasets.

## Requirements
- Python 3.x
- pyDataverse library

## Usage
1. **Input Parameters**: 
    - DOI: The Digital Object Identifier (DOI) of the dataset.
    - Token: Authentication token for accessing the Dataverse repository.

2. **Setup**: 
    - Initialize the base URL for the Dataverse instance.
    - Authenticate the API using the provided token.

3. **Export Metadata**:
    - Retrieve metadata for the specified dataset.
    - Extract various categories of metadata such as citation details, geospatial information, social science metadata, etc.
    - Extract file metadata associated with the dataset.

4. **Create Readme**:
    - Generate a README file containing detailed information about the dataset.
    - Include sections for general information, access information, different kinds of metadata and file overview metadata.
    - Write extracted metadata to the README file.

5. **Download README**:
    - Provide options for downloading the generated README file.
    - In Google Colab, a download button is provided.
    - In Jupyter Notebook, a download link is provided.

## File Structure
- `create_Readme_script.ipynb`: The main script for exporting metadata and generating the README file.
- `Readme.txt`: The generated Readme file containing detailed information about the dataset.

## Usage Example
```python
# Set DOI and token
doi = 'doi:10.34810/dataXXX'
token = 'your_token_here'

# Run the script
