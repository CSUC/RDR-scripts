# import requests
import pandas as pd
from pyDataverse.api import NativeApi

# ============================================================
# Configuration
# ============================================================

API_TOKEN = ""
BASE_URL = "https://dataverse.csuc.cat"
DOI = "doi:10.34810/data"

headers = {
    "X-Dataverse-key": API_TOKEN
}

api = NativeApi(BASE_URL, API_TOKEN)


# ============================================================
# Get dataset file metadata
# ============================================================

def get_all_file_metadata(api, doi):

    response = api.get_dataset(doi)
    response.raise_for_status()

    files = response.json()["data"]["latestVersion"]["files"]

    rows = []

    for f in files:

        data_file = f.get("dataFile", {})

        rows.append({
            "id": data_file.get("id"),
            "filename": data_file.get("filename"),
            "directoryLabel": f.get("directoryLabel", "")
        })

    return pd.DataFrame(rows)


# ============================================================
# Show menu and let user choose
# ============================================================

def choose_files_to_delete(df_files):

    folders = sorted(
        folder
        for folder in df_files["directoryLabel"].fillna("").unique()
        if folder != ""
    )

    print("\n========================================")
    print("DELETE OPTIONS")
    print("========================================")

    print("0 - ALL files in dataset")

    for i, folder in enumerate(folders, start=1):

        count = len(
            df_files[
                df_files["directoryLabel"].fillna("").apply(
                    lambda x:
                    x == folder or x.startswith(folder + "/")
                )
            ]
        )

        print(f"{i} - {folder} ({count} files)")

    choice = input("\nSelect an option number: ").strip()

    # --------------------------------------------------------
    # Delete ALL files
    # --------------------------------------------------------

    if choice == "0":

        return df_files.copy(), "ALL DATASET FILES"

    # --------------------------------------------------------
    # Validate input
    # --------------------------------------------------------

    if not choice.isdigit():

        print("\nInvalid option. Operation cancelled.")
        return None, None

    choice_num = int(choice)

    if choice_num < 1 or choice_num > len(folders):

        print("\nInvalid option. Operation cancelled.")
        return None, None

    # --------------------------------------------------------
    # Selected folder
    # --------------------------------------------------------

    selected_folder = folders[choice_num - 1]

    selected_files = df_files[
        df_files["directoryLabel"].fillna("").apply(
            lambda x:
            x == selected_folder or x.startswith(selected_folder + "/")
        )
    ].copy()

    return selected_files, selected_folder


# ============================================================
# MAIN
# ============================================================

print("\nLoading dataset metadata...")

df_files = get_all_file_metadata(api, DOI)

# ------------------------------------------------------------
# Check if dataset has files
# ------------------------------------------------------------

if df_files.empty:

    print("\nNo files found in dataset.")
    exit()

print(f"\nFound {len(df_files)} files in dataset.")

# ------------------------------------------------------------
# Ask user what to delete
# ------------------------------------------------------------

df_to_delete, selected_target = choose_files_to_delete(df_files)

if df_to_delete is None:

    exit()

# ------------------------------------------------------------
# Show selected files
# ------------------------------------------------------------

print("\n========================================")
print("SELECTED TARGET")
print("========================================")

print(selected_target)

print(f"\nFiles selected: {len(df_to_delete)}\n")

print(
    df_to_delete[
        ["id", "filename", "directoryLabel"]
    ].to_string(index=False)
)

# ------------------------------------------------------------
# Confirmation
# ------------------------------------------------------------

confirm = input(
    "\nWARNING: This operation will permanently delete "
    "the files listed above.\n"
    "Type exactly 'Yes' to continue or 'No' to cancel the operation: "
).strip()

# ------------------------------------------------------------
# Cancel safely
# ------------------------------------------------------------

if confirm != "Yes":

    print("\nOperation cancelled. No files were deleted.")

# ------------------------------------------------------------
# Execute deletion
# ------------------------------------------------------------

else:

    print("\n========================================")
    print("STARTING DELETION")
    print("========================================\n")

    deleted_count = 0
    failed_ids = []

    for file_id in df_to_delete["id"].dropna().astype(int):

        url = f"{BASE_URL}/api/files/{file_id}"

        print(f"Deleting file with id={file_id} ...")

        try:

            response = requests.delete(
                url,
                headers=headers
            )

            if response.status_code == 200:

                print(f"Deleted file {file_id}")

                deleted_count += 1

            else:

                print(
                    f"Failed to delete file {file_id} "
                    f"(HTTP {response.status_code})"
                )

                print(response.text)

                failed_ids.append(
                    (
                        file_id,
                        response.status_code,
                        response.text
                    )
                )

        except Exception as e:

            print(f"Error deleting file {file_id}: {e}")

            failed_ids.append(
                (
                    file_id,
                    "Exception",
                    str(e)
                )
            )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print("\n========================================")
    print("SUMMARY")
    print("========================================")

    print(
        f"\nDeleted {deleted_count}/"
        f"{len(df_to_delete)} files."
    )

    if failed_ids:

        print("\nFailed deletions:\n")

        for fid, status, msg in failed_ids:

            print(
                f" - ID {fid} | "
                f"status: {status}"
            )

    else:

        print("\nAll selected files were deleted successfully.")