[![ca](https://img.shields.io/badge/lang-ca-blue.svg)](https://github.com/CSUC/RDR-scripts/blob/main/extract_metadata/README.md)
[![en](https://img.shields.io/badge/lang-en-green.svg)](https://github.com/CSUC/RDR-scripts/blob/main/extract_metadata/README_ENG.md)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CSUC/RDR-scripts/blob/main/extract_metadata/extract_metadata_script.ipynb)

# Automatic Metadata Export Script
For any queries regarding the code, contact rdr-contacte@csuc.cat

## Script Objective
This script automates the extraction and export of metadata from a dataset on Dataverse.

## Description

The script retrieves metadata from a specified dataset using the provided DOI and token. It then organizes the metadata into a DataFrame and exports it to a CSV file. The script is capable of running both in Google Colab and Jupyter Notebook environments, providing convenient options for downloading the metadata file.

## Requirements

Ensure that the following libraries are installed:
- pyDataverse
- html2text
- pandas
- ipywidgets (for Google Colab)

## Usage

1. **Input Values:**
    - DOI: Enter the DOI of the dataset.
    - Token: Provide the API token for authentication.
    - Base URL: Specify the URL of the Dataverse repository.

2. **Execution:**
    - Execute the script after providing the required input values.
    - The script will extract metadata from the dataset and organize it into a DataFrame.
    - The DataFrame will be saved as a CSV file in the specified directory.

3. **Download Options:**
    - **Google Colab:** If running in Google Colab, a download button will be provided to download the metadata file.
    - **Jupyter Notebook:** In Jupyter Notebook, a download link will be displayed for downloading the metadata file.


