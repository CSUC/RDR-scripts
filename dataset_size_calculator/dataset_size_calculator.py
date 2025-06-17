import os
import subprocess
import sys
import logging
import requests
import pandas as pd
from pyDataverse.api import NativeApi, DataAccessApi

# ========== SETUP ==========

# Ensure required package is installed
try:
    import pyDataverse
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyDataverse"])

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== CONFIGURATION CLASSES ==========

class Config:
    def __init__(self, api_url, logger, token):
        self.api_url = api_url
        self.logger = logger
        self.token = token

    def get_api_url(self): return self.api_url
    def get_logger(self): return self.logger
    def get_token(self): return self.token

class UtilsConnection:
    def __init__(self, config):
        self.config = config

    def call_api(self, url, method="GET", data=None):
        headers = {'X-Dataverse-key': self.config.get_token()}
        response = requests.request(method, url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()

class DatasetProcessor:
    def __init__(self, config, identifier):
        self.config = config
        self.identifier = identifier
        self.datasets = []
        self.children = []

    def create_list_datasets(self, identifier):
        conn = UtilsConnection(self.config)
        url_api = f"{self.config.get_api_url()}/api/dataverses/{identifier}/contents"
        response = conn.call_api(url_api, "GET")

        if response:
            logger.info("Fetching datasets...")
            for item in response.get("data", []):
                if item['type'] == 'dataverse':
                    self.children.append(item['id'])
                elif item['type'] == 'dataset' and item['protocol'] == 'doi':
                    doi = f"{item['protocol']}:{item['authority']}/{item['identifier']}"
                    self.datasets.append(doi)

        if identifier != self.identifier and identifier in self.children:
            self.children.remove(identifier)

        for child in self.children:
            sub_processor = DatasetProcessor(self.config, child)
            sub_processor.create_list_datasets(child)
            self.datasets.extend(sub_processor.datasets)

    def get_list_datasets(self):
        return list(set(self.datasets))  # Deduplicate

# ========== METADATA HELPERS ==========

def filemetadata(base_url, token, doi):
    api = NativeApi(base_url, token)
    file_keys, file_values = [], []

    if doi == 'doi:10.34810/data1872':
        return file_keys, file_values

    try:
        dataset = api.get_dataset(doi)
        files = dataset.json()['data']['latestVersion']['files']
        for f in files:
            data_file = f['dataFile']
            file_keys.append(list(data_file.keys()))
            file_values.append(list(data_file.values()))
    except Exception as e:
        print(f"[Error] DOI {doi}: {str(e)}")

    return file_keys, file_values

def get_dataset_sizes(base_url, token, doi):
    keys, values = filemetadata(base_url, token, doi)

    def extract_size(entry, keys_list):
        idx = keys_list.index('originalFileSize') if 'originalFileSize' in keys_list else \
              keys_list.index('filesize') if 'filesize' in keys_list else None
        if idx is not None and isinstance(entry[idx], int):
            return entry[idx]
        return 0

    sizes = [extract_size(v, keys[i]) for i, v in enumerate(values)]
    total_original = sum(sizes)

    archival_index = keys[0].index('filesize') if keys and 'filesize' in keys[0] else None
    total_archival = sum(v[archival_index] for v in values if archival_index is not None and isinstance(v[archival_index], int))

    return total_original, total_archival

def format_size(size):
    units = ["Bytes", "KB", "MB", "GB", "TB"]
    idx = 0
    size = float(size)
    while size >= 1024 and idx < len(units) - 1:
        size /= 1024
        idx += 1
    return round(size, 2), units[idx]

# ========== MAIN ==========

def main():
    base_url = "https://dataverse.csuc.cat/"

    print("🔑 Enter your Dataverse API token:")
    token = input("> ").strip()
    config = Config(api_url=base_url, logger=logger, token=token)

    institutions = [
        'UB', 'UAB', 'UPC', 'UPF', 'UdG', 'UdL', 'URV', 'UOC', 'UVIC-UCC',
        'URL', 'UIC', 'UIB', 'Agrotecnio', 'CED', 'CRAG', 'CREAF', 'CRM', 'CTFC',
        'i2CAT', 'I3PT', 'IBEC', 'IBEI', 'ICAC-CERCA', 'ICFO-CERCA','ICIQ', 'ICN2',
        'ICRA-CERCA', 'IDIBAPS', 'IDIBELL', 'IDIBGI-CERCA', 'IFAE', 'IJC','IRSantPau','CVC','IRSJD',
        'IPHES-CERCA', 'IRBBarcelona-CERCA', 'IRB', 'IRSICAIXA', 'IRTA',
        'ISGLOBAL', 'VHIR'
    ]

    print("\n🏢 Enter institution codes separated by commas (or type 'all'):")
    print(f"Available: {', '.join(institutions)}")
    user_input = input("> ").strip().upper()
    selected = institutions if user_input == 'ALL' else [i.strip() for i in user_input.split(',') if i.strip() in institutions]

    if not selected:
        print("⚠️ No valid institutions selected.")
        return

    data = []
    for inst in selected:
        print(f"🔍 Processing institution: {inst}")
        processor = DatasetProcessor(config, inst)
        processor.create_list_datasets(inst)

        for doi in processor.get_list_datasets():
            orig, arch = get_dataset_sizes(base_url, token, doi)
            f_orig, u_orig = format_size(orig)
            f_arch, u_arch = format_size(arch)
            data.append([doi, inst, orig, arch, f_orig, u_orig, f_arch, u_arch])

    # Generate DataFrame
    df = pd.DataFrame(data, columns=[
        "DOI", "Institution", "Original Size (Bytes)", "Archival Size (Bytes)",
        "Formatted Original Size", "Unit (Original Size)",
        "Formatted Archival Size", "Unit (Archival Size)"
    ])

    df['DOI_Number'] = df['DOI'].str.extract(r'data(\d+)').astype(int)
    df = df.sort_values(by='DOI_Number')
    df['DOI'] = 'https://doi.org/10.34810/data' + df['DOI_Number'].astype(str)
    df.drop(columns=['DOI_Number'], inplace=True)

    # Save to Excel
    output_file = "datasets_sizes.xlsx"
    df.to_excel(output_file, index=False)
    print(f"\n✅ Data saved to {output_file}")
    print(df)

if __name__ == "__main__":
    main()
