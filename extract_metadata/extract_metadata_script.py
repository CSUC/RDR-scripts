# ================== USER PARAMETERS ==================
token = ""         # <-- Your API token
identifier = ""    # <-- Last part of the DOI (e.g., "XYZ" from "doi:10.34810/dataXYZ")
base_url = "https://dataverse.csuc.cat/"
doi = 'doi:10.34810/data' + identifier

# ================== IMPORTS ==================
import os
import sys
import subprocess

def install_packages():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "-q"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyDataverse", "pandas", "openpyxl", "-q"])
    print("Libraries installed or updated.")

try:
    import pyDataverse
    import pandas as pd
    from pyDataverse.api import NativeApi, DataAccessApi
except ImportError:
    print("Installing required libraries...")
    install_packages()
    import pyDataverse
    import pandas as pd
    from pyDataverse.api import NativeApi, DataAccessApi

# ================== METADATA UTILITIES ==================
def extract_value(data_dict):
    if isinstance(data_dict, dict):
        type_names, values = [], []
        for key, value in data_dict.items():
            if key == 'typeName' and 'value' in data_dict:
                if isinstance(data_dict['value'], list):
                    for v in data_dict['value']:
                        type_names.append(data_dict['typeName'])
                        values.append(v)
                else:
                    type_names.append(data_dict['typeName'])
                    values.append(data_dict['value'])
            elif isinstance(value, dict) and 'typeName' in value and 'value' in value:
                type_names.append(value['typeName'])
                values.append(value['value'])
            elif isinstance(value, str) and key == 'typeName':
                type_names.append(value)
                values.append(value)
            else:
                sub_keys, sub_values = extract_value(value)
                type_names += sub_keys
                values += sub_values
        return type_names, values
    elif isinstance(data_dict, list):
        type_names, values = [], []
        for item in data_dict:
            sub_keys, sub_values = extract_value(item)
            type_names += sub_keys
            values += sub_values
        return type_names, values
    else:
        return [], []

def export_metadata(api, doi,
                    citation_keys, citation_values,
                    geo_keys, geo_values,
                    social_keys, social_values,
                    astronomy_keys, astronomy_values,
                    biomedical_keys, biomedical_values,
                    journal_keys, journal_values,
                    computationalworkflow_keys, computationalworkflow_values,
                    LocalContextsCVoc_keys, LocalContextsCVoc_values,
                    darwincore_keys, darwincore_values):

    metadata_blocks = [
        ("citation", citation_keys, citation_values),
        ("geospatial", geo_keys, geo_values),
        ("socialscience", social_keys, social_values),
        ("astrophysics", astronomy_keys, astronomy_values),
        ("biomedical", biomedical_keys, biomedical_values),
        ("journal", journal_keys, journal_values),
        ("computationalworkflow", computationalworkflow_keys, computationalworkflow_values),
        ("LocalContextsCVoc", LocalContextsCVoc_keys, LocalContextsCVoc_values),
        ("darwincore", darwincore_keys, darwincore_values)
    ]

    try:
        dataset = api.get_dataset(doi)
        metadata = dataset.json()['data']['latestVersion']['metadataBlocks']

        for block_name, keys_list, values_list in metadata_blocks:
            if block_name in metadata:
                fields = metadata[block_name]['fields']
                extracted_keys, extracted_values = extract_value(fields)
                keys_list.extend(extracted_keys)
                values_list.extend(extracted_values)
                for item in fields:
                    if isinstance(item.get('value'), str):
                        try:
                            index = keys_list.index(item['typeName'])
                            values_list[index] = item['value']
                        except ValueError:
                            pass
    except Exception as e:
        print(f"Error exporting metadata for DOI {doi}: {e}")
        raise

def extract_metadata(data,
                     citation_keys, citation_values,
                     geo_keys, geo_values,
                     social_keys, social_values,
                     astronomy_keys, astronomy_values,
                     biomedical_keys, biomedical_values,
                     journal_keys, journal_values,
                     computationalworkflow_keys, computationalworkflow_values,
                     LocalContextsCVoc_keys, LocalContextsCVoc_values,
                     darwincore_keys, darwincore_values):

    metadata_blocks = [
        (citation_keys, citation_values),
        (geo_keys, geo_values),
        (social_keys, social_values),
        (astronomy_keys, astronomy_values),
        (biomedical_keys, biomedical_values),
        (journal_keys, journal_values),
        (computationalworkflow_keys, computationalworkflow_values),
        (LocalContextsCVoc_keys, LocalContextsCVoc_values),
        (darwincore_keys, darwincore_values)
    ]

    for keys, values in metadata_blocks:
        for key, value in zip(keys, values):
            if not isinstance(value, dict):
                data.append([key, value])

# ================== MAIN SCRIPT ==================
if not token or not identifier:
    print("❗ Please provide both `token` and `identifier` at the top of the script.")
    sys.exit(1)

print("Connecting to Dataverse API...")
api = NativeApi(base_url, token)
data_api = DataAccessApi(base_url, token)
path = doi.replace("doi:10.34810/", "")

# Prepare key/value containers
citation_keys, geo_keys, social_keys, astronomy_keys, biomedical_keys, journal_keys, computationalworkflow_keys, LocalContextsCVoc_keys, darwincore_keys = [[] for _ in range(9)]
citation_values, geo_values, social_values, astronomy_values, biomedical_values, journal_values, computationalworkflow_values, LocalContextsCVoc_values, darwincore_values = [[] for _ in range(9)]

# Extract and organize metadata
print("Fetching metadata...")
export_metadata(api, doi,
                citation_keys, citation_values,
                geo_keys, geo_values,
                social_keys, social_values,
                astronomy_keys, astronomy_values,
                biomedical_keys, biomedical_values,
                journal_keys, journal_values,
                computationalworkflow_keys, computationalworkflow_values,
                LocalContextsCVoc_keys, LocalContextsCVoc_values,
                darwincore_keys, darwincore_values)

# Flatten metadata into tabular format
data = []
extract_metadata(data,
                 citation_keys, citation_values,
                 geo_keys, geo_values,
                 social_keys, social_values,
                 astronomy_keys, astronomy_values,
                 biomedical_keys, biomedical_values,
                 journal_keys, journal_values,
                 computationalworkflow_keys, computationalworkflow_values,
                 LocalContextsCVoc_keys, LocalContextsCVoc_values,
                 darwincore_keys, darwincore_values)

# Save to CSV and Excel
df = pd.DataFrame(data, columns=['Metadata', 'Value'])
csv_file = path + '_metadata.csv'
excel_file = path + '_metadata.xlsx'

df.to_csv(csv_file, index=False)
df.to_excel(excel_file, index=False)

print(f" Metadata exported to:\n  📄 {csv_file}\n   {excel_file}")
