# ===========================
# PARAMETERS (Set Before Run)
# ===========================
# Set your API token here
API_TOKEN = "YOUR_API_TOKEN_HERE"

# Set your selected institutions (choose from the list below or use all)
# Example: ["UB", "UAB"] or ["All"]
SELECTED_INSTITUTIONS = ["All"]

# ===========================
# BEGIN SCRIPT
# ===========================
import os
import subprocess
import sys
import logging
import pandas as pd
import requests
from datetime import datetime
from pyDataverse.api import NativeApi, DataAccessApi
from collections import defaultdict

# Install required package if not installed
try:
    import pyDataverse
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "pyDataverse"])

# Define institution list
INSTITUTIONS = [
    'UB', 'UAB', 'UPC', 'UPF', 'UdG', 'UdL', 'URV', 'UOC', 'UVIC-UCC',
    'URL', 'UIC', 'UIB', 'Agrotecnio', 'CED', 'CRAG', 'CREAF', 'CRM', 'CTFC','CVC',
    'i2CAT', 'I3PT', 'IBEC', 'IBEI', 'ICAC-CERCA', 'ICFO-CERCA','ICIQ', 'ICN2',
    'ICRA-CERCA', 'IDIBAPS', 'IDIBELL', 'IDIBGI-CERCA', 'IFAE', 'IJC','IRSantPau','CVC','IRSJD',
    'IPHES-CERCA', 'IRBBarcelona-CERCA', 'IRB', 'IRSICAIXA', 'IRTA','IRSJD',
    'ISGLOBAL', 'VHIR'
]

if "All" in SELECTED_INSTITUTIONS:
    SELECTED_INSTITUTIONS = INSTITUTIONS

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Config classes
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

    def call_api(self, url, method, data=None):
        headers = {'X-Dataverse-key': self.config.get_token()}
        response = requests.request("GET", url, headers=headers)
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

    def update_list_dataverse_children(self, dataseverse_id):
        self.list_dataverse_children.append(dataseverse_id)

    def remove_id_list_dataverse_children(self, dataseverse_id):
        self.list_dataverse_children.remove(dataseverse_id)

    def get_list_datasets(self):
        return self.list_datasets

    def get_list_dataverse_children(self):
        return self.list_dataverse_children

    def create_list_datasets(self, identifier):
        conn = UtilsConnection(self.config)
        url_api = f"{self.config.get_api_url()}/api/dataverses/{identifier}/contents"
        object_json = conn.call_api(url_api, "GET")

        if object_json:
            array_json = object_json.get("data", [])
            for value in array_json:
                if value['type'] == 'dataverse':
                    self.update_list_dataverse_children(value['id'])
                elif value['type'] == 'dataset' and value['protocol'] == 'doi':
                    self.update_list_dataset(f"{value['protocol']}:{value['authority']}/{value['identifier']}")
        if identifier != self.identifier:
            self.remove_id_list_dataverse_children(identifier)
        if self.get_list_dataverse_children():
            self.create_list_datasets(self.get_list_dataverse_children()[0])

# Metadata extraction
def export_metadata(base_url, token, doi, data_keys, data_values, stateDataset):
    api = NativeApi(base_url, token)
    try:
        dataset = api.get_dataset(doi)
        dataset_data = dataset.json()['data']['latestVersion']
        if "publicationDate" in dataset_data:
            data_keys.append("publicationDate")
            data_values.append(dataset_data["publicationDate"])
    except:
        pass

def filemetadata(base_url, token, doi, filemetadata_keys, filemetadata_values):
    api = NativeApi(base_url, token)
    try:
        if doi != 'doi:10.34810/data1872':
            dataset = api.get_dataset(doi)
            for file_info in dataset.json()['data']['latestVersion']['files']:
                data_file = file_info['dataFile']
                filemetadata_keys.append(list(data_file.keys()))
                filemetadata_values.append(list(data_file.values()))
    except KeyError:
        print(f"Error reading file metadata for DOI: {doi}")

# Main Execution
config = Config(api_url="https://dataverse.csuc.cat/", logger=logger, token=API_TOKEN)
base_url = config.get_api_url()

filemetadata_keys = []
filemetadata_values = []
list_doi = []
instancia = []
name_readme_file = []
validation_readme_file = []
published = []

for institution in SELECTED_INSTITUTIONS:
    processor = DatasetProcessor(config, institution)
    processor.create_list_datasets(institution)
    for doi in processor.get_list_datasets():
        data_keys, data_values, stateDataset = [], [], []
        export_metadata(base_url, API_TOKEN, doi, data_keys, data_values, stateDataset)

        published.append('Published' if data_values else 'Draft')

        file_keys_aux, file_values_aux = [], []
        filemetadata(base_url, API_TOKEN, doi, file_keys_aux, file_values_aux)
        filemetadata_keys.extend(file_keys_aux)
        filemetadata_values.extend(file_values_aux)
        instancia.append(institution)
        list_doi.append(doi)

        readme_files = []
        for k, v in zip(file_keys_aux, file_values_aux):
            if 'filename' in k:
                idx = k.index('filename')
                if 'readme' in v[idx].lower():
                    readme_files.append(v[idx])
        name_readme_file.append(readme_files)
        validation_readme_file.append('Yes' if readme_files else 'No')

# Create and save DataFrame
df = pd.DataFrame({
    'DOI': list_doi,
    'Published': published,
    'Institution': instancia,
    'Is there Readme?': validation_readme_file,
    'Readme file name': [", ".join(r) for r in name_readme_file]
})

df['DOI_Number'] = df['DOI'].str.extract(r'data(\d+)').astype(int)
df = df.sort_values(by='DOI_Number')
df['DOI'] = 'https://doi.org/10.34810/data' + df['DOI_Number'].astype(str)
df = df.drop(columns=['DOI_Number'])

excel_filename = 'datasets_readme_verification.xlsx'
df.to_excel(excel_filename, index=False)

print(f"\nExcel file created: {excel_filename}")
print(df)
