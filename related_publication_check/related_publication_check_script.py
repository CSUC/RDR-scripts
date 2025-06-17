import subprocess
import os
import sys

# Function to install required packages
def install_packages():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "-q"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyDataverse", "-q"])
    print("Libraries have been downloaded or updated.")

# Install libraries if they are not installed already
try:
    import pyDataverse
except ImportError:
    install_packages()

import logging
from pyDataverse.api import NativeApi, DataAccessApi
import pandas as pd
import requests
from datetime import datetime
from collections import defaultdict

# ========== USER PARAMETERS ==========
API_TOKEN = "PASTE_YOUR_API_TOKEN_HERE"
SELECTED_INSTITUTIONS = ['UB', 'UAB']  # Replace with your list or ['All'] to include all institutions
# =====================================

# Dataverse API base URL
BASE_URL = "https://dataverse.csuc.cat/"

# Full institution list
ALL_INSTITUTIONS = [
    'UB', 'UAB', 'UPC', 'UPF', 'UdG', 'UdL', 'URV', 'UOC', 'UVIC-UCC',
    'URL', 'UIC', 'UIB', 'Agrotecnio', 'CED', 'CRAG', 'CREAF', 'CRM', 'CTFC','CVC',
    'i2CAT', 'I3PT', 'IBEC', 'IBEI', 'ICAC-CERCA', 'ICFO-CERCA','ICIQ', 'ICN2',
    'ICRA-CERCA', 'IDIBAPS', 'IDIBELL', 'IDIBGI-CERCA', 'IFAE', 'IJC','IRSantPau','CVC','IRSJD',
    'IPHES-CERCA', 'IRBBarcelona-CERCA', 'IRB', 'IRSICAIXA', 'IRTA','IRSJD',
    'ISGLOBAL', 'VHIR'
]

if 'All' in SELECTED_INSTITUTIONS:
    SELECTED_INSTITUTIONS = ALL_INSTITUTIONS

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration Classes
class Config:
    def __init__(self, api_url, logger, token):
        self.api_url = api_url
        self.logger = logger
        self.token = token

    def get_api_url(self):
        return self.api_url

    def get_logger(self):
        return self.logger

    def get_token(self):
        return self.token

