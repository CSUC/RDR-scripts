# Replace files in Dataverse

import os
import json
import requests
import hashlib
from pyDataverse.api import NativeApi


# ============================================================
# CONFIGURATION
# ============================================================

API_TOKEN = ""
identifier = ""
SERVER_URL = ""
FOLDER_PATH = ""


# Formats that Dataverse may ingest and convert to .tab
TABULAR_EXTENSIONS = {
    ".xlsx",
    ".xls",
    ".csv",
    ".tsv",
    ".sav",
    ".por",
    ".dta",
    ".rdata",
    ".rda"
}


# ============================================================
# GET FILE METADATA FROM DATAVERSE
# ============================================================

def get_dataverse_files(server_url, api_token, doi):

    api = NativeApi(server_url, api_token)

    try:
        dataset = api.get_dataset(doi)

        if dataset.status_code != 200:
            try:
                message = dataset.json().get("message", "Unknown error")
            except Exception:
                message = dataset.text

            print(f"❌ Error retrieving dataset: {message}")
            return []

        files = (
            dataset.json()
            .get("data", {})
            .get("latestVersion", {})
            .get("files", [])
        )

        file_metadata = []

        for file_entry in files:

            data_file = file_entry.get("dataFile", {}).copy()

            # These metadata fields are outside dataFile
            data_file["description"] = file_entry.get(
                "description", ""
            )

            data_file["directoryLabel"] = file_entry.get(
                "directoryLabel", ""
            )

            data_file["categories"] = file_entry.get(
                "categories", []
            )

            file_metadata.append(data_file)

        return file_metadata

    except Exception as e:
        print(f"❌ Error retrieving dataset: {e}")
        return []


# ============================================================
# GET DATAVERSE FILES
# ============================================================

dataverse_files = get_dataverse_files(
    SERVER_URL,
    API_TOKEN,
    identifier
)


# Create filename lookup dictionary
metadata_dict = {}

for metadata in dataverse_files:

    filename = metadata.get("filename")

    if filename:
        metadata_dict[filename] = metadata


# ============================================================
# FIND LOCAL FILES
# ============================================================

def get_all_files(folder_path):

    file_list = []

    for root, _, files in os.walk(folder_path):

        for filename in files:

            file_list.append(
                os.path.join(root, filename)
            )

    return file_list


# ============================================================
# FIND MATCHING DATAVERSE FILE
# ============================================================

def find_dataverse_file(local_filename, metadata_dict):

    # First try exact filename
    if local_filename in metadata_dict:

        return (
            metadata_dict[local_filename],
            "exact"
        )

    # If it is a tabular format, try the .tab version
    base_name, extension = os.path.splitext(local_filename)

    extension = extension.lower()

    if extension in TABULAR_EXTENSIONS:

        tab_filename = base_name + ".tab"

        if tab_filename in metadata_dict:

            return (
                metadata_dict[tab_filename],
                "ingested"
            )

    return None, None


# ============================================================
# CHECKSUM
# ============================================================

def compute_file_hash(file_path, algorithm):

    algorithms = {
        "MD5": hashlib.md5,
        "SHA-1": hashlib.sha1,
        "SHA-256": hashlib.sha256,
        "SHA-512": hashlib.sha512
    }

    hash_function = algorithms.get(
        algorithm.upper()
    )

    if hash_function is None:
        return None

    hasher = hash_function()

    with open(file_path, "rb") as f:

        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b""
        ):
            hasher.update(chunk)

    return hasher.hexdigest()


# ============================================================
# PROCESS FILES
# ============================================================

files_to_upload = get_all_files(FOLDER_PATH)

if not files_to_upload:

    print(
        f"⚠️ No files found in folder: {FOLDER_PATH}"
    )


for file_path in files_to_upload:

    local_filename = os.path.basename(file_path)

    file_metadata, match_type = find_dataverse_file(
        local_filename,
        metadata_dict
    )


    # --------------------------------------------------------
    # NO MATCH
    # --------------------------------------------------------

    if file_metadata is None:

        print(
            f"⚠️ Not replaced (no matching file): "
            f"{local_filename}"
        )

        continue


    # --------------------------------------------------------
    # GET DATAVERSE FILE ID
    # --------------------------------------------------------

    file_id = file_metadata.get("id")

    if file_id is None:

        print(
            f"❌ Error replacing {local_filename}: "
            f"Dataverse file ID not found."
        )

        continue


    # --------------------------------------------------------
    # CHECK IF EXACT-MATCH FILE IS IDENTICAL
    #
    # We don't compare hashes for .xlsx -> .tab etc.
    # because the .tab checksum represents a different file.
    # --------------------------------------------------------

    if match_type == "exact":

        checksum = file_metadata.get(
            "checksum",
            {}
        )

        checksum_type = checksum.get("type")
        existing_checksum = checksum.get("value")

        if checksum_type and existing_checksum:

            new_checksum = compute_file_hash(
                file_path,
                checksum_type
            )

            if (
                new_checksum
                and new_checksum.lower()
                == existing_checksum.lower()
            ):

                print(
                    f"⏭️ Not replaced (identical): "
                    f"{local_filename}"
                )

                continue


    # --------------------------------------------------------
    # METADATA TO PRESERVE
    # --------------------------------------------------------

    json_data = {
        "description": file_metadata.get(
            "description", ""
        ),
        "directoryLabel": file_metadata.get(
            "directoryLabel", ""
        ),
        "categories": file_metadata.get(
            "categories", []
        ),
        "forceReplace": True
    }


    # --------------------------------------------------------
    # REPLACE FILE
    # --------------------------------------------------------

    url = (
        f"{SERVER_URL}/api/files/"
        f"{file_id}/replace"
    )

    headers = {
        "X-Dataverse-key": API_TOKEN
    }


    try:

        with open(file_path, "rb") as file:

            files = {
                "file": (
                    local_filename,
                    file
                )
            }

            data = {
                "jsonData": json.dumps(json_data)
            }

            response = requests.post(
                url,
                headers=headers,
                files=files,
                data=data,
                timeout=300
            )


        # Try reading Dataverse response
        try:
            response_json = response.json()

        except ValueError:

            print(
                f"❌ Error replacing {local_filename}: "
                f"HTTP {response.status_code} - "
                f"{response.text[:300]}"
            )

            continue


        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        if (
            response.status_code == 200
            and response_json.get("status") == "OK"
        ):

            print(
                f"✅ Replaced: {local_filename}"
            )


        # ----------------------------------------------------
        # ERROR
        # ----------------------------------------------------

        else:

            message = response_json.get("message")

            if not message:

                response_data = response_json.get(
                    "data",
                    {}
                )

                if isinstance(response_data, dict):
                    message = response_data.get("message")

            if not message:
                message = str(response_json)

            print(
                f"❌ Error replacing {local_filename}: "
                f"{message}"
            )


    except requests.RequestException as e:

        print(
            f"❌ Error replacing {local_filename}: {e}"
        )


    except Exception as e:

        print(
            f"❌ Error replacing {local_filename}: {e}"
        )
