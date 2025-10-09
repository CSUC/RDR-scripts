import os
import subprocess
import sys
import re


def read_secret(path):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except Exception as e:
        raise RuntimeError(f"Failed to read secret from {path}: {e}")


# Load token from Docker secret
token = read_secret("/run/secrets/DATAVERSE_TOKEN")  # Do not allow hardcoded credentials...

doi = os.environ.get("DOI")
lang = os.environ.get("LANG", "english")
base_url = os.environ.get("BASE_URL", "https://dataverse.csuc.cat/")
output_path = os.environ.get("OUTPUT_PATH")

# Example usage
print("✅ Token, DOI, LANG, BASE_URL and OUTPUT_PATH loaded successfully")
print(f"TOKEN (first 5 chars): {token[:5]}...")
print(f"DOI: {doi}")
print(f"LANG: {lang}")
print(f"BASE_URL: {base_url}")
print(f"OUTPUT_PATH: {output_path}")


# Function to install required packages
def install_packages():
    """
    Function to install or update necessary Python packages.
    """
    # Upgrade pip first
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "-q"])

    # Install the required libraries
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyDataverse", "-q"])


    print("Libraries have been downloaded or updated.")

# Install libraries if they are not installed already
try:
    import pyDataverse
except ImportError:
    print("Installing libraries...")
    install_packages()


# Initialize the Dataverse API 
from pyDataverse.api import NativeApi
native_api = NativeApi(base_url, token)

