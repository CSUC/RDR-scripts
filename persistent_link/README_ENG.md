[![ca](https://img.shields.io/badge/lang-ca-blue.svg)](https://github.com/CSUC/RDR-scripts/blob/main/persistent_link/README.md)
[![en](https://img.shields.io/badge/lang-en-green.svg)](https://github.com/CSUC/RDR-scripts/blob/main/persistent_link/README_ENG.md)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CSUC/RDR-scripts/blob/main/persistent_link/extract_persistent_link.ipynb)
# Extracció d'Enllaços Persistents de Conjunts de Dades
# Extracting Persistent Links from Datasets

For any questions about the code, please contact rdr-contacte@csuc.cat

## Description

This Python script is designed to extract persistent links from files in datasets hosted on Dataverse. Persistent links are useful for consistently referencing specific data, even if the data is moved or updated in the future.

## Requirements

- Python 3.x
- Python Libraries: `pyDataverse`, `xlsxwriter`, `pandas`

## Usage

1. **Install Libraries**: Click the "Install Libraries" button to install or update the required libraries.

2. **Enter Information**: Provide the API token, dataset DOI, and repository URL.

3. **Run Script**: Click the play button to run the cell and extract the persistent links.

4. **Download Results**: An Excel file with the persistent links will be generated. You can download the file by clicking the provided link.

## File Structure
- `persistent_link.ipynb`: The main script to export metadata and generate the README file.
- `excel_name.xlsx`: The generated excel file named excel_name containing detailed information about the persistent links dataset.

## Usage Example
```python
# Set the DOI and token
doi = 'doi:10.34810/dataXXX'
token = 'el_teul_propi_token'

# Run the script
