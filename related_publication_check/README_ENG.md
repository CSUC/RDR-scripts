[![ca](https://img.shields.io/badge/lang-ca-blue.svg)](https://github.com/CSUC/RDR-scripts/blob/main/related_publication_check/README.md)
[![en](https://img.shields.io/badge/lang-en-green.svg)](https://github.com/CSUC/RDR-scripts/blob/main/related_publication_check/README_ENG.md)
# Script for Generating Metadata for Publications (Related Publication Study)
For any inquiries regarding the code, please contact rdr-contacte@csuc.cat

## Objective of the Script

This script allows users to assess and generate a metadata dashboard related to publications associated with datasets. The goal is to extract and aggregate specific metadata for each dataset for later visualization and analysis in an Excel file. Below is a detailed guide on how to use the script and its features.

## Description of the Script

The script performs the following tasks:

1. **Metadata Extraction:**
    - Extracts specific metadata (such as publication relation type, publication citation, publication ID, etc.) from various datasets using the API.
    - Filters the metadata based on the options selected by the user.

2. **Metadata Aggregation:**
    - Aggregates metadata by DOI to combine values associated with each dataset.
    - Ensures that values for each DOI are properly formatted and displayed as concatenated lists when they repeat.

3. **Metadata Dashboard Creation:**
    - Creates a DataFrame from the aggregated metadata, showing the selected metadata and the institutions associated with each DOI.
    - Sorts the results by DOI and formats the DOI links for display.

4. **Export to Excel:**
    - Once the metadata dashboard is generated, the script saves the data into an Excel file for easier reference and further use.

## Instructions

1. **Input Values:**
    - **Metadata Options:** Select the metadata fields you wish to extract (e.g., `publicationRelationType`, `publicationCitation`, etc.).
    - **DOIs and Institutions:** The script will obtain the data from the institutions and DOIs associated with the datasets.

2. **Execution:**
    - Run the script after providing the metadata options and the list of datasets.
    - The script will perform metadata filtering and aggregation to create the dashboard.

3. **Download the Excel File:**
    - Once the dashboard is generated, the script will provide a link to download the Excel file containing the generated metadata.

4. **Excel File Format:**
    - The file will contain the following columns: DOI, Institution, and the selected metadata fields.

## Example Output

| DOI                                | Institution | publicationRelationType | publicationCitation | publicationIDType | publicationIDNumber | publicationURL |
|------------------------------------|-------------|-------------------------|---------------------|--------------------|----------------------|----------------|
| https://doi.org/10.34810/dataXXX   | UB          | ...                     | ...                 | ...                | ...                  | ...            |
| https://doi.org/10.34810/dataXXX   | UAB         | ...                     | ...                 | ...                | ...                  | ...            |

## Limitations and Considerations

- The script relies on the data provided by the datasets associated with the DOIs.
- It may be necessary to adapt the script if additional metadata fields need to be selected that are not initially included.

For any questions or issues related to the process, please contact the script maintainer.
