import subprocess
import sys

# Function to install required packages
def install_packages():
    """
    Function to install or update necessary Python packages.
    """
    # Upgrade pip first
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "-q"])

    # Install the required libraries
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyDataverse", "pandas", "requests", "-q"])

    print("Libraries have been downloaded or updated.")

# Install libraries if they are not installed already
try:
    import pyDataverse
except ImportError:
    print("Installing libraries...")
    install_packages()

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pyDataverse.api import NativeApi, DataAccessApi, MetricsApi
from pyDataverse.models import Dataverse
import pandas as pd
import requests
import logging
from datetime import datetime
class UtilsConnection:
    def __init__(self, config):
        self.config = config

    def call_api(self, url, method, data=None):
        payload = {}
        headers = {'X-Dataverse-key': config.get_token()}

        response = requests.request("GET", url, headers=headers, data=payload)
        response.raise_for_status()
        return response.json()

class Config:
    def __init__(self, api_url, logger, token):
        self.api_url = api_url
        self.logger = logger
        self.token = token

    def get_app_config(self):
        return self

    def get_api_url(self):
        return self.api_url

    def get_logger(self):
        return self.logger

    def get_token(self):
        return self.token

class DatasetProcessor:
    def __init__(self, config, identifier):
        self.config = config
        self.list_datasets = []
        self.list_dataverse_children = []
        self.identifier = identifier

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

    def count(self):
        return len(self.list_datasets)

    def create_list_datasets(self, identifier):

        conn = UtilsConnection(self.config)

        url_api = f"{self.config.get_api_url()}/api/dataverses/{identifier}/contents"
        object_json = conn.call_api(url_api, "GET")

        if object_json:
            self.config.get_logger().info(f"Reading the API values")
            array_json = object_json.get("data", {})

            for value in array_json:
                if value['type'] == 'dataverse':
                    self.update_list_dataverse_children(value['id'])
                elif value['type'] == 'dataset' and value['protocol'] == 'doi':
                    self.update_list_dataset(value['protocol'] + ':' + value['authority'] + '/' + value['identifier'])
        else:
            self.config.get_logger().error(f"Call API ERROR")

        if not identifier == self.identifier:
            self.remove_id_list_dataverse_children(identifier)

        if len(self.get_list_dataverse_children()) != 0:

            self.create_list_datasets(self.get_list_dataverse_children()[0])
def extract_value(data_dict):
    """
    Function to extract type names and values from a JSON metadata dictionary.

    Args:
    data_dict (dict): JSON metadata dictionary.

    Returns:
    tuple: Type names and values extracted from the metadata dictionary.
    """
    if isinstance(data_dict, dict):
        type_names = []
        values = []
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
                extracted_type_names, extracted_values = extract_value(value)
                type_names += extracted_type_names
                values += extracted_values
        return type_names, values
    elif isinstance(data_dict, list):
        type_names = []
        values = []
        for item in data_dict:
            extracted_type_names, extracted_values = extract_value(item)
            type_names += extracted_type_names
            values += extracted_values
        return type_names, values
    else:
        return [], []

