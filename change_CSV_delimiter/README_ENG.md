# CSV Delimiter Converter

For any queries regarding the code, contact [rdr-contacte@csuc.cat](mailto:rdr-contacte@csuc.cat)

## Overview
This script is designed to convert semicolon-separated CSV files to comma-separated CSV files. It allows users to upload one or multiple semicolon-separated CSV files, which are then processed and saved with comma delimiters. The processed files are zipped together and made available for download.

## Requirements
- Python 3.x
- ipywidgets library
- Google Colab (for interactive use)

## Usage
1. **Upload CSV Files**:
    - Click on the "Upload" button to select one or more semicolon-separated CSV files for conversion.

2. **Process CSV Files**:
    - The script will automatically convert the uploaded files to comma-separated CSV format.
    - Each processed file will be saved with a `_new.csv` suffix.

3. **Download Processed Files**:
    - Once the conversion is complete, a zip file containing all the processed CSV files will be automatically downloaded.

## File Structure
- `csv_delimiter_converter.ipynb`: The main script for converting CSV files from semicolon to comma delimiter.
- `example_semicolon.csv`: Example semicolon-separated CSV file for testing purposes.
- `processed_csv_files.zip`: Example output containing the generated comma-separated CSV files.

## Usage Example
```python
# Run the script and follow the instructions to upload semicolon-separated CSV files.
# The script will convert each uploaded file to comma-separated format and download the generated files as a zip archive.
