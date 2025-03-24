[![ca](https://img.shields.io/badge/lang-ca-blue.svg)](https://github.com/CSUC/RDR-scripts/blob/main/dataset_size_calculator/README.md) 
[![en](https://img.shields.io/badge/lang-en-green.svg)](https://github.com/CSUC/RDR-scripts/blob/main/dataset_size_calculator/README_ENG.md)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CSUC/RDR-scripts/blob/main/dataset_size_calculator/dataset_size_calculator.ipynb)
# Script to Calculate Datasets Size of dataverses in Dataverse  
For any inquiries about the code, contact rdr-contacte@csuc.cat  

## Description  
This script calculates the total size of a datasets hosted in a dataverse in the Research Data Repository (https://dataverse.csuc.cat/). It uses the Dataverse API to retrieve the size of all files associated with all datasets of a dataverse and returns the total size in bytes, KB, MB, or GB.  

## Requirements  
- Python 3.x  
- `requests` library to make API calls to Dataverse  

## Usage  

1. **Input Parameters**:  
    - Token: Authentication token to access the Dataverse repository.  

2. **Configuration**:  
    - Specify the base URL of the Dataverse instance.  
    - Provide the dataset DOI and the authentication token.  

3. **Obtaining the Dataset Size**:  
    - Retrieve information about all files size associated with the datasets.  
    - Sum the size of each file to get the total datasets size.  

4. **Output Format**:  
    - Displays the total size in different units (bytes, KB, MB, GB) for easier interpretation.  

5. **Download Options**:  
    - If running in Google Colab, you can download a report with the datasets size.  
    - It can also be run in other Python environments such as Jupyter Notebook or locally.  

## File Structure  
- `dataset_size_calculator.ipynb`: Script to calculate the datasetS size.  
- `README.md`: Documentation file for the script.  

## Example Usage  

# Set token
token = 'XXX-XXXX-XXXXX-XXXXX'

# Run the function to calculate the size
The script generates an Excel file named `mida_datasets.xlsx` containing the following information:

| DOI  | Institution          | Original Size (Bytes) | Archival Size (Bytes) | Formatted Original Size | Unit (Original Size) | Formatted Archival Size | Unit (Archival Size) |
|------|----------------------|----------------------|----------------------|------------------------|----------------------|------------------------|----------------------|
| doi1 | Example Institution | 1024000             | 512000               | 1.00                   | MB                   | 500.00                 | KB                   |
| doi2 | Example Institution | 598424             | 896771               | 584.4                  | KB                   | 875.75                 | KB                   |


Where:

- **Original Size (Bytes)**: is the size in bytes of the dataset's files in their original format.
- **Archival Size (Bytes)**: is the size in bytes of the dataset's files in their transformed format during ingestion.
- **Formatted Original Size**: is the size of the dataset's files in their original format with the unit of measurement indicated in *Unit (Original Size)*.
- **Formatted Archival Size**: is the size of the dataset's files in their transformed format during ingestion with the unit of measurement indicated in *Unit (Archival Size)*.