def export_metadata(base_url, token, doi, data_keys, data_values, citation_keys, citation_values, geo_keys, geo_values, social_keys, social_values, astronomy_keys, astronomy_values, biomedical_keys, biomedical_values, journal_keys, journal_values, customUAB_keys, customUAB_values, stateDataset):
    """
    Function to export metadata from a dataset and store it in respective lists.

    Args:
    base_url (str): Base URL of the Dataverse repository.
    token (str): API token for authentication.
    doi (str): DOI of the dataset.
    citation_keys (list): List to store citation metadata keys.
    citation_values (list): List to store citation metadata values.
    geo_keys (list): List to store geospatial metadata keys.
    geo_values (list): List to store geospatial metadata values.
    social_keys (list): List to store social science metadata keys.
    social_values (list): List to store social science metadata values.
    astronomy_keys (list): List to store astronomy metadata keys.
    astronomy_values (list): List to store astronomy metadata values.
    biomedical_keys (list): List to store biomedical metadata keys.
    biomedical_values (list): List to store biomedical metadata values.
    journal_keys (list): List to store journal metadata keys.
    journal_values (list): List to store journal metadata values.
    customUAB_keys (list): List to store customUAB metadata keys.
    customUAB_values (list): List to store customUAB metadata values.

    Returns:
    None
    """
    from pyDataverse.api import NativeApi, DataAccessApi
    from pyDataverse.models import Dataverse
    api = NativeApi(base_url, token)  # Function to access the API
    data_api = DataAccessApi(base_url, token)  # Function to access data via the API
    try:
        dataset = api.get_dataset(doi)  # Retrieve dataset metadata

      # Extract dataset dates metadata if available
        dataset_data = dataset.json()['data']['latestVersion']  # Extract once

        date_keys_all = [
            "publicationDate", "lastUpdateTime", "releaseTime",
            "createTime", "productionDate", "citationDate"
        ]

        for key in date_keys_all:
            if key in dataset_data:
                data_keys.append(key)
                data_values.append(dataset_data[key])

      # Extract citation metadata if available
        if 'citation' in dataset.json()['data']['latestVersion']['metadataBlocks']:
            metadata_citation = dataset.json()['data']['latestVersion']['metadataBlocks']['citation']['fields']
            citation = extract_value(metadata_citation)
            citation_keys.extend(citation[0])
            citation_values.extend(citation[1])
            for item in metadata_citation:
                if isinstance(item['value'], str):
                    index_change = citation_keys.index(item['typeName'])
                    citation_values[index_change] = item['value']

        # Extract geospatial metadata if available
        if 'geospatial' in dataset.json()['data']['latestVersion']['metadataBlocks']:
            metadata_geospatial = dataset.json()['data']['latestVersion']['metadataBlocks']['geospatial']['fields']
            geospatial = extract_value(metadata_geospatial)
            geo_keys.extend(geospatial[0])
            geo_values.extend(geospatial[1])
            for item in metadata_geospatial:
                if isinstance(item['value'], str):
                    index_canvi = geo_keys.index(item['typeName'])
                    geo_values[index_canvi] = item['value']

        # Extract social science metadata if available
        if 'socialscience' in dataset.json()['data']['latestVersion']['metadataBlocks']:
            metadata_socialscience = dataset.json()['data']['latestVersion']['metadataBlocks']['socialscience']['fields']
            socialscience = extract_value(metadata_socialscience)
            social_keys.extend(socialscience[0])
            social_values.extend(socialscience[1])
            for item in metadata_socialscience:
                if isinstance(item['value'], str):
                    index_canvi = social_keys.index(item['typeName'])
                    social_values[index_canvi] = item['value']

        # Extract astronomy metadata if available
        if 'astrophysics' in dataset.json()['data']['latestVersion']['metadataBlocks']:
            metadata_astronomy = dataset.json()['data']['latestVersion']['metadataBlocks']['astrophysics']['fields']
            astronomy = extract_value(metadata_astronomy)
            astronomy_keys.extend(astronomy[0])
            astronomy_values.extend(astronomy[1])
            for item in metadata_astronomy:
                if isinstance(item['value'], str):
                    index_canvi = astronomy_keys.index(item['typeName'])
                    astronomy_values[index_canvi] = item['value']

        # Extract biomedical metadata if available
        if 'biomedical' in dataset.json()['data']['latestVersion']['metadataBlocks']:
            metadata_biomedical = dataset.json()['data']['latestVersion']['metadataBlocks']['biomedical']['fields']
            biomedical = extract_value(metadata_biomedical)
            biomedical_keys.extend(biomedical[0])
            biomedical_values.extend(biomedical[1])
            for item in metadata_biomedical:
                if isinstance(item['value'], str):
                    index_canvi = biomedical_keys.index(item['typeName'])
                    biomedical_values[index_canvi] = item['value']

        # Extract journal metadata if available
        if 'journal' in dataset.json()['data']['latestVersion']['metadataBlocks']:
            metadata_journal = dataset.json()['data']['latestVersion']['metadataBlocks']['journal']['fields']
            journal = extract_value(metadata_journal)
            journal_keys.extend(journal[0])
            journal_values.extend(journal[1])
            for item in metadata_journal:
                if isinstance(item['value'], str):
                    index_canvi = journal_keys.index(item['typeName'])
                    journal_values[index_canvi] = item['value']

        # Extract Library UAB metadata if available

        if 'customUAB' in dataset.json()['data']['latestVersion']['metadataBlocks']:
            metadata_customUAB = dataset.json()['data']['latestVersion']['metadataBlocks']['customUAB']['fields']
            customUAB = extract_value(metadata_customUAB)
            customUAB_keys.extend(customUAB[0])
            customUAB_values.extend(customUAB[1])
            for item in metadata_customUAB:
                if isinstance(item['value'], str):
                    index_change = customUAB_keys.index(item['typeName'])
                    customUAB_values[index_change] = item['value']

    except KeyError or InvalidSchema:
        pass