class UtilsConnection:
    def __init__(self, config):
        self.config = config

    def call_api(self, url, method, data=None):
        headers = {'X-Dataverse-key': self.config.get_token()}
        response = requests.request(method, url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()

class DatasetProcessor:
    def __init__(self, config, identifier):
        self.config = config
        self.identifier = identifier
        self.list_datasets = []
        self.list_dataverse_children = []

    def update_list_dataset(self, dataset_id):
        self.list_datasets.append(dataset_id)

    def update_list_dataverse_children(self, dataverse_id):
        self.list_dataverse_children.append(dataverse_id)

    def remove_id_list_dataverse_children(self, dataverse_id):
        self.list_dataverse_children.remove(dataverse_id)

    def get_list_datasets(self):
        return self.list_datasets

    def create_list_datasets(self, identifier):
        conn = UtilsConnection(self.config)
        url_api = f"{self.config.get_api_url()}/api/dataverses/{identifier}/contents"
        object_json = conn.call_api(url_api, "GET")
        if object_json:
            self.config.get_logger().info(f"Reading the API values for {identifier}")
            for value in object_json.get("data", []):
                if value['type'] == 'dataverse':
                    self.update_list_dataverse_children(value['id'])
                elif value['type'] == 'dataset' and value['protocol'] == 'doi':
                    self.update_list_dataset(f"{value['protocol']}:{value['authority']}/{value['identifier']}")
        if identifier != self.identifier:
            self.remove_id_list_dataverse_children(identifier)
        if self.list_dataverse_children:
            self.create_list_datasets(self.list_dataverse_children[0])

# Metadata extraction helpers
def extract_value(data_dict):
    if isinstance(data_dict, dict):
        type_names, values = [], []
        for key, value in data_dict.items():
            if key == 'typeName' and 'value' in data_dict:
                v = data_dict['value']
                if isinstance(v, list):
                    type_names.extend([data_dict['typeName']] * len(v))
                    values.extend(v)
                else:
                    type_names.append(data_dict['typeName'])
                    values.append(v)
            else:
                t, v = extract_value(value)
                type_names += t
                values += v
        return type_names, values
    elif isinstance(data_dict, list):
        type_names, values = [], []
        for item in data_dict:
            t, v = extract_value(item)
            type_names += t
            values += v
        return type_names, values
    return [], []

def export_metadata(base_url, token, doi, citation_keys, citation_values, customUAB_keys, customUAB_values, stateDataset):
    api = NativeApi(base_url, token)
    try:
        dataset = api.get_dataset(doi).json()['data']['latestVersion']
        if 'citation' in dataset['metadataBlocks']:
            citation = extract_value(dataset['metadataBlocks']['citation']['fields'])
            citation_keys.extend(citation[0])
            citation_values.extend(citation[1])
        if 'customUAB' in dataset['metadataBlocks']:
            custom = extract_value(dataset['metadataBlocks']['customUAB']['fields'])
            customUAB_keys.extend(custom[0])
            customUAB_values.extend(custom[1])
    except Exception as e:
        logger.error(f"Failed to export metadata for {doi}: {e}")

def extract_metadata(data, citation_keys, citation_values, customUAB_keys, customUAB_values):
    for key, value in zip(citation_keys, citation_values):
        if not isinstance(value, dict):
            data.append([key, value])
    for key, value in zip(customUAB_keys, customUAB_values):
        if not isinstance(value, dict):
            data.append([key, value])

# Collect data
selected_metadata = ["publicationRelationType", "publicationCitation", "publicationIDType", "publicationIDNumber", "publicationURL", "reviewLibrary"]
metadata_keys_list = []
metadata_values_list = []
list_doi = []
instancia = []

config = Config(api_url=BASE_URL, logger=logger, token=API_TOKEN)

for institution in SELECTED_INSTITUTIONS:
    processor = DatasetProcessor(config, institution)
    processor.create_list_datasets(institution)
    for doi in processor.get_list_datasets():
        citation_keys, citation_values = [], []
        customUAB_keys, customUAB_values = [], []
        stateDataset = []
        export_metadata(BASE_URL, API_TOKEN, doi, citation_keys, citation_values, customUAB_keys, customUAB_values, stateDataset)
        data = []
        extract_metadata(data, citation_keys, citation_values, customUAB_keys, customUAB_values)
        df = pd.DataFrame(data, columns=['Metadata', 'Value'])
        metadata_keys_list.append(df['Metadata'].tolist())
        metadata_values_list.append(df['Value'].tolist())
        instancia.append(institution)
        list_doi.append(doi)

# Aggregate metadata
def aggregate_metadata(metadata_keys_list, metadata_values_list, list_doi, selected_metadata):
    metadata_values = defaultdict(lambda: defaultdict(set))
    for i in range(len(metadata_keys_list)):
        doi = list_doi[i]
        for key, value in zip(metadata_keys_list[i], metadata_values_list[i]):
            if key in selected_metadata:
                if isinstance(value, list):
                    metadata_values[key][doi].update(value)
                else:
                    metadata_values[key][doi].add(value)
    aggregated_metadata = {field: [''] * len(list_doi) for field in selected_metadata}
    for field in selected_metadata:
        for doi in list_doi:
            values = list(metadata_values[field][doi])
            aggregated_metadata[field][list_doi.index(doi)] = '; '.join(values) if values else ''
    return aggregated_metadata

metadata = aggregate_metadata(metadata_keys_list, metadata_values_list, list_doi, selected_metadata)

# Create final DataFrame
data = {'DOI': list_doi, 'Institution': instancia}
for field in selected_metadata:
    data[field] = metadata[field]
df = pd.DataFrame(data)

# Format and sort
df['DOI_Number'] = df['DOI'].str.extract(r'data(\d+)').astype(int)
df = df.sort_values(by='DOI_Number')
df['DOI'] = 'https://doi.org/10.34810/data' + df['DOI_Number'].astype(str)
df = df.drop(columns=['DOI_Number'])

# Save to Excel
filename = 'related_publication_metadata.xlsx'
df.to_excel(filename, index=False)
print(f"\nExcel file generated: {filename}")

