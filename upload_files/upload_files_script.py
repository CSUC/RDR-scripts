# ======================== PARAMETERS ========================
IDENTIFIER = "123"  # Last digits of DOI, e.g., '123'
TOKEN = "your-api-token-here"  # Your Dataverse API token
EXCEL_FILE_NAME = "metadata.xlsx"  # Your Excel metadata file
BASE_URL = "https://dataverse.csuc.cat/"  # Repository base URL
# ============================================================

# Construct DOI
DOI = "doi:10.34810/data" + IDENTIFIER

# ========== Install required packages if needed ==========
import subprocess
import sys

def install_packages():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyDataverse"])

try:
    import pyDataverse
except ImportError:
    print("Installing required packages...")
    install_packages()

# ========== Imports ==========
import os
from pathlib import Path
import pandas as pd
from pyDataverse.api import NativeApi, DataAccessApi
from pyDataverse.models import Datafile

# ========== API Initialization ==========
api = NativeApi(BASE_URL, TOKEN)
data_api = DataAccessApi(BASE_URL, TOKEN)

# ========== File Upload Function ==========
def upload_files(base_url, token, doi, excel_file_name):
    try:
        files_metadata = pd.read_excel(excel_file_name).to_numpy().tolist()
        all_exist = True
        for row in files_metadata:
            file_path = Path(row[0])
            if not file_path.is_file():
                print(" File not found:", row[0])
                all_exist = False
        if not all_exist:
            print("⚠ Some files are missing. Please check paths.")
            return

        dataset = api.get_dataset(doi)
        for row in files_metadata:
            file_name = row[0]
            df = Datafile()
            df.set({"pid": doi, "filename": file_name})
            if not pd.isna(row[1]):
                df.set({"description": row[1]})
            if not pd.isna(row[2]):
                df.set({"directoryLabel": row[2]})
            if not pd.isna(row[3]):
                df.set({"categories": [cat.strip() for cat in row[3].split(",")]})
            resp = api.upload_datafile(doi, file_name, df.json())
            print(" Uploaded:", file_name)
    except FileNotFoundError:
        print(" Metadata file not found:", excel_file_name)
    except Exception as e:
        print(" Upload failed:", e)

# ========== Run Upload ==========
upload_files(BASE_URL, TOKEN, DOI, EXCEL_FILE_NAME)

# ========== Get File Metadata ==========
def filemetadata(base_url, token, doi, keys_out, values_out):
    try:
        dataset = api.get_dataset(doi)
        files = dataset.json()["data"]["latestVersion"]["files"]
        for file in files:
            filemeta = file["dataFile"]
            keys_out.append(list(filemeta.keys()))
            values_out.append(list(filemeta.values()))
    except KeyError:
        print(" Error reading file metadata for dataset:", doi)

filemetadata_keys = []
filemetadata_values = []
filemetadata(BASE_URL, TOKEN, DOI, filemetadata_keys, filemetadata_values)

# ========== File Size Calculation ==========
def format_size(bytes_size):
    units = ["Bytes", "KB", "MB", "GB", "TB"]
    size = float(bytes_size)
    idx = 0
    while size >= 1024 and idx < len(units) - 1:
        size /= 1024
        idx += 1
    return f"{size:.2f} {units[idx]}"

def get_index(key_list, key):
    return key_list.index(key) if key in key_list else None

def get_size(entry, keys):
    orig_idx = get_index(keys, "originalFileSize")
    file_idx = get_index(keys, "filesize")
    if orig_idx is not None and isinstance(entry[orig_idx], int):
        return entry[orig_idx]
    elif file_idx is not None:
        return entry[file_idx]
    return 0

filesize_index = get_index(filemetadata_keys[0], "filesize")
sizes = [get_size(entry, filemetadata_keys[i]) for i, entry in enumerate(filemetadata_values)]

total_original_size_bytes = sum(sizes)
total_archival_size_bytes = sum(entry[filesize_index] for entry in filemetadata_values if isinstance(entry[filesize_index], int))

print("\n Total original format dataset size:", format_size(total_original_size_bytes))
print(" Total archival format dataset size:", format_size(total_archival_size_bytes))