def extract_metadata(data, data_keys,data_values,citation_keys, citation_values, geo_keys, geo_values, social_keys, social_values, astronomy_keys, astronomy_values, biomedical_keys, biomedical_values, journal_keys, journal_values, customUAB_keys, customUAB_values):
    for key, value in zip(data_keys, data_values):
        if not isinstance(value, dict):
            data.append([key, value])

    for key, value in zip(citation_keys, citation_values):
        if not isinstance(value, dict):
            data.append([key, value])

    for key, value in zip(geo_keys, geo_values):
        if not isinstance(value, dict):
            data.append([key, value])

    for key, value in zip(social_keys, social_values):
        if not isinstance(value, dict):
            data.append([key, value])

    for key, value in zip(astronomy_keys, astronomy_values):
        if not isinstance(value, dict):
            data.append([key, value])

    for key, value in zip(biomedical_keys, biomedical_values):
        if not isinstance(value, dict):
            data.append([key, value])

    for key, value in zip(journal_keys, journal_values):
        if not isinstance(value, dict):
            data.append([key, value])

    for key, value in zip(customUAB_keys, customUAB_values):
        if not isinstance(value, dict):
            data.append([key, value])

import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ask the user for the token
token = input("Please enter your API token: ")

# Use the token in your configuration
config = Config(api_url="https://dataverse.csuc.cat/", logger=logger, token=token)
# List of institutions
institucions = [
    'UB', 'UAB', 'UPC', 'UPF', 'UdG', 'UdL', 'URV', 'UOC', 'UVIC-UCC',
    'URL', 'UIC', 'UIB', 'Agrotecnio', 'CED', 'CRAG', 'CREAF', 'CRM', 'CTFC','CVC',
    'i2CAT', 'I3PT', 'IBEC', 'IBEI', 'ICAC-CERCA', 'ICFO-CERCA','ICIQ', 'ICN2',
    'ICRA-CERCA', 'IDIBAPS', 'IDIBELL', 'IDIBGI-CERCA', 'IFAE', 'IJC','IRSantPau','CVC','IRSJD',
    'IPHES-CERCA', 'IRBBarcelona-CERCA', 'IRB', 'IRSICAIXA', 'IRTA','IRSJD',
    'ISGLOBAL', 'VHIR'
]

# Define metadata categories
data_metadata = {"publicationDate":"Publication Date",
                 "createTime":"Create Time",
                 "lastUpdateTime":"Last Update Time",
                 "releaseTime": "Release Time",
                 "productionDate": "Production Date",
                 "citationDate": "Citation Date" }
citation_metadata = {
    "PreviousDatasetPersistentID": "Previous Dataset Persistent ID",
    "title": "Title",
    "subtitle": "Subtitle",
    "alternativeTitle": "Alternative Title",
    "alternativeURL": "Alternative URL",
    "otherIdAgency": "Other ID Agency",
    "otherIdValue": "Other ID Value",
    "authorName": "Author Name",
    "authorAffiliation": "Author Affiliation",
    "authorIdentifierScheme": "Author Identifier Scheme",
    "authorIdentifier": "Author Identifier",
    "datasetContactName": "Dataset Contact Name",
    "datasetContactAffiliation": "Dataset Contact Affiliation",
    "datasetContactEmail": "Dataset Contact Email",
    "dsDescriptionValue": "Description Value",
    "dsDescriptionDate": "Description Date",
    "subject": "Subject",
    "keywordValue": "Keyword",
    "keywordVocabulary": "Keyword Vocabulary",
    "keywordVocabularyURI": "Keyword Vocabulary URI",
    "topicClassValue": "Topic Class",
    "topicClassVocab": "Topic Class Vocabulary",
    "topicClassVocabURI": "Topic Class Vocabulary URI",
    "publicationRelationType": "Publication Relation Type",
    "publicationCitation": "Publication Citation",
    "publicationIDType": "Publication ID Type",
    "publicationIDNumber": "Publication ID Number",
    "publicationURL": "Publication URL",
    "notesText": "Notes",
    "language": "Language",
    "producerName": "Producer Name",
    "producerAffiliation": "Producer Affiliation",
    "producerAbbreviation": "Producer Abbreviation",
    "producerURL": "Producer URL",
    "productionDate": "Production Date",
    "productionPlace": "Production Place",
    "contributorType": "Contributor Type",
    "contributorName": "Contributor Name",
    "grantNumberAgency": "Grant Number Agency",
    "grantNumberValue": "Grant Number Value",
    "distributorAffiliation": "Distributor Affiliation",
    "distributorAbbreviation": "Distributor Abbreviation",
    "distributorURL": "Distributor URL",
    "distributionDate": "Distribution Date",
    "depositor": "Depositor",
    "dateOfDeposit": "Date of Deposit",
    "timePeriodCoveredStart": "Time Period Covered Start",
    "timePeriodCoveredEnd": "Time Period Covered End",
    "dateOfCollectionStart": "Date of Collection Start",
    "dateOfCollectionEnd": "Date of Collection End",
    "kindOfData": "Kind of Data",
    "seriesName": "Series Name",
    "seriesInformation": "Series Information",
    "softwareName": "Software Name",
    "softwareVersion": "Software Version",
    "relatedMaterial": "Related Material",
    "relatedDatasets": "Related Datasets",
    "otherReferences": "Other References",
    "dataSources": "Data Sources",
    "originOfSources": "Origin of Sources",
    "characteristicOfSources": "Characteristic of Sources",
    "accessToSources": "Access to Sources"
}


