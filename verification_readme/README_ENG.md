[![ca](https://img.shields.io/badge/lang-ca-blue.svg)](https://github.com/CSUC/RDR-scripts/blob/main/verification_readme/README.md)
[![en](https://img.shields.io/badge/lang-en-green.svg)](https://github.com/CSUC/RDR-scripts/blob/main/verification_readme/README_ENG.md)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CSUC/RDR-scripts/blob/main/verification_readme/verification_readme_script.ipynb)

# Script to Check if Datasets Contain a Readme File

This script automatically checks whether datasets from a given Dataverse institution contain a file with “Readme” in its name, and exports this information to an Excel file. It also indicates whether the dataset is published or in draft status.

## Purpose

The main goal is to help identify datasets that meet the basic documentation requirement by including a `Readme` file — essential for data quality and understanding.

## Requirements

The script uses the following Python libraries:

- `pandas`
- `IPython.display` (for displaying tables and downloading files in Colab)
- `google.colab` (optional, for managing file download in Colab)
- Predefined configuration using the API, institution aliases, `base_url`, and `token`

## Usage Instructions

1. **Run the script in Google Colab:**
   - The script is designed for execution in Google Colab. Just copy and run the code cell by cell.

2. **Select the institution(s):**
   - Specify one or more institutions from the `options` list.

3. **Run the check:**
   - The script will iterate over all datasets from each institution and check for the presence of a `Readme` file.

4. **Download the results:**
   - An Excel file named `datasets_sizes.xlsx` will be generated and can be downloaded from Colab.

## Excel File Structure

The generated Excel file includes the following columns:

- **DOI:** Persistent link to the dataset.
- **Published:** Indicates if the dataset is published (`Published`) or in draft (`Draft`).
- **Institution:** Alias of the institution analyzed.
- **Is there Readme?:** Yes (`Yes`) if a file containing "readme" was found, No (`No`) otherwise.
- **Readme file name:** The name(s) of the detected `Readme` file(s).

## Example Output

| DOI                                  | Published | Institution | Is there Readme? | Readme file name    |
|-------------------------------------|-----------|-------------|------------------|----------------------|
| https://doi.org/10.34810/data1234   | Published | upf         | Yes              | readme_dataset.txt   |
| https://doi.org/10.34810/data1235   | Draft     | udl         | No               |                      |

## Notes

- The script performs a case-insensitive search for the word `readme` in file names.
- Draft datasets are also included in the analysis.

## Author

Script developed by [CSUC](https://www.csuc.cat/) as part of maintenance and validation scripts for Dataverse-based research data repositories.

---
