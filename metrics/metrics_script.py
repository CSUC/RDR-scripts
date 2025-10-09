import os
import sys
import subprocess
import logging
import requests
import pandas as pd
from pyDataverse.api import NativeApi, DataAccessApi
from datetime import datetime

# ====================== Package Installation ======================
def install_packages():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyDataverse", "pandas", "openpyxl", "requests"])

try:
    import pyDataverse
except ImportError:
    print("Installing required libraries...")
    install_packages()
    import pyDataverse

# ====================== Configuration Classes ======================
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
        response = requests.request(method, url, headers=headers, data=data or {})
        response.raise_for_status()
        return response.json()

class DatasetProcessor:
    def __init__(self, config, identifier):
        self.config = config
        self.list_datasets = []
        self.list_dataverse_children = []
        self.identifier = identifier

    def update_list_dataset(self, dataset_id):
        self.list_datasets.append(dataset_id)

    def update_list_dataverse_children(self, dataverse_id):
        self.list_dataverse_children.append(dataverse_id)

    def remove_id_list_dataverse_children(self, dataverse_id):
        if dataverse_id in self.list_dataverse_children:
            self.list_dataverse_children.remove(dataverse_id)

    def get_list_datasets(self):
        return self.list_datasets

    def get_list_dataverse_children(self):
        return self.list_dataverse_children

    def create_list_datasets(self, identifier):
        conn = UtilsConnection(self.config)
        url_api = f"{self.config.get_api_url()}/api/dataverses/{identifier}/contents"
        object_json = conn.call_api(url_api, "GET")

        if object_json:
            self.config.get_logger().info(f"Reading API values for {identifier}")
            array_json = object_json.get("data", [])
            for value in array_json:
                if value['type'] == 'dataverse':
                    self.update_list_dataverse_children(value['id'])
                elif value['type'] == 'dataset' and value['protocol'] == 'doi':
                    self.update_list_dataset(f"{value['protocol']}:{value['authority']}/{value['identifier']}")
        else:
            self.config.get_logger().error(f"API call failed for {identifier}")

        if identifier != self.identifier:
            self.remove_id_list_dataverse_children(identifier)

        if self.list_dataverse_children:
            self.create_list_datasets(self.list_dataverse_children[0])

# ====================== Metrics Extraction ======================
def fetch_metric(doi, metric, base_url):
    try:
        url = f"{base_url}/api/datasets/:persistentId/makeDataCount/{metric}?persistentId={doi}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "OK" and "data" in data:
                if metric == "citations":
                    return len(data["data"])
                elif isinstance(data["data"], dict):
                    return data["data"].get(metric)
    except Exception as e:
        print(f"Error fetching {metric} for {doi}: {e}")
    return None

# ====================== User Input ======================
SERVER_URL = "https://dataverse.csuc.cat"
token = input(" Enter your API token (get it from https://dataverse.csuc.cat/dataverseuser.xhtml?selectTab=apiTokenTab): ").strip()

# Institution list
institutions = [
    'UB', 'UAB', 'UPC', 'UPF', 'UdG', 'UdL', 'URV', 'UOC', 'UVIC-UCC', 'URL', 'UIC', 'UIB',
    'Agrotecnio', 'CED', 'CRAG', 'CREAF', 'CRM', 'CTFC', 'CVC', 'i2CAT', 'I3PT', 'IBEC',
    'IBEI', 'ICAC-CERCA', 'ICFO-CERCA', 'ICIQ', 'ICN2', 'ICRA-CERCA', 'IDIBAPS', 'IDIBELL',
    'IDIBGI-CERCA', 'IFAE', 'IJC', 'IRSantPau', 'IRSJD', 'IPHES-CERCA', 'IRBBarcelona-CERCA',
    'IRB', 'IRSICAIXA', 'IRTA', 'ISGLOBAL', 'VHIR'
]

print("\n Available Institutions:")
for i, name in enumerate(institutions, 1):
    print(f"  {i:2}. {name}")
print("  0. All institutions")

selection = input("Select institution numbers separated by commas (e.g., 1,3,5) or 0 for all: ")
selection = [s.strip() for s in selection.split(",")]

if "0" in selection:
    selected_institutions = institutions
else:
    selected_institutions = [institutions[int(s) - 1] for s in selection if s.isdigit() and 0 < int(s) <= len(institutions)]

# ====================== Initialize Logging and API ======================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DataverseMetrics")
config = Config(api_url=SERVER_URL, logger=logger, token=token)

api = NativeApi(SERVER_URL, token)
data_api = DataAccessApi(SERVER_URL, token)

# ====================== Main Execution ======================
metrics_data = []

print("\n Gathering metrics...")

for institution in selected_institutions:
    print(f"📡 Processing institution: {institution}")
    processor = DatasetProcessor(config, institution)
    processor.create_list_datasets(institution)

    for doi in processor.get_list_datasets():
        metrics_data.append({
            "DOI": doi,
            "Institution": institution,
            "Total Views": fetch_metric(doi, "viewsTotal", SERVER_URL),
            "Unique Views": fetch_metric(doi, "viewsUnique", SERVER_URL),
            "Total Downloads": fetch_metric(doi, "downloadsTotal", SERVER_URL),
            "Unique Downloads": fetch_metric(doi, "downloadsUnique", SERVER_URL),
            "Citations": fetch_metric(doi, "citations", SERVER_URL)
        })

# Create and sort DataFrame
df = pd.DataFrame(metrics_data)
df['DOI_Number'] = df['DOI'].str.extract(r'data(\d+)').astype(float)
df = df.sort_values(by='DOI_Number')
df['DOI'] = 'https://doi.org/10.34810/data' + df['DOI_Number'].astype(int).astype(str)
df.drop(columns=['DOI_Number'], inplace=True)

# Save to Excel
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f"dataverse_metrics_{timestamp}.xlsx"
df.to_excel(filename, index=False)

# Done
print(f"\n Export complete! Metrics saved to: {filename}")
