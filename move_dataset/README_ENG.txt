### Move Dataset Script

For any queries regarding the code, contact rdr-contacte@csuc.cat.

## Script Objective

This script facilitates the movement of a dataset from one dataverse to another on Dataverse.

## Description

The script moves a dataset to a different dataverse using the provided DOI, API token, and target dataverse alias. It communicates with the Dataverse API to retrieve dataset information and perform the move operation. Upon completion, it provides feedback on the success or failure of the operation.

## Requirements

Ensure that the following libraries are installed:
- pyDataverse
- requests

## Usage

1. **Input Values:**
    - DOI: Enter the DOI of the dataset.
    - Token: Provide the API token for authentication.
    - Alias: Specify the alias of the target dataverse.

2. **Execution:**
    - Execute the script after providing the required input values.
    - The script will attempt to move the dataset to the specified dataverse.
    - It will display a success or failure message based on the outcome of the operation.