geospatial_metadata = {
    "country": "Country",
    "state": "State",
    "city": "City",
    "otherGeographicCoverage": "Other Geographic Coverage",
    "geographicUnit": "Geographic Unit",
    "westLongitude": "West Longitude",
    "eastLongitude": "East Longitude",
    "northLongitude": "North Longitude",
    "southLongitude": "South Longitude"
}


social_metadata = {
    "unitOfAnalysis": "Unit of Analysis",
    "universe": "Universe",
    "timeMethod": "Time Method",
    "dataCollector": "Data Collector",
    "collectorTraining": "Collector Training",
    "frequencyOfDataCollection": "Frequency of Data Collection",
    "samplingProcedure": "Sampling Procedure",
    "targetSampleActualSize": "Target Sample Actual Size",
    "targetSampleSizeFormula": "Target Sample Size Formula",
    "deviationsFromSampleDesign": "Deviations From Sample Design",
    "collectionMode": "Collection Mode",
    "researchInstrument": "Research Instrument",
    "dataCollectionSituation": "Data Collection Situation",
    "actionsToMinimizeLoss": "Actions to Minimize Loss",
    "controlOperations": "Control Operations",
    "weighting": "Weighting",
    "cleaningOperations": "Cleaning Operations",
    "datasetLevelErrorNotes": "Dataset Level Error Notes",
    "responseRate": "Response Rate",
    "samplingErrorEstimates": "Sampling Error Estimates",
    "otherDataAppraisal": "Other Data Appraisal",
    "socialScienceNotesType": "Social Science Notes Type",
    "socialScienceNotesSubject": "Social Science Notes Subject",
    "socialScienceNotesText": "Social Science Notes Text"
}


astronomy_metadata = {
    "astroType": "Astro Type",
    "astroFacility": "Astro Facility",
    "astroInstrument": "Astro Instrument",
    "astroObject": "Astro Object",
    "resolution.Spatial": "Spatial Resolution",
    "resolution.Spectral": "Spectral Resolution",
    "resolution.Temporal": "Temporal Resolution",
    "coverage.Spectral.Bandpass": "Spectral Bandpass",
    "coverage.Spectral.CentralWavelength": "Central Wavelength",
    "coverage.Spectral.MinimumWavelength": "Minimum Wavelength",
    "coverage.Spectral.MaximumWavelength": "Maximum Wavelength",
    "coverage.Temporal.StartTime": "Temporal Start Time",
    "coverage.Temporal.StopTime": "Temporal Stop Time",
    "coverage.Spatial": "Spatial Coverage",
    "coverage.Depth": "Depth",
    "coverage.ObjectDensity": "Object Density",
    "coverage.ObjectCount": "Object Count",
    "coverage.SkyFraction": "Sky Fraction",
    "coverage.Polarization": "Polarization",
    "redshiftType": "Redshift Type",
    "resolution.Redshift": "Redshift Resolution",
    "coverage.Redshift.MinimumValue": "Minimum Redshift",
    "coverage.Redshift.MaximumValue": "Maximum Redshift"
}


lifesciences_metadata = {
    "studyDesignType": "Study Design Type",
    "studyFactorType": "Study Factor Type",
    "studyAssayOrganism": "Assay Organism",
    "studyAssayOtherOrganism": "Other Assay Organism",
    "studyAssayMeasurementType": "Assay Measurement Type",
    "studyAssayOtherMeasurementType": "Other Assay Measurement Type",
    "studyAssayTechnologyType": "Assay Technology Type",
    "studyAssayPlatform": "Assay Platform",
    "studyAssayCellType": "Assay Cell Type"
}

journal_metadata = {
    "journalVolume": "Journal Volume",
    "journalIssue": "Journal Issue",
    "journalPubDate": "Journal Publication Date",
    "journalArticleType": "Journal Article Type"
}
customUAB_metadata={"reviewLibrary":"Library reviewing and publishing"}

from collections import defaultdict
import pandas as pd

# Initialize all selected metadata sets as empty
selected_data = set()
selected_citation = set()
selected_geospatial = set()
selected_social = set()
selected_astronomy = set()
selected_lifesciences = set()
selected_journal = set()
selected_customUAB = set()

# Combine all selected metadata keys
selected_metadata = (selected_data | selected_citation | selected_geospatial |
                     selected_social | selected_astronomy | selected_lifesciences |
                     selected_journal | selected_customUAB)

# Initialize lists
metadata_keys_list = []
metadata_values_list = []
list_doi = []
instancia = []
# states = []  # Uncomment if needed

# opcions should be defined earlier (set of selected institutions)
# config should be defined earlier (your configuration object)

for element in opcions:
    processor = DatasetProcessor(config, element)
    processor.create_list_datasets(element)
    sigles = element

    for i in processor.get_list_datasets():
        # Prepare empty lists for metadata keys and values
        data_keys, citation_keys, geo_keys, social_keys, astronomy_keys, biomedical_keys, journal_keys, customUAB_keys, state = [[] for _ in range(9)]
        data_values, citation_values, geo_values, social_values, astronomy_values, biomedical_values, journal_values, customUAB_values, state = [[] for _ in range(9)]
        data = []
        stateDataset = []

        # Export metadata for dataset 'i'
        export_metadata(config.get_api_url(), config.get_token(), i,
                        data_keys, data_values,
                        citation_keys, citation_values,
                        geo_keys, geo_values,
                        social_keys, social_values,
                        astronomy_keys, astronomy_values,
                        biomedical_keys, biomedical_values,
                        journal_keys, journal_values,
                        customUAB_keys, customUAB_values,
                        stateDataset)

        # Extract and arrange metadata into `data` list
        extract_metadata(data,
                         data_keys, data_values,
                         citation_keys, citation_values,
                         geo_keys, geo_values,
                         social_keys, social_values,
                         astronomy_keys, astronomy_values,
                         biomedical_keys, biomedical_values,
                         journal_keys, journal_values,
                         customUAB_keys, customUAB_values)

        # Create DataFrame from extracted metadata
        df = pd.DataFrame(data, columns=['Metadata', 'Value'])
        metadata_keys_aux = df['Metadata'].tolist()
        metadata_values_aux = df['Value'].tolist()

        metadata_keys_list.append(metadata_keys_aux)
        metadata_values_list.append(metadata_values_aux)
        instancia.append(sigles)
        list_doi.append(i)
        # states.append(stateDataset[0])  # Uncomment if you use states

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

# Aggregate metadata values
metadata = aggregate_metadata(metadata_keys_list, metadata_values_list, list_doi, selected_metadata)

# Create dictionary to build DataFrame
data = {
    'DOI': list_doi,
    'Institution': instancia
}

# Add selected metadata fields to data dictionary
for field in selected_metadata:
    data[field] = metadata[field]

# Build DataFrame
df = pd.DataFrame(data)

# Extract numeric part of DOI for sorting
df['DOI_Number'] = df['DOI'].str.extract(r'data(\d+)').astype(int)

# Sort by DOI_Number
df = df.sort_values(by='DOI_Number')

# Format DOI URLs
df['DOI'] = 'https://doi.org/10.34810/data' + df['DOI_Number'].astype(str)

# Drop DOI_Number column (optional)
df = df.drop(columns=['DOI_Number'])

# Save to Excel file
excel_filename = 'datasets_metadata.xlsx'
df.to_excel(excel_filename, index=False)

print(f"Metadata saved to {excel_filename}")