# Functions to extract values of a metadata JSON
def extract_value(data_dict):
    """
    Function to extract all keys and values from a JSON metadata dictionary.

    Parameters:
    - data_dict: dict. JSON metadata dictionary.

    Returns:
    - type_names: list. List of type names extracted from the metadata.
    - values: list. List of values extracted from the metadata.
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
        
def exportmetadata(base_url, token, doi,
                   citation_keys, citation_values,
                   geo_keys, geo_values,
                   social_keys, social_values,
                   astronomy_keys, astronomy_values,
                   biomedical_keys, biomedical_values,
                   journal_keys, journal_values,
                   computationalworkflow_keys, computationalworkflow_values,
                   LocalContextsCVoc_keys, LocalContextsCVoc_values,
                   darwincore_keys, darwincore_values):
    """
    Export metadata from a Dataverse dataset using its DOI.

    Parameters:
        (same as original, see above)

    Returns:
        None. Populates provided lists with extracted metadata.
    """
    from pyDataverse.api import NativeApi, DataAccessApi
    import os
    
    api = NativeApi(base_url, token)

    # Metadata blocks mapping: (block_name, keys_list, values_list)
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
                    if isinstance(item['value'], str):
                        try:
                            index = keys_list.index(item['typeName'])
                            values_list[index] = item['value']
                        except ValueError:
                            pass  # typeName wasn't added by extract_value

    except Exception as e:
        print(f"Error exporting metadata for DOI {doi}: {e}")

def filemetadata(base_url, token, doi, filemetadata_keys, filemetadata_values):
    """
    Function to extract metadata for files associated with a dataset identified by its DOI.

    Parameters:
    - base_url: str. Base URL of the Dataverse instance.
    - token: str. API token for authentication.
    - doi: str. DOI of the dataset.
    - filemetadata_keys: list. List to store file metadata keys.
    - filemetadata_values: list. List to store file metadata values.

    Returns:
    - None. Updates the provided lists with extracted file metadata.
    """
    from pyDataverse.api import NativeApi, DataAccessApi
    from pyDataverse.models import Dataverse

    # Instantiate API objects for accessing Dataverse
    api = NativeApi(base_url, token)
    data_api = DataAccessApi(base_url, token)

    try:
        # Retrieve dataset metadata
        dataset = api.get_dataset(doi)

        # Iterate through files and extract metadata
        for i in range(len(dataset.json()['data']['latestVersion']['files'])):
            filemetadata_resp = dataset.json()['data']['latestVersion']['files'][i]['dataFile']
            filemetadata_keys_aux = list(filemetadata_resp.keys())
            filemetadata_values_aux = list(filemetadata_resp.values())
            filemetadata_keys.append(filemetadata_keys_aux)
            filemetadata_values.append(filemetadata_values_aux)
    except KeyError:
        print('There was an error reading metadata for the files of the dataset: ' + doi)

def list_duplicates_of(seq, item):
    """
    Function to list indexes of duplicates of an item in a sequence.

    Parameters:
    - seq: list. Sequence to search for duplicates.
    - item: any. Item to search for duplicates.

    Returns:
    - locs: list. List of indexes where the item occurs more than once in the sequence.
    """
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item, start_at + 1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs

def find_keys(keys, specified_keys, values):
    """
    Function to find specified keys and their corresponding values in a list of keys and values.

    Parameters:
    - keys: list. List of keys.
    - specified_keys: list. List of specified keys to find.
    - values: list. List of values corresponding to the keys.

    Returns:
    - extracted_values: list. List of dictionaries containing extracted key-value pairs.
    """
    # Dictionary to store extracted values
    extracted_values = []
    # Dictionary to store current entry
    current_entry = {}
    # Set to keep track of found keys
    found_keys = set()
    # Iterate through keys and values
    for key, value in zip(keys, values):
        # Check if current key is in specified keys
        if key in specified_keys:
            current_entry[key] = value
            found_keys.add(key)
            # If all specified keys are found, add entry to extracted_values
            if len(found_keys) == len(specified_keys):
                extracted_values.append(current_entry)
                current_entry = {}  # Reset current entry
                found_keys.clear()  # Clear found keys set for next entry
    return extracted_values

#Function to create Readme File in a path
def createreadme(base_url, token, doi, language,
                 citation_keys, citation_values,
                 geo_keys, geo_values,
                 social_keys, social_values,
                 astronomy_keys, astronomy_values,
                 biomedical_keys, biomedical_values,
                 journal_keys, journal_values,
                 computationalworkflow_keys, computationalworkflow_values,
                 LocalContextsCVoc_keys,LocalContextsCVoc_values,
                 darwincore_keys, darwincore_values,
                 filemetadata_keys, filemetadata_values):
    """
    Function to create a readme file for a dataset.

    Parameters:
    - base_url: str. Base URL of the Dataverse instance.
    - token: str. API token for authentication.
    - doi: str. DOI of the dataset.
    - citation_keys: list. List of citation metadata keys.
    - citation_values: list. List of citation metadata values.
    - geo_keys: list. List of geospatial metadata keys.
    - geo_values: list. List of geospatial metadata values.
    - social_keys: list. List of social science metadata keys.
    - social_values: list. List of social science metadata values.
    - astronomy_keys: list. List of astronomy metadata keys.
    - astronomy_values: list. List of astronomy metadata values.
    - biomedical_keys: list. List of biomedical metadata keys.
    - biomedical_values: list. List of biomedical metadata values.
    - journal_keys: list. List of journal metadata keys.
    - journal_values: list. List of journal metadata values.
    - filemetadata_keys: list. List of file metadata keys.
    - filemetadata_values: list. List of file metadata values.
    """

    # Import necessary libraries
    from pyDataverse.api import NativeApi, DataAccessApi
    from pyDataverse.models import Dataverse
    import os

    # Instantiate API objects for accessing Dataverse
    api = NativeApi(base_url, token)
    data_api = DataAccessApi(base_url, token)

    # Retrieve dataset metadata
    dataset = api.get_dataset(doi)

    # Extract path from DOI if not provided
    if output_path is None:
        path = doi.replace("doi:10.34810/", "")
    else:
        path = output_path


    try:
        # Create directory if it does not exist
        os.mkdir(path)
    except OSError:
        print("Directory " + path + ' already exists. The Readme will be saved in this directory.')
    translation_metadata = {
        "english": {
            "title": "Dataset Title",
            "PreviousDatasetPersistentID": "Previous Dataset Persistent ID",
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
            "keywordValue": "Keyword Value",
            "keywordTermURI": "Keyword Term URI",
            "keywordVocabulary": "Keyword Vocabulary",
            "keywordVocabularyURI": "Keyword Vocabulary URI",
            "topicClassValue": "Topic Class Value",
            "topicClassVocab": "Topic Class Vocabulary",
            "topicClassVocabURI": "Topic Class Vocabulary URI",
            "publicationRelationType": "Publication Relation Type",
            "publicationCitation": "Publication Citation",
            "publicationIDType": "Publication ID Type",
            "publicationIDNumber": "Publication ID Number",
            "publicationURL": "Publication URL",
            "notesText": "Notes Text",
            "language": "Language",
            "producerName": "Producer Name",
            "producerAffiliation": "Producer Affiliation",
            "producerAbbreviation": "Producer Abbreviation",
            "producerURL": "Producer URL",
            "producerLogoURL": "Producer Logo URL",
            "productionDate": "Production Date",
            "productionPlace": "Production Place",
            "contributorType": "Contributor Type",
            "contributorName": "Contributor Name",
            "grantNumberAgency": "Grant Number Agency",
            "grantNumberValue": "Grant Number Value",
            "distributorName": "Distributor Name",
            "distributorAffiliation": "Distributor Affiliation",
            "distributorAbbreviation": "Distributor Abbreviation",
            "distributorURL": "Distributor URL",
            "distributorLogoURL": "Distributor Logo URL",
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
            "accessToSources": "Access to Sources",
            "country": "Country",
            "state": "State",
            "city": "City",
            "otherGeographicCoverage": "Other Geographic Coverage",
            "geographicUnit": "Geographic Unit",
            "westLongitude": "West Longitude",
            "eastLongitude": "East Longitude",
            "northLatitude": "North Latitude",
            "southLatitude": "South Latitude",
            "unitOfAnalysis": "Unit of Analysis",
            "universe": "Universe",
            "timeMethod": "Time Method",
            "dataCollector": "Data Collector",
            "collectorTraining": "Collector Training",
            "frequencyOfDataCollection": "Frequency of Data Collection",
            "samplingProcedure": "Sampling Procedure",
            "targetSampleActualSize": "Target Sample Actual Size",
            "targetSampleSizeFormula": "Target Sample Size Formula",
            "deviationsFromSampleDesign": "Deviations from Sample Design",
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
            "socialScienceNotesText": "Social Science Notes Text",
            "astroType": "Astro Type",
            "astroFacility": "Astro Facility",
            "astroInstrument": "Astro Instrument",
            "astroObject": "Astro Object",
            "resolution.Spatial": "Resolution Spatial",
            "resolution.Spectral": "Resolution Spectral",
            "resolution.Temporal": "Resolution Temporal",
            "coverage.Spectral.Bandpass": "Coverage Spectral Bandpass",
            "coverage.Spectral.CentralWavelength": "Coverage Spectral Central Wavelength",
            "coverage.Spectral.MinimumWavelength": "Coverage Spectral Minimum Wavelength",
            "coverage.Spectral.MaximumWavelength": "Coverage Spectral Maximum Wavelength",
            "coverage.Temporal.StartTime": "Coverage Temporal Start Time",
            "coverage.Temporal.StopTime": "Coverage Temporal Stop Time",
            "coverage.Spatial": "Coverage Spatial",
            "coverage.Depth": "Coverage Depth",
            "coverage.ObjectDensity": "Coverage Object Density",
            "coverage.ObjectCount": "Coverage Object Count",
            "coverage.SkyFraction": "Coverage Sky Fraction",
            "coverage.Polarization": "Coverage Polarization",
            "redshiftType": "Redshift Type",
            "resolution.Redshift": "Resolution Redshift",
            "coverage.Redshift.MinimumValue": "Coverage Redshift Minimum Value",
            "coverage.Redshift.MaximumValue": "Coverage Redshift Maximum Value",
            "studyDesignType": "Study Design Type",
            "studyOtherDesignType": "Study Other Design Type",
            "studyFactorType": "Study Factor Type",
            "studyOtherFactorType": "Study Other Factor Type",
            "studyAssayOrganism": "Study Assay Organism",
            "studyAssayOtherOrganism": "Study Assay Other Organism",
            "studyAssayMeasurementType": "Study Assay Measurement Type",
            "studyAssayOtherMeasurmentType": "Study Assay Other Measurement Type",
            "studyAssayTechnologyType": "Study Assay Technology Type",
            "studyAssayOtherTechnologyType": "Study Assay Other Technology Type",
            "studyAssayPlatform": "Study Assay Platform",
            "studyAssayOtherPlatform": "Study Assay Other Platform",
            "studyAssayCellType": "Study Assay Cell Type",
            "journalVolume": "Journal Volume",
            "journalIssue": "Journal Issue",
            "journalPubDate": "Journal Publication Date",
            "journalArticleType": "Journal Article Type",
            "workflowType": "Workflow Type",
            "workflowCodeRepository": "Workflow Code Repository",
            "workflowDocumentation": "Workflow Documentation",
            "LCProjectUrl": "Local Contexts Project URL"
        },
        "spanish": {
            "title": "Título del Conjunto de Datos",
            "PreviousDatasetPersistentID": "ID Persistente del Conjunto de Datos Anterior",
            "subtitle": "Subtítulo",
            "alternativeTitle": "Título Alternativo",
            "alternativeURL": "URL Alternativa",
            "otherIdAgency": "Agencia de Otro ID",
            "otherIdValue": "Valor de Otro ID",
            "authorName": "Nombre del/de la autor(a)",
            "authorAffiliation": "Afiliación del/de la autor(a)",
            "authorIdentifierScheme": "Esquema de Identificador del/de la autor(a)",
            "authorIdentifier": "Identificador del/de la autor(a)",
            "datasetContactName": "Nombre del/de la contacto del conjunto de datos",
            "datasetContactAffiliation": "Afiliación del/de la contacto del conjunto de datos",
            "datasetContactEmail": "Correo electrónico del/de la contacto del conjunto de datos",
            "dsDescriptionValue": "Valor de la descripción",
            "dsDescriptionDate": "Fecha de la descripción",
            "subject": "Tema",
            "keywordValue": "Valor de la palabra clave",
            "keywordTermURI": "URI del término clave",
            "keywordVocabulary": "Vocabulario de palabra clave",
            "keywordVocabularyURI": "URI del vocabulario de palabra clave",
            "topicClassValue": "Valor de la clasificación temática",
            "topicClassVocab": "Vocabulario de clasificación temática",
            "topicClassVocabURI": "URI del vocabulario de clasificación temática",
            "publicationRelationType": "Tipo de relación de la publicación",
            "publicationCitation": "Cita de la publicación",
            "publicationIDType": "Tipo de ID de publicación",
            "publicationIDNumber": "Número de ID de publicación",
            "publicationURL": "URL de la publicación",
            "notesText": "Texto de notas",
            "language": "Idioma",
            "producerName": "Nombre del/de la productor(a)",
            "producerAffiliation": "Afiliación del/de la productor(a)",
            "producerAbbreviation": "Abreviatura del/de la productor(a)",
            "producerURL": "URL del/de la productor(a)",
            "producerLogoURL": "URL del logo del/de la productor(a)",
            "productionDate": "Fecha de producción",
            "productionPlace": "Lugar de producción",
            "contributorType": "Tipo de colaborador(a)",
            "contributorName": "Nombre del/de la colaborador(a)",
            "grantNumberAgency": "Agencia del número de subvención",
            "grantNumberValue": "Valor del número de subvención",
            "distributorName": "Nombre del/de la distribuidor(a)",
            "distributorAffiliation": "Afiliación del/de la distribuidor(a)",
            "distributorAbbreviation": "Abreviatura del/de la distribuidor(a)",
            "distributorURL": "URL del/de la distribuidor(a)",
            "distributorLogoURL": "URL del logo del/de la distribuidor(a)",
            "distributionDate": "Fecha de distribución",
            "depositor": "Depositante",
            "dateOfDeposit": "Fecha de depósito",
            "timePeriodCoveredStart": "Inicio del período cubierto",
            "timePeriodCoveredEnd": "Fin del período cubierto",
            "dateOfCollectionStart": "Inicio de la recolección de datos",
            "dateOfCollectionEnd": "Fin de la recolección de datos",
            "kindOfData": "Tipo de datos",
            "seriesName": "Nombre de la serie",
            "seriesInformation": "Información de la serie",
            "softwareName": "Nombre del software",
            "softwareVersion": "Versión del software",
            "relatedMaterial": "Material relacionado",
            "relatedDatasets": "Conjuntos de datos relacionados",
            "otherReferences": "Otras referencias",
            "dataSources": "Fuentes de datos",
            "originOfSources": "Origen de las fuentes",
            "characteristicOfSources": "Características de las fuentes",
            "accessToSources": "Acceso a las fuentes",
            "country": "País",
            "state": "Estado",
            "city": "Ciudad",
            "otherGeographicCoverage": "Otra cobertura geográfica",
            "geographicUnit": "Unidad geográfica",
            "westLongitude": "Longitud oeste",
            "eastLongitude": "Longitud este",
            "northLatitude": "Latitud norte",
            "southLatitude": "Latitud sur",
            "unitOfAnalysis": "Unidad de análisis",
            "universe": "Universo",
            "timeMethod": "Método temporal",
            "dataCollector": "Recolector(a) de datos",
            "collectorTraining": "Capacitación del/de la recolector(a)",
            "frequencyOfDataCollection": "Frecuencia de recolección de datos",
            "samplingProcedure": "Procedimiento de muestreo",
            "targetSampleActualSize": "Tamaño real de la muestra objetivo",
            "targetSampleSizeFormula": "Fórmula del tamaño de la muestra objetivo",
            "deviationsFromSampleDesign": "Desviaciones del diseño muestral",
            "collectionMode": "Modo de recolección",
            "researchInstrument": "Instrumento de investigación",
            "dataCollectionSituation": "Situación de recolección de datos",
            "actionsToMinimizeLoss": "Acciones para minimizar la pérdida",
            "controlOperations": "Operaciones de control",
            "weighting": "Ponderación",
            "cleaningOperations": "Operaciones de limpieza",
            "datasetLevelErrorNotes": "Notas de error a nivel de conjunto de datos",
            "responseRate": "Tasa de respuesta",
            "samplingErrorEstimates": "Estimaciones del error de muestreo",
            "otherDataAppraisal": "Otra evaluación de datos",
            "socialScienceNotesType": "Tipo de notas de ciencias sociales",
            "socialScienceNotesSubject": "Tema de las notas de ciencias sociales",
            "socialScienceNotesText": "Texto de las notas de ciencias sociales",
            "astroType": "Tipo de observación astronómica",
            "astroFacility": "Instalación astronómica",
            "astroInstrument": "Instrumento astronómico",
            "astroObject": "Objeto astronómico",
            "resolution.Spatial": "Resolución espacial",
            "resolution.Spectral": "Resolución espectral",
            "resolution.Temporal": "Resolución temporal",
            "coverage.Spectral.Bandpass": "Cobertura espectral - Banda de paso",
            "coverage.Spectral.CentralWavelength": "Cobertura espectral - Longitud de onda central",
            "coverage.Spectral.MinimumWavelength": "Cobertura espectral - Longitud de onda mínima",
            "coverage.Spectral.MaximumWavelength": "Cobertura espectral - Longitud de onda máxima",
            "coverage.Temporal.StartTime": "Cobertura temporal - Hora de inicio",
            "coverage.Temporal.StopTime": "Cobertura temporal - Hora de finalización",
            "coverage.Spatial": "Cobertura espacial",
            "coverage.Depth": "Cobertura de profundidad",
            "coverage.ObjectDensity": "Densidad de objetos",
            "coverage.ObjectCount": "Cantidad de objetos",
            "coverage.SkyFraction": "Fracción del cielo",
            "coverage.Polarization": "Polarización",
            "redshiftType": "Tipo de corrimiento al rojo",
            "resolution.Redshift": "Resolución del corrimiento al rojo",
            "coverage.Redshift.MinimumValue": "Cobertura corrimiento al rojo - Valor mínimo",
            "coverage.Redshift.MaximumValue": "Cobertura corrimiento al rojo - Valor máximo",
            "studyDesignType": "Tipo de diseño del estudio",
            "studyOtherDesignType": "Otro tipo de diseño del estudio",
            "studyFactorType": "Tipo de factor del estudio",
            "studyOtherFactorType": "Otro tipo de factor del estudio",
            "studyAssayOrganism": "Organismo de ensayo del estudio",
            "studyAssayOtherOrganism": "Otro organismo de ensayo del estudio",
            "studyAssayMeasurementType": "Tipo de medición del ensayo",
            "studyAssayOtherMeasurmentType": "Otro tipo de medición del ensayo",
            "studyAssayTechnologyType": "Tipo de tecnología del ensayo",
            "studyAssayOtherTechnologyType": "Otro tipo de tecnología del ensayo",
            "studyAssayPlatform": "Plataforma del ensayo",
            "studyAssayOtherPlatform": "Otra plataforma del ensayo",
            "studyAssayCellType": "Tipo de célula del ensayo",
            "journalVolume": "Volumen de la revista",
            "journalIssue": "Número de la revista",
            "journalPubDate": "Fecha de publicación de la revista",
            "journalArticleType": "Tipo de artículo de la revista",
            "workflowType": "Tipo de flujo de trabajo",
            "workflowCodeRepository": "Repositorio de código del flujo de trabajo",
            "workflowDocumentation": "Documentación del flujo de trabajo",
            "LCProjectUrl": "URL del proyecto Local Contexts"
        },
        "catalan": {
            "title": "Títol del Conjunt de Dades",
            "PreviousDatasetPersistentID": "ID Persistent del Conjunt de Dades Anterior",
            "subtitle": "Subtítol",
            "alternativeTitle": "Títol Alternatiu",
            "alternativeURL": "URL Alternativa",
            "otherIdAgency": "Agència d'un Altre ID",
            "otherIdValue": "Valor d'un Altre ID",
            "authorName": "Nom de l'autor(a)",
            "authorAffiliation": "Afiliació de l'autor(a)",
            "authorIdentifierScheme": "Esquema d'identificador de l'autor(a)",
            "authorIdentifier": "Identificador de l'autor(a)",
            "datasetContactName": "Nom del/de la contacte del conjunt de dades",
            "datasetContactAffiliation": "Afiliació del/de la contacte del conjunt de dades",
            "datasetContactEmail": "Correu electrònic del/de la contacte del conjunt de dades",
            "dsDescriptionValue": "Valor de la descripció",
            "dsDescriptionDate": "Data de la descripció",
            "subject": "Tema",
            "keywordValue": "Valor de la paraula clau",
            "keywordTermURI": "URI del terme clau",
            "keywordVocabulary": "Vocabulari de paraula clau",
            "keywordVocabularyURI": "URI del vocabulari de paraula clau",
            "topicClassValue": "Valor de la classificació temàtica",
            "topicClassVocab": "Vocabulari de classificació temàtica",
            "topicClassVocabURI": "URI del vocabulari de classificació temàtica",
            "publicationRelationType": "Tipus de relació de la publicació",
            "publicationCitation": "Citació de la publicació",
            "publicationIDType": "Tipus d'ID de publicació",
            "publicationIDNumber": "Número d'ID de publicació",
            "publicationURL": "URL de la publicació",
            "notesText": "Text de notes",
            "language": "Llengua",
            "producerName": "Nom del/de la productor(a)",
            "producerAffiliation": "Afiliació del/de la productor(a)",
            "producerAbbreviation": "Abreviatura del/de la productor(a)",
            "producerURL": "URL del/de la productor(a)",
            "producerLogoURL": "URL del logotip del/de la productor(a)",
            "productionDate": "Data de producció",
            "productionPlace": "Lloc de producció",
            "contributorType": "Tipus de col·laborador(a)",
            "contributorName": "Nom del/de la col·laborador(a)",
            "grantNumberAgency": "Agència del número de subvenció",
            "grantNumberValue": "Valor del número de subvenció",
            "distributorName": "Nom del/de la distribuïdor(a)",
            "distributorAffiliation": "Afiliació del/de la distribuïdor(a)",
            "distributorAbbreviation": "Abreviatura del/de la distribuïdor(a)",
            "distributorURL": "URL del/de la distribuïdor(a)",
            "distributorLogoURL": "URL del logotip del/de la distribuïdor(a)",
            "distributionDate": "Data de distribució",
            "depositor": "Dipositant",
            "dateOfDeposit": "Data de dipòsit",
            "timePeriodCoveredStart": "Inici del període cobert",
            "timePeriodCoveredEnd": "Final del període cobert",
            "dateOfCollectionStart": "Inici de la recollida de dades",
            "dateOfCollectionEnd": "Final de la recollida de dades",
            "kindOfData": "Tipus de dades",
            "seriesName": "Nom de la sèrie",
            "seriesInformation": "Informació de la sèrie",
            "softwareName": "Nom del programari",
            "softwareVersion": "Versió del programari",
            "relatedMaterial": "Material relacionat",
            "relatedDatasets": "Conjunts de dades relacionats",
            "otherReferences": "Altres referències",
            "dataSources": "Fonts de dades",
            "originOfSources": "Origen de les fonts",
            "characteristicOfSources": "Característiques de les fonts",
            "accessToSources": "Accés a les fonts",
            "country": "País",
            "state": "Estat",
            "city": "Ciutat",
            "otherGeographicCoverage": "Altra cobertura geogràfica",
            "geographicUnit": "Unitat geogràfica",
            "westLongitude": "Longitud oest",
            "eastLongitude": "Longitud est",
            "northLatitude": "Latitud nord",
            "southLatitude": "Latitud sud",
            "unitOfAnalysis": "Unitat d'anàlisi",
            "universe": "Univers",
            "timeMethod": "Mètode temporal",
            "dataCollector": "Recollidor(a) de dades",
            "collectorTraining": "Formació del/de la recollidor(a)",
            "frequencyOfDataCollection": "Freqüència de recollida de dades",
            "samplingProcedure": "Procediment de mostreig",
            "targetSampleActualSize": "Mida real de la mostra objectiu",
            "targetSampleSizeFormula": "Fòrmula de la mida de la mostra objectiu",
            "deviationsFromSampleDesign": "Desviacions del disseny mostral",
            "collectionMode": "Mode de recollida",
            "researchInstrument": "Instrument d'investigació",
            "dataCollectionSituation": "Situació de recollida de dades",
            "actionsToMinimizeLoss": "Accions per minimitzar la pèrdua",
            "controlOperations": "Operacions de control",
            "weighting": "Ponderació",
            "cleaningOperations": "Operacions de neteja",
            "datasetLevelErrorNotes": "Notes d'error a nivell de conjunt de dades",
            "responseRate": "Taxa de resposta",
            "samplingErrorEstimates": "Estimacions de l'error de mostreig",
            "otherDataAppraisal": "Altres avaluacions de dades",
            "socialScienceNotesType": "Tipus de notes de ciències socials",
            "socialScienceNotesSubject": "Tema de les notes de ciències socials",
            "socialScienceNotesText": "Text de les notes de ciències socials",
            "astroType": "Tipus d'observació astronòmica",
            "astroFacility": "Instal·lació astronòmica",
            "astroInstrument": "Instrument astronòmic",
            "astroObject": "Objecte astronòmic",
            "resolution.Spatial": "Resolució espacial",
            "resolution.Spectral": "Resolució espectral",
            "resolution.Temporal": "Resolució temporal",
            "coverage.Spectral.Bandpass": "Cobertura espectral - Banda de pas",
            "coverage.Spectral.CentralWavelength": "Cobertura espectral - Longitud d'ona central",
            "coverage.Spectral.MinimumWavelength": "Cobertura espectral - Longitud d'ona mínima",
            "coverage.Spectral.MaximumWavelength": "Cobertura espectral - Longitud d'ona màxima",
            "coverage.Temporal.StartTime": "Cobertura temporal - Hora d'inici",
            "coverage.Temporal.StopTime": "Cobertura temporal - Hora de finalització",
            "coverage.Spatial": "Cobertura espacial",
            "coverage.Depth": "Cobertura de profunditat",
            "coverage.ObjectDensity": "Densitat d'objectes",
            "coverage.ObjectCount": "Quantitat d'objectes",
            "coverage.SkyFraction": "Fracció del cel",
            "coverage.Polarization": "Polarització",
            "redshiftType": "Tipus de desplaçament cap al vermell",
            "resolution.Redshift": "Resolució del desplaçament cap al vermell",
            "coverage.Redshift.MinimumValue": "Cobertura desplaçament cap al vermell - Valor mínim",
            "coverage.Redshift.MaximumValue": "Cobertura desplaçament cap al vermell - Valor màxim",
            "studyDesignType": "Tipus de disseny de l'estudi",
            "studyOtherDesignType": "Altres tipus de disseny de l'estudi",
            "studyFactorType": "Tipus de factor de l'estudi",
            "studyOtherFactorType": "Altres tipus de factor de l'estudi",
            "studyAssayOrganism": "Organisme d'assaig de l'estudi",
            "studyAssayOtherOrganism": "Altres organismes d'assaig de l'estudi",
            "studyAssayMeasurementType": "Tipus de mesura de l'assaig",
            "studyAssayOtherMeasurmentType": "Altres tipus de mesura de l'assaig",
            "studyAssayTechnologyType": "Tipus de tecnologia de l'assaig",
            "studyAssayOtherTechnologyType": "Altres tecnologies de l'assaig",
            "studyAssayPlatform": "Plataforma de l'assaig",
            "studyAssayOtherPlatform": "Altres plataformes de l'assaig",
            "studyAssayCellType": "Tipus de cèl·lula de l'assaig",
            "journalVolume": "Volum de la revista",
            "journalIssue": "Número de la revista",
            "journalPubDate": "Data de publicació de la revista",
            "journalArticleType": "Tipus d'article de la revista",
            "workflowType": "Tipus de flux de treball",
            "workflowCodeRepository": "Repositori de codi del flux de treball",
            "workflowDocumentation": "Documentació del flux de treball",
            "LCProjectUrl": "URL del projecte Local Contexts"
        }
    }
    translation_titles = {
        'english': {
            # Section titles
            'GENERAL INFORMATION': 'GENERAL INFORMATION',
            'DESCRIPTION': 'DESCRIPTION',
            'ACCESS INFORMATION': 'ACCESS INFORMATION',
            'GEOSPATIAL METADATA': 'GEOSPATIAL METADATA',
            'SOCIAL SCIENCE AND HUMANITIES METADATA': 'SOCIAL SCIENCE AND HUMANITIES METADATA',
            'ASTRONOMY AND ASTROPHYSICS METADATA': 'ASTRONOMY AND ASTROPHYSICS METADATA',
            'LIFE SCIENCES METADATA': 'LIFE SCIENCES METADATA',
            'JOURNAL METADATA': 'JOURNAL METADATA',
            'COMPUTATIONAL WORKFLOW METADATA': 'COMPUTATIONAL WORKFLOW METADATA',
            'LOCAL CONTEXTS METADATA': 'LOCAL CONTEXTS METADATA',

            # Group metadata titles
            'Authorship': 'Authorship',
            'Dataset contact': 'Dataset contact',
            'Keyword': 'Keywords',
            'Topic classification': 'Topic classification',
            'Producer': 'Producer',
            'Contributor': 'Contributor',
            'Grant information': 'Grant information',
            'Distributor': 'Distributor',
            'Creative Commons License of the dataset':'Creative Commons License of the dataset',
            'Dataset DOI':'Dataset DOI',
            'Related publication': 'Related publication',
            'Geographical location/s of data collection': 'Geographical location/s of data collection',
            'Time period covered (single date or date range)': 'Time period covered (single date or date range)',
            'Date of data collection (single date or date range)': 'Date of data collection (single date or date range)',
            'Target Sample Size': 'Target Sample Size',
            'Notes': 'Notes',
            'Journal': 'Journal',
            'Bandpass': 'Bandpass',
            'Central Wavelength (m)': 'Central Wavelength (m)',
            'Wavelength Range': 'Wavelength Range',
            'Dataset Date Range': 'Dataset Date Range',
            'Publication Date': 'Publication Date',
            'Series': 'Series',
            'Software': 'Software',
            'Time period covered (single date or date range)': 'Time period covered (single date or date range)',
            "FILE OVERVIEW": "FILE OVERVIEW",
            "File name": "File name",
            "Description": "Description",
            "File format": "File format"
        },

        'spanish': {
            # Section titles
            'GENERAL INFORMATION': 'INFORMACIÓN GENERAL',
            'DESCRIPTION': 'DESCRIPCIÓN',
            'ACCESS INFORMATION': 'INFORMACIÓN DE ACCESO',
            'GEOSPATIAL METADATA': 'METADATOS GEOSPACIALES',
            'SOCIAL SCIENCE AND HUMANITIES METADATA': 'METADATOS DE CIENCIAS SOCIALES Y HUMANIDADES',
            'ASTRONOMY AND ASTROPHYSICS METADATA': 'METADATOS DE ASTRONOMÍA Y ASTROFÍSICA',
            'LIFE SCIENCES METADATA': 'METADATOS DE CIENCIAS DE LA VIDA',
            'JOURNAL METADATA': 'METADATOS DE REVISTA',
            'COMPUTATIONAL WORKFLOW METADATA': 'METADATOS DE FLUJOS DE TRABAJO COMPUTACIONALES',
            'LOCAL CONTEXTS METADATA': 'METADATOS DE CONTEXTOS LOCALES',

            # Group metadata titles
            'Authorship': 'Autoría',
            'Dataset contact': 'Contacto del conjunto de datos',
            'Keyword': 'Palabras clave',
            'Topic classification': 'Clasificación temática',
            'Producer': 'Productor(a)',
            'Contributor': 'Colaborador(a)',
            'Grant information': 'Información sobre subvenciones',
            'Distributor': 'Distribuidor(a)',
            'Creative Commons License of the dataset':'Licencia Creative Commons del dataset',
            'Dataset DOI':'DOI del dataset',
            'Related publication': 'Publicación relacionada',
            'Geographical location/s of data collection': 'Ubicación(es) geográfica(s) de la recopilación de datos',
            'Time period covered (single date or date range)': 'Periodo de tiempo cubierto (fecha única o rango de fechas)',
            'Date of data collection (single date or date range)': 'Fecha de recogida de datos (fecha única o rango de fechas)',
            'Target Sample Size': 'Tamaño objetivo de la muestra',
            'Notes': 'Notas',
            'Journal': 'Revista',
            'Bandpass': 'Banda de paso',
            'Central Wavelength (m)': 'Longitud de onda central (m)',
            'Wavelength Range': 'Rango de longitud de onda',
            'Dataset Date Range': 'Rango de fechas del conjunto de datos',
            'Publication Date': 'Fecha de publicación',
            'Series': 'Serie',
            'Software': 'Software',
            'Time period covered (single date or date range)': 'Periodo de tiempo cubierto (fecha única o rango de fechas)',
            "FILE OVERVIEW": "RESUMEN DEL ARCHIVO",
            "File name": "Nombre del archivo",
            "Description": "Descripción",
            "File format": "Formato del archivo"
        },

        'catalan': {
            # Section titles
            'GENERAL INFORMATION': 'INFORMACIÓ GENERAL',
            'DESCRIPTION': 'DESCRIPCIÓ',
            'ACCESS INFORMATION': "INFORMACIÓ D'ACCÉS",
            'GEOSPATIAL METADATA': 'METADADES GEOSPACIALS',
            'SOCIAL SCIENCE AND HUMANITIES METADATA': 'METADADES DE CIÈNCIES SOCIALS I HUMANITATS',
            'ASTRONOMY AND ASTROPHYSICS METADATA': 'METADADES D’ASTRONOMIA I ASTROFÍSICA',
            'LIFE SCIENCES METADATA': 'METADADES DE CIÈNCIES DE LA VIDA',
            'JOURNAL METADATA': 'METADADES DE REVISTA',
            'COMPUTATIONAL WORKFLOW METADATA': 'METADADES DE FLUXOS DE TREBALL COMPUTACIONALS',
            'LOCAL CONTEXTS METADATA': 'METADADES DE CONTEXTOS LOCALS',

            # Group metadata titles
            'Authorship': 'Autoria',
            'Dataset contact': 'Contacte del conjunt de dades',
            'Keyword': 'Paraules clau',
            'Topic classification': 'Classificació temàtica',
            'Producer': 'Productor(a)',
            'Contributor': 'Col·laborador(a)',
            'Grant information': 'Informació sobre subvencions',
            'Distributor': 'Distribuïdor(a)',
            'Creative Commons License of the dataset':'Llicència Creative Commons del dataset',
            'Dataset DOI':'DOI del dataset',
            'Related publication': 'Publicació relacionada',
            'Geographical location/s of data collection': 'Ubicació(ons) geogràfica(s) de la recopilació de dades',
            'Time period covered (single date or date range)': 'Període de temps cobert (data única o rang de dates)',
            'Date of data collection (single date or date range)': 'Data de recollida de dades (data única o rang de dates)',
            'Target Sample Size': 'Mida objectiu de la mostra',
            'Notes': 'Notes',
            'Journal': 'Revista',
            'Bandpass': 'Banda de pas',
            'Central Wavelength (m)': 'Longitud d’ona central (m)',
            'Wavelength Range': 'Rang de longituds d’ona',
            'Dataset Date Range': 'Rang de dates del conjunt de dades',
            'Publication Date': 'Data de publicació',
            'Series': 'Sèrie',
            'Software': 'Programari',
            'Time period covered (single date or date range)': 'Període de temps cobert (data única o rang de dates)',
            "FILE OVERVIEW": "RESUM DEL FITXER",
            "File name": "Nom del fitxer",
            "File description": "Descripció",
            "File format": "Format del fitxer"
        }
    }

    #Functions to translate metadata and titles
    def translate_key(key, lang='en', dict_type='metadata'):
      """
      Translate metadata key or titles based on language code.
      Fallback: if key not found, return the original key.
      """
      if dict_type == 'metadata':
          # Use the metadata translations dictionary
          return translation_metadata.get(lang, {}).get(key, key)
      elif dict_type == 'title':
          # Use the titles translations dictionary
          return translation_titles.get(lang, {}).get(key, key)
      else:
          return key

    # Code to begin to write Readme
    with open(path + '/' + 'Readme.txt', 'w', encoding='utf-8') as f:

        # Functiosn to write metadata depending if they are single or multiples

        def write_single_key_section(f, cont, key, keys, values, lang, section_title_key):
            #Writes a section to the output file for a metadata field that occurs once or multiple times under the same key.
            if key in keys:
                cont += 1
                f.write(f"{cont}.  {translate_key(section_title_key, lang, dict_type='metadata')}:\n")
                indexes = list_duplicates_of(keys, key)
                for i in indexes:
                    f.write('\t' + values[i])
                    if i != indexes[-1]:
                        f.write('\n ')
                f.write('\n\n')
            return cont

        def write_grouped_keys_section(f, cont, group_keys, keys, values, lang, section_title_key):
            #Writes a section for a group of related metadata fields, each with its translated label.
            if any(k in keys for k in group_keys):
                cont += 1
                f.write(f"{cont}.  {translate_key(section_title_key, lang, dict_type='title')}:\n")
                specified_keys = [k for k in group_keys if k in keys]
                extracted_values = find_keys(keys, specified_keys, values)
                for entry in extracted_values:
                    for key, value in entry.items():
                        translated_key = translate_key(key, lang, dict_type='metadata')
                        f.write(f'\t{translated_key}: {value}\n')
                    f.write('\n')
            return cont

        def write_dataset_level_key(f, cont, key, dataset, lang, section_title_key):
            # Writes a section for a single top-level metadata field from the dataset (not per file).
            if key in dataset.get('data', {}):
                cont += 1
                f.write(f"{cont}.  {translate_key(section_title_key, lang, dict_type='metadata')}:\n")
                f.write('\t' + dataset['data'][key] + '\n\n')
            return cont

        # Sample usage of the refactored functions in main logic
        title = translate_key('GENERAL INFORMATION', lang, dict_type='title')
        f.write(title + '\n' + '-' * len(title) + '\n')
        cont = 0
        cont = write_single_key_section(f, cont, 'PreviousDatasetPersistentID', citation_keys, citation_values, lang, 'PreviousDatasetPersistentID')
        cont = write_single_key_section(f, cont, 'title', citation_keys, citation_values, lang, 'title')
        cont = write_grouped_keys_section(f, cont, ['authorName', 'authorAffiliation', 'authorIdentifierScheme', 'authorIdentifier'], citation_keys, citation_values, lang, 'Authorship')
        cont = write_grouped_keys_section(f, cont, ['datasetContactName', 'datasetContactAffiliation', 'datasetContactEmail'], citation_keys, citation_values, lang, 'Dataset contact')

        # Description metadata
        title = translate_key('DESCRIPTION', lang, dict_type='title')
        f.write(title + '\n' + '-' * len(title) + '\n')
        cont = 0
        cont = write_single_key_section(f, cont, 'language', citation_keys, citation_values, lang, 'language')
        cont = write_single_key_section(f, cont, 'dsDescriptionValue', citation_keys, citation_values, lang, 'dsDescriptionValue')
        cont = write_single_key_section(f, cont, 'subject', citation_keys, citation_values, lang, 'subject')
        cont = write_grouped_keys_section(f, cont, ['keywordValue', 'keywordVocabulary', 'keywordVocabularyURI'], citation_keys, citation_values, lang, 'Keyword')
        cont = write_grouped_keys_section(f, cont, ['topicClassValue', 'topicClassVocab', 'topicClassVocabURI'], citation_keys, citation_values, lang, 'Topic classification')
        cont = write_single_key_section(f, cont, 'notesText', citation_keys, citation_values, lang, 'notesText')
        cont = write_grouped_keys_section(f, cont, ['producerName', 'producerAffiliation', 'producerAbbreviation', 'producerURL'], citation_keys, citation_values, lang, 'Producer')
        cont = write_single_key_section(f, cont, 'productionDate', citation_keys, citation_values, lang, 'productionDate')
        cont = write_single_key_section(f, cont, 'productionPlace', citation_keys, citation_values, lang, 'productionPlace')
        cont = write_grouped_keys_section(f, cont, ['contributorType', 'contributorName'], citation_keys, citation_values, lang, 'Contributor')
        cont = write_grouped_keys_section(f, cont, ['grantNumberAgency', 'grantNumberValue'], citation_keys, citation_values, lang, 'Grant information')
        cont = write_grouped_keys_section(f, cont, ['distributorName', 'distributorAffiliation', 'distributorAbbreviation', 'distributorURL'], citation_keys, citation_values, lang, 'Distributor')
        cont = write_single_key_section(f, cont, 'distributionDate', citation_keys, citation_values, lang, 'distributionDate')
        cont = write_single_key_section(f, cont, 'depositor', citation_keys, citation_values, lang, 'depositor')
        cont = write_single_key_section(f, cont, 'dateOfDeposit', citation_keys, citation_values, lang, 'dateOfDeposit')
        cont = write_grouped_keys_section(f, cont, ['timePeriodCoveredStart', 'timePeriodCoveredEnd'], citation_keys, citation_values, lang, 'Time period covered (single date or date range)')
        cont = write_grouped_keys_section(f, cont, ['dateOfCollectionStart', 'dateOfCollectionEnd'], citation_keys, citation_values, lang, 'Date of data collection (single date or date range)')
        cont = write_dataset_level_key(f, cont, 'publicationDate', dataset.json(), lang, 'Publication Date')
        cont = write_single_key_section(f, cont, 'kindOfData', citation_keys, citation_values, lang, 'kindOfData')
        cont = write_grouped_keys_section(f, cont, ['seriesName', 'seriesInformation'], citation_keys, citation_values, lang, 'Series')
        cont = write_grouped_keys_section(f, cont, ['softwareName', 'softwareVersion'], citation_keys, citation_values, lang, 'Software')
        cont = write_single_key_section(f, cont, 'relatedMaterial', citation_keys, citation_values, lang, 'relatedMaterial')
        cont = write_single_key_section(f, cont, 'relatedDatasets', citation_keys, citation_values, lang, 'relatedDatasets')
        cont = write_single_key_section(f, cont, 'otherReferences', citation_keys, citation_values, lang, 'otherReferences')
        cont = write_single_key_section(f, cont, 'dataSources', citation_keys, citation_values, lang, 'dataSources')
        cont = write_single_key_section(f, cont, 'originOfSources', citation_keys, citation_values, lang, 'originOfSources')
        cont = write_single_key_section(f, cont, 'characteristicOfSources', citation_keys, citation_values, lang, 'characteristicOfSources')
        cont = write_single_key_section(f, cont, 'accessToSources', citation_keys, citation_values, lang, 'accessToSources')

        #Acces Information metadata
        title = translate_key('ACCESS INFORMATION', lang, dict_type='title')
        f.write(title + '\n' + '-' * len(title) + '\n')
        cont = 0
        if 'license' in dataset.json()['data']['latestVersion']:
            cont+=1
            section_title_key = 'Creative Commons License of the dataset'
            f.write(f"{cont}.  {translate_key(section_title_key, lang, dict_type='title')}:\n")
            f.write('\t'+dataset.json()['data']['latestVersion']['license']['name']+'\n\n')
        if 'persistentUrl' in dataset.json()['data']:
            cont+=1
            section_title_key = 'Dataset DOI'
            f.write(f"{cont}.  {translate_key(section_title_key, lang, dict_type='title')}:\n")
            f.write('\t'+dataset.json()['data']['persistentUrl']+'\n\n')
        cont = write_grouped_keys_section(f, cont,['publicationRelationType', 'publicationCitation', 'publicationIDType', 'publicationIDNumber', 'publicationURL'], citation_keys, citation_values,lang, 'Related publication')

        #Geospatial metadata
        if len(geo_keys) != 0:
            title = translate_key('Geospatial Metadata', lang, dict_type='title')
            f.write(title + '\n' + '-' * len(title) + '\n')
            cont = 0
            cont = write_grouped_keys_section(f, cont, ['country', 'state', 'city', 'otherGeographicCoverage'], geo_keys, geo_values, lang, 'Geographical location/s of data collection')
            cont = write_single_key_section(f, cont, 'geographicUnit', geo_keys, geo_values, lang, 'geographicUnit')
            cont = write_grouped_keys_section(f, cont, ['westLongitude', 'eastLongitude', 'northLongitude', 'southLongitude'], geo_keys, geo_values, lang, 'Geographic Bounding Box')

        #Social science metadata
        if len(social_keys) != 0:
            title = translate_key('Social Science and Humanities Metadata', lang, dict_type='title'); f.write(title + '\n' + '-' * len(title) + '\n')
            cont = 0
            cont = write_single_key_section(f, cont, 'unitOfAnalysis', social_keys, social_values, lang, 'unitOfAnalysis')
            cont = write_single_key_section(f, cont, 'universe', social_keys, social_values, lang, 'universe')
            cont = write_single_key_section(f, cont, 'timeMethod', social_keys, social_values, lang, 'timeMethod')
            cont = write_single_key_section(f, cont, 'dataCollector', social_keys, social_values, lang, 'dataCollector')
            cont = write_single_key_section(f, cont, 'collectorTraining', social_keys, social_values, lang, 'collectorTraining')
            cont = write_single_key_section(f, cont, 'frequencyOfDataCollection', social_keys, social_values, lang, 'frequencyOfDataCollection')
            cont = write_single_key_section(f, cont, 'samplingProcedure', social_keys, social_values, lang, 'samplingProcedure')
            cont = write_grouped_keys_section(f, cont, ['targetSampleActualSize', 'targetSampleSizeFormula'], social_keys, social_values, lang, 'Target Sample Size')
            cont = write_single_key_section(f, cont, 'deviationsFromSampleDesign', social_keys, social_values, lang, 'deviationsFromSampleDesign')
            cont = write_single_key_section(f, cont, 'collectionMode', social_keys, social_values, lang, 'collectionMode')
            cont = write_single_key_section(f, cont, 'researchInstrument', social_keys, social_values, lang, 'researchInstrument')
            cont = write_single_key_section(f, cont, 'dataCollectionSituation', social_keys, social_values, lang, 'dataCollectionSituation')
            cont = write_single_key_section(f, cont, 'actionsToMinimizeLoss', social_keys, social_values, lang, 'actionsToMinimizeLoss')
            cont = write_single_key_section(f, cont, 'controlOperations', social_keys, social_values, lang, 'controlOperations')
            cont = write_single_key_section(f, cont, 'weighting', social_keys, social_values, lang, 'weighting')
            cont = write_single_key_section(f, cont, 'cleaningOperations', social_keys, social_values, lang, 'cleaningOperations')
            cont = write_single_key_section(f, cont, 'datasetLevelErrorNotes', social_keys, social_values, lang, 'datasetLevelErrorNotes')
            cont = write_single_key_section(f, cont, 'responseRate', social_keys, social_values, lang, 'responseRate')
            cont = write_single_key_section(f, cont, 'samplingErrorEstimates', social_keys, social_values, lang, 'samplingErrorEstimates')
            cont = write_single_key_section(f, cont, 'otherDataAppraisal', social_keys, social_values, lang, 'otherDataAppraisal')
            cont = write_grouped_keys_section(f, cont, ['socialScienceNotesType', 'socialScienceNotesSubject', 'socialScienceNotesText'], social_keys, social_values, lang, 'Notes')

        #Astronomy metadata
        if len(astronomy_keys) != 0:
            title = translate_key('Astronomy and Astrophysics Metadata', lang, dict_type='title')
            f.write(title + '\n' + '-' * len(title) + '\n')
            cont = 0
            cont = write_single_key_section(f, cont, 'astroType', astronomy_keys, astronomy_values, lang, 'Type')
            cont = write_single_key_section(f, cont, 'astroFacility', astronomy_keys, astronomy_values, lang, 'Facility')
            cont = write_single_key_section(f, cont, 'astroInstrument', astronomy_keys, astronomy_values, lang, 'Instrument')
            cont = write_single_key_section(f, cont, 'astroObject', astronomy_keys, astronomy_values, lang, 'Object')
            cont = write_single_key_section(f, cont, 'resolution.Spatial', astronomy_keys, astronomy_values, lang, 'Spatial Resolution')
            cont = write_single_key_section(f, cont, 'resolution.Spectral', astronomy_keys, astronomy_values, lang, 'Spectral Resolution')
            cont = write_single_key_section(f, cont, 'resolution.Temporal', astronomy_keys, astronomy_values, lang, 'Temporal Resolution')
            cont = write_grouped_keys_section(f, cont, ['coverage.Spectral.Bandpass'], astronomy_keys, astronomy_values, lang, 'Bandpass')
            cont = write_grouped_keys_section(f, cont, ['coverage.Spectral.CentralWavelength'], astronomy_keys, astronomy_values, lang, 'Central Wavelength (m)')
            cont = write_grouped_keys_section(f, cont, ['coverage.Spectral.MinimumWavelength', 'coverage.Spectral.MaximumWavelength'], astronomy_keys, astronomy_values, lang, 'Wavelength Range')
            cont = write_grouped_keys_section(f, cont, ['coverage.Temporal.StartTime', 'coverage.Temporal.EndTime'], astronomy_keys, astronomy_values, lang, 'Dataset Date Range')
            cont = write_single_key_section(f, cont, 'coverage.Spatial', astronomy_keys, astronomy_values, lang, 'Sky Coverage')
            cont = write_single_key_section(f, cont, 'coverage.Depth', astronomy_keys, astronomy_values, lang, 'Depth Coverage')
            cont = write_single_key_section(f, cont, 'coverage.ObjectDensity', astronomy_keys, astronomy_values, lang, 'Object Density')
            cont = write_single_key_section(f, cont, 'coverage.ObjectCount', astronomy_keys, astronomy_values, lang, 'Object Count')
            cont = write_single_key_section(f, cont, 'coverage.SkyFraction', astronomy_keys, astronomy_values, lang, 'Fraction of Sky')
            cont = write_single_key_section(f, cont, 'coverage.Polarization', astronomy_keys, astronomy_values, lang, 'Polarization')
            cont = write_single_key_section(f, cont, 'redshiftType', astronomy_keys, astronomy_values, lang, 'Redshift Type')
            cont = write_single_key_section(f, cont, 'resolution.Redshift', astronomy_keys, astronomy_values, lang, 'Redshift Resolution')
            cont = write_grouped_keys_section(f, cont, ['coverage.Redshift.MinimumValue', 'coverage.Redshift.MaximumValue'], astronomy_keys, astronomy_values, lang, 'Redshift Value')

        #Life Sciences Metadata
        if len(biomedical_keys) != 0:
            title = translate_key('Life Sciences Metadata', lang, dict_type='title')
            f.write(title + '\n' + '-' * len(title) + '\n')
            cont = 0
            cont = write_single_key_section(f, cont, 'studyDesignType', biomedical_keys, biomedical_values, lang, 'Design Type')
            cont = write_single_key_section(f, cont, 'studyFactorType', biomedical_keys, biomedical_values, lang, 'Factor Type')
            cont = write_single_key_section(f, cont, 'studyAssayOrganism', biomedical_keys, biomedical_values, lang, 'Organism')
            cont = write_single_key_section(f, cont, 'studyAssayOtherOrganism', biomedical_keys, biomedical_values, lang, 'Other Organism')
            cont = write_single_key_section(f, cont, 'studyAssayMeasurementType', biomedical_keys, biomedical_values, lang, 'Measurement Type')
            cont = write_single_key_section(f, cont, 'studyAssayOtherMeasurmentType', biomedical_keys, biomedical_values, lang, 'Other Measurement Type')
            cont = write_single_key_section(f, cont, 'studyAssayTechnologyType', biomedical_keys, biomedical_values, lang, 'Technology Type')
            cont = write_single_key_section(f, cont, 'studyAssayPlatform', biomedical_keys, biomedical_values, lang, 'Technology Platform')
            cont = write_single_key_section(f, cont, 'studyAssayCellType', biomedical_keys, biomedical_values, lang, 'Cell Type')

        #Journal metadata
        if len(journal_keys) != 0:
            title = translate_key('Journal Metadata', lang, dict_type='title')
            f.write(title + '\n' + '-' * len(title) + '\n')
            cont = 0
            cont = write_grouped_keys_section(f, cont, ['journalVolume', 'journalIssue', 'journalPubDate'], journal_keys, journal_values, lang, 'Journal')
            cont = write_single_key_section(f, cont, 'journalArticleType', journal_keys, journal_values, lang, 'Type of Article')

        #Computational Workflow metadata
        if len(computationalworkflow_keys) != 0:
            title = translate_key('Computational Workflow Metadata', lang, dict_type='title')
            f.write(title + '\n' + '-' * len(title) + '\n')
            cont=0
            cont = write_single_key_section(f, cont, 'workflowType', computationalworkflow_keys, computationalworkflow_values, lang, 'workflowType')
            cont = write_single_key_section(f, cont, 'workflowCodeRepository', computationalworkflow_keys, computationalworkflow_values, lang, 'workflowCodeRepository')
            cont = write_single_key_section(f, cont, 'workflowDocumentation', computationalworkflow_keys, computationalworkflow_values, lang, 'workflowDocumentation')

        #Local Contexts Metadata
        if len(LocalContextsCVoc_keys) != 0:
            title = translate_key('Local Contexts Metadata', lang, dict_type='title')
            f.write(title + '\n' + '-' * len(title) + '\n')
            cont=0
            cont = write_single_key_section(f, cont, 'LCProjectUrl', LocalContextsCVoc_keys, LocalContextsCVoc_values, lang, 'LCProjectUrl')

        #Files metadata
        title = translate_key('FILE OVERVIEW', lang, dict_type='title')
        f.write(title + '\n' + '-' * len(title) + '\n')
        for i in range(0,len(filemetadata_keys)):
            f.write('\t'+translate_key('File name', lang, dict_type='title')+': '+filemetadata_values[i][filemetadata_keys[i].index('filename')]+'\n')
            if 'description' in filemetadata_keys[i]:
                f.write('\t'+translate_key('File decription', lang, dict_type='title')+': '+filemetadata_values[i][filemetadata_keys[i].index('description')]+'\n')
            f.write('\t'+translate_key('File format', lang, dict_type='title')+': '+filemetadata_values[i][filemetadata_keys[i].index('contentType')]+'\n\n')
        print('The Readme has been created in the directory ' + path +'.')
        
# Checking if both inputs are provided
if not doi or not token:
    print("Please enter DOI, Token and URL of the repository correctly.")
else:
    api = NativeApi(base_url, token)
    dataset = api.get_dataset(doi)

    #  Metadata lists:
    citation_keys, geo_keys, social_keys, astronomy_keys, biomedical_keys, journal_keys, computationalworkflow_keys, LocalContextsCVoc_keys, darwincore_keys  = [[] for _ in range(9)]
    citation_values, geo_values, social_values, astronomy_values, biomedical_values, journal_values, computationalworkflow_values, LocalContextsCVoc_values, darwincore_values = [[] for _ in range(9)]
    filemetadata_keys=[]
    filemetadata_values=[]

    # Exporting metadata and creating readme
    exportmetadata(base_url, token, doi, citation_keys, citation_values, geo_keys, geo_values, social_keys,
                      social_values, astronomy_keys, astronomy_values, biomedical_keys, biomedical_values,
                      journal_keys, journal_values,computationalworkflow_keys, computationalworkflow_values,
                      LocalContextsCVoc_keys, LocalContextsCVoc_values, darwincore_keys, darwincore_values)
    filemetadata(base_url, token, doi, filemetadata_keys, filemetadata_values)
    createreadme(base_url, token, doi, lang,
                      citation_keys, citation_values,
                      geo_keys, geo_values,
                      social_keys, social_values,
                      astronomy_keys, astronomy_values,
                      biomedical_keys, biomedical_values,
                      journal_keys, journal_values,
                      computationalworkflow_keys, computationalworkflow_values,
                      LocalContextsCVoc_keys, LocalContextsCVoc_values, darwincore_keys, darwincore_values,
                      filemetadata_keys, filemetadata_values)

# Construct the correct file path
file_path = os.path.join(f'{doi.replace("doi:10.34810/", "")}', 'Readme.txt')