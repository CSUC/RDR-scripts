[![ca](https://img.shields.io/badge/lang-ca-blue.svg)](https://github.com/CSUC/RDR-scripts/blob/main/metrics/README.md)
[![en](https://img.shields.io/badge/lang-en-green.svg)](https://github.com/CSUC/RDR-scripts/blob/main/metrics/README_ENG.md)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CSUC/RDR-scripts/blob/main/metrics/metrics_script.ipynb)

# Script to Extract Metrics from Datasets in a Dataverse Instance

This script allows you to extract metrics from datasets in a Dataverse instance using the Dataverse API. The metrics include total views, unique views, total downloads, unique downloads, and citations.

## Objective

The main objective is to simplify the process of obtaining metrics from datasets in a specific Dataverse instance. The data can be exported to an Excel file for further analysis.

## Requirements

This script requires the following libraries:

- `pyDataverse`
- `numpy`
- `pandas`
- `openpyxl`
- `requests`

Additionally, you need to have an account with sufficient permissions on the Dataverse instance and a private token to access the API.

## Instructions

1. **Run the Script in Google Colab:**
   - The script is prepared to be executed in Google Colab. Copy the code into a Google Colab cell and follow the instructions in the markdown and code cells.

2. **Install the Necessary Libraries:**
   - Run the cell titled *"Install or Update Libraries"*. This will install all required dependencies.

3. **Enter the Token and Institution Alias:**
   - Provide your private token and the institution alias when prompted.

4. **Execute the Metric Extraction:**
   - Run the corresponding cells to extract the metrics from the datasets.

5. **Save the Metrics to an Excel File:**
   - The script generates an Excel file with the extracted metrics. Run the final cell to download the file to your computer.

## Excel File Structure

The Excel file will have the following columns:

- **DOI:** Persistent identifier of the dataset.
- **Total Views:** Total views of the dataset.
- **Unique Views:** Total unique views of the dataset.
- **Total Downloads:** Total downloads of the dataset.
- **Unique Downloads:** Total unique downloads of the dataset.
- **Citations:** Total number of citations.

## Usage Examples

### Obtaining Metrics

1. Enter the institution alias and token:
