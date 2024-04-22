# Tranform Excel format file to CSV format

For any queries regarding the code, contact rdr-contacte@csuc.cat 

## Overview
This script is designed to convert Excel files to CSV format. It allows users to upload an Excel file (.xlsx), which is then processed to generate CSV files for each sheet in the Excel workbook. The script offers options to separate tables in each sheet into different CSV files or convert each sheet into a single CSV file.

## Requirements
- Python 3.x
- pandas library
- ipywidgets library
- Google Colab (for interactive use)

## Usage
1. **Upload Excel File**: 
    - Click on the "Upload" button to select an Excel file (.xlsx) for conversion.

2. **Process Excel File**:
    - If prompted, choose whether to separate tables in each sheet into different CSV files.
    - Click on "Process Excel" to start the conversion process.

3. **Download CSV Files**:
    - Once the conversion is complete, a zip file containing the CSV files will be automatically downloaded.

## File Structure
- `Excel_to_CSV_Converter.ipynb`: The main script for converting Excel files to CSV format.
- `example.xlsx`: Example Excel file for testing purposes.
- `example_output.zip`: Example output containing the generated CSV files.

## Usage Example
```python
# Run the script and follow the instructions to upload an Excel file.
# Choose whether to separate tables in each sheet into different CSV files.
# The script will convert the Excel file to CSV format and download the generated files.
