# Script for Automatic File Upload

For any queries regarding the code, contact rdr-contacte@csuc.cat

## Script Objective

This script facilitates the automatic upload of files to a dataset on Dataverse using metadata provided in an Excel file.

## Script Overview

### Prerequisites
- Ensure that the script files and the files to be uploaded are located in the same directory.
- In Google Colab, upload the Excel file using the "Upload files" icon.

### Metadata Excel File Requirements
1. The first row serves as the header and must contain the following variable names in the specified order:
    - File Name
    - Description
    - File Path
    - Tag
2. Each subsequent row corresponds to a file to be uploaded.
3. The file name (File Name) is mandatory and must be written correctly, including the file extension.
4. Leave any cell blank if the corresponding information is not available.
5. If a metadata value contains a number, enclose it in quotes.
6. For the 'Tag' variable, if multiple tags are to be applied, separate them with a comma.

### Function Parameters
- `base_url`: Base URL of the Dataverse repository.
- `token`: API token for authentication.
- `doi`: DOI of the dataset.
- `excel_file_name`: Name of the Excel file containing metadata.

### Usage
- Execute the script by providing the required input values.
- The script will read metadata from the Excel file, verify file existence, and upload files to the dataset accordingly.
- Upon completion, the script will display messages indicating successful file uploads or any encountered errors.

