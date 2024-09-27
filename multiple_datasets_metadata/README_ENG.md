# Extract metadata from multiple datasets of an institution

This script processes and aggregates metadata from various institutions and categories such as citations, geospatial metadata, social, astronomical, biomedical, journal, and others. The results are exported to an Excel file that can be downloaded automatically.

## Description
The script allows the selection of one or more institutions and metadata categories to process data corresponding to datasets associated with these institutions. Once the data is processed, it aggregates the metadata and exports it in an Excel format, with metadata associated with their DOI identifiers.

## Requirements
- Python 3.x
- `ipywidgets` library
- `pandas` library
- `openpyxl` library
- Google Colab (for interactive use)

## Usage

1. **Load Institutions and Metadata**:
    - Select one or more institutions and metadata categories (citations, geospatial, social, etc.) using the interactive widgets.

2. **Process Metadata**:
    - The script will process the data for each dataset of the selected institutions and aggregate the metadata corresponding to their DOI.

3. **Generate an Excel File**:
    - Once processing is complete, the script will create an Excel file with DOIs, institutions, and selected metadata. The file can be downloaded automatically.

## File Structure

- `metadata_processor.ipynb`: The main script to process and aggregate metadata.
- `estudi_metadades.xlsx`: The Excel file generated with the processed data.

## Example Usage
```python
# Run the script in Google Colab and follow the instructions to select institutions and metadata.
# The script will generate an Excel file with the processed data and automatically download it.
