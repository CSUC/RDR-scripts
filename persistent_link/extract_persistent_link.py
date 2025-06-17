"""
Script to extract file-level metadata from a Dataverse dataset and export it to Excel.
Dependencies (install manually if needed):
- pyDataverse
- pandas
- xlsxwriter
- httpx>=0.28.1,<1.0.0
"""

# ---------- USER PARAMETERS ----------
token = ""  # API token
identifier = ""  # e.g., "doi:10.34810/dataXXX"
base_url = "https://dataverse.csuc.cat/"  # Repository URL
# -------------------------------------

import os
import pandas as pd
from pyDataverse.api import NativeApi, DataAccessApi

# Validate DOI
doi = identifier.strip()

# API clients
api = NativeApi(base_url, token)
data_api = DataAccessApi(base_url, token)

def filemetadata(base_url, token, doi, filemetadata_keys, filemetadata_values):
    """
    Extract file-level metadata from a Dataverse dataset by DOI.
    """
    api = NativeApi(base_url, token)
    data_api = DataAccessApi(base_url, token)

    try:
        dataset = api.get_dataset(doi)
        files = dataset.json()['data']['latestVersion']['files']

        for file_entry in files:
            data_file = file_entry['dataFile']
            filemetadata_keys.append(list(data_file.keys()))
            filemetadata_values.append(list(data_file.values()))

    except KeyError:
        print(f"Error reading metadata for dataset files: {doi}")

# Collect file metadata
filemetadata_keys_one = []
filemetadata_values_one = []
filemetadata(base_url, token, doi, filemetadata_keys_one, filemetadata_values_one)

# Create a DataFrame from extracted file metadata
data = []
for values in filemetadata_values_one:
    file_id = values[0]
    filename = values[2]
    persistent_link = f"{base_url.rstrip('/')}/file.xhtml?fileId={file_id}"
    data.append({'Persistent Link': persistent_link, 'Filename': filename})

df = pd.DataFrame(data)

# Generate Excel file
excel_name = doi.split("/")[-1] + '.xlsx'
with pd.ExcelWriter(excel_name, engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name=doi.split("/")[-1], index=False)

print(f"Metadata saved to: {excel_name}")
