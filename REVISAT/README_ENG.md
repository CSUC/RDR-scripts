[![ca](https://img.shields.io/badge/lang-ca-blue.svg)](https://github.com/CSUC/RDR-scripts/blob/main/REVISAT/README.md)
[![en](https://img.shields.io/badge/lang-en-green.svg)](https://github.com/CSUC/RDR-scripts/blob/main/REVISAT/README_ENG.md)
# Dataset Evaluation Script (REVISAT / CURATED)
For any queries regarding the code, contact rdr-contacte@csuc.cat

## Script Objective
This script allows users to evaluate a dataset before publication to ensure compliance with open access best practices. It performs various checks and evaluations on the dataset metadata and content. Below is a detailed guide on how to use the script and its functionalities.

## Script Overview

The script performs the following checks and evaluations on the dataset:

1. **Minimum Metadata Requirements:**
    - Validates whether the dataset contains the minimum required metadata fields.
    - Displays if the dataset contains all mandatory metadata fields.

2. **Title and Related Publication:**
    - Verifies the title of the dataset.
    - Checks if the dataset has any related publication and ensures that the publication citation is included.
    - Compares the title of the dataset with the related publication title if applicable.

3. **Authors' Affiliation and ORCID:**
    - Checks if at least one author is affiliated with the specified institution.
    - Determines if at least one author provides their ORCID.

4. **Description:**
    - Displays the dataset description.

5. **File Formats:**
    - Counts the occurrences of different file extensions in the dataset.
    - Checks if the dataset contains a `readme.txt` file.

6. **License:**
    - Displays the dataset license or terms of use.

7. **F-UJI Evaluation (Optional):**
    - If specified, the script can open F-UJI (Fair Use and Justification for Use of Infrastructures) for manual evaluation of the dataset.

## Instructions

1. **Input Values:**
    - **DOI (Dataset Identifier):** Enter the DOI of the dataset.
    - **Token (API Token):** Provide the API token for authentication.
    - **Institution:** Enter the full name of the institution where the dataset is hosted.
    - **WebDriver (Optional):** Choose a WebDriver (e.g., Chrome or Firefox) if evaluating the dataset on F-UJI.

2. **Execution:**
    - Execute the script after providing the required input values.
    - The script will perform checks and evaluations on the dataset.

3. **Interpreting Results:**
    - Review the output of each check to ensure compliance with open access best practices.

