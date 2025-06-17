# =======================
# CONFIGURATION PARAMETERS
# =======================
doi = ""  # Full DOI, e.g., "doi:10.34810/data123456"
token = ""  # API token from https://dataverse.csuc.cat/dataverseuser.xhtml?selectTab=apiTokenTab
driver = None  # Use: webdriver.Chrome(), webdriver.Firefox(), or None
opcions = [
    "Universitat Rovira i Virgili",
    "Universitat Pompeu Fabra",
    "Universitat Oberta de Catalunya",
    "Vall d’Hebron Institut de Recerca",
    "Centre for Research on Ecology and Forestry Applications",
    "Universitat Ramon Llull",
    "Consorci Institut D'Investigacions Biomèdiques August Pi i Sunyer",
    "Centre de Recerca en Agrigenòmica",
    "Institut Català de Nanociència i Nanotecnologia",
    "Institut de Recerca Sant Joan de Déu",
    "Universitat Autònoma de Barcelona",
    "Universitat Politècnica de Catalunya",
    "Consorci de Serveis Universitaris de Catalunya",
    "Institut de Física d'Altes Energies",
    "Universitat Internacional de Catalunya",
    "Centre de Recerca Matemàtica",
    "Institut d'Investigació Biomèdica de Bellvitge",
    "Universitat de Lleida",
    "Universitat de Girona",
    "i2CAT",
    "Institut de Recerca i Tecnologia Agroalimentàries",
    "Fundación Josep Carreras Contra la Leucemia",
    "Centre for Demographic Studies",
    "Centre Tecnològic Forestal de Catalunya",
    "Universitat de Vic - Universitat Central de Catalunya",
    "IrsiCaixa",
    "Institute for Bioengineering of Catalonia",
    "Biomedical Research Institute of Lleida",
    "Institut Barcelona d'Estudis Internacionals",
    "Barcelona University",
    "Catalan Institute for Water Research",
    "Institute of Research and Innovation Parc Taulí",
    "Institut Català de Paleoecologia Humana i Evolució Social",
    "Universitat de les Illes Balears",
    "Institute of Photonic Sciences",
    "Institute for Research in Biomedicine",
    "Agrotecnio - Centre for Food and Agriculture Research",
    "Institut d'Investigació Biomèdica de Girona",
    "Institut Català d'Arqueologia Clàssica",
    "Barcelona Institute for Global Health"
]


# =======================
# IMPORTS & INSTALLATION
# =======================
import os
import sys
import subprocess
from datetime import date
from pyDataverse.api import NativeApi
from selenium import webdriver
from selenium.webdriver.common.by import By
from collections import Counter
from IPython.display import HTML, display

# Install necessary packages if running interactively (optional)
def install_packages():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyDataverse"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "tensorflow-probability"])

# =======================
# MAIN FUNCTION
# =======================
def Meta(doi, token, driver, opcions):
    today = date.today()
    print("Data:", today)

    base_url = 'https://dataverse.csuc.cat/'
    api = NativeApi(base_url, token)
    Metadata = api.get_dataset(doi)

    fields_metadata = Metadata.json()["data"]["latestVersion"]["metadataBlocks"]["citation"]["fields"]
    metadata_repositori = [field["typeName"] for field in fields_metadata]

    Metadata_min_req = ['title', 'datasetContact', 'dsDescription', 'keyword', 'subject', 'kindOfData', 'author']
    intersect_metadata = list(set(metadata_repositori) & set(Metadata_min_req))
    same_metadata = len(list(set(Metadata_min_req) ^ set(intersect_metadata)))

    print("\nConté les metadades mínimes obligatòries?")
    if same_metadata != 0:
        print("NO", list(set(Metadata_min_req) ^ set(intersect_metadata)))
    else:
        print("SÍ")

    # Title
    index_title = metadata_repositori.index('title')
    titol = fields_metadata[index_title]["value"]
    print("\nTítol dataset:\n{}\n".format(titol))

    titol_1 = titol.split(":")

    # Related publication
    print("En el cas que el dataset tingui una publicació relacionada, inclou la citació?")
    if 'publication' in metadata_repositori:
        print("SÍ")
        index_publication = metadata_repositori.index('publication')
        Rel_pub = [pub["publicationCitation"]["value"] for pub in fields_metadata[index_publication]["value"]]
        for citation in Rel_pub:
            print(citation)

        if "Replication Data for" in titol_1[0] and len(titol_1) > 1:
            only_title = titol[21:]
            print("\nEl títol inclou: Replication data for")
            for i in Rel_pub[0].split("."):
                if only_title.casefold() == i.strip().casefold():
                    print("Els títols coincideixen")
        else:
            print("\nNo és rèplica de l'article")
    else:
        print("\nNo té publicacions relacionades")

    # Author info
    index_author = metadata_repositori.index('author')
    author_id = []
    afiliacion = []
    institucion = []

    for author in fields_metadata[index_author]["value"]:
        aff = author.get("authorAffiliation", {})
        aff_val = aff.get("expandedvalue", {}).get("termName") or aff.get("value")
        if aff_val:
            afiliacion.append(aff_val)

        if "authorIdentifier" in author:
            author_id.append("SÍ")

    for aff in afiliacion:
        matched = any(inst in aff for inst in opcions)
        institucion.append("SÍ" if matched else "NO")

    print("\nAlmenys un/a dels/les autors/es pertany a la institució on es diposita:", "SÍ" if "SÍ" in institucion else "NO")
    print("Almenys un/a dels/les autors/es informa del seu ORCID?")
    print("ORCID: ", "SÍ" if "SÍ" in author_id else "NO")

    # Description
    index_descripcion = metadata_repositori.index('dsDescription')
    descripcion = fields_metadata[index_descripcion]["value"][0]['dsDescriptionValue']["value"]
    print("\nDescripció:\n", descripcion)

    # File formats
    print("\nFormat de fitxers")
    total_files = len(Metadata.json()['data']['latestVersion']['files'])
    files = [file['dataFile']['filename'] for file in Metadata.json()['data']['latestVersion']['files']]
    extensions = [os.path.splitext(f)[1] for f in files]
    print(Counter(extensions))

    lowercase_files = [f.lower() for f in files]
    if "readme.txt" in lowercase_files:
        print("Sí que conté el fitxer readme.txt")

    # License
    print("\nLlicència:")
    license_info = Metadata.json()["data"]['latestVersion'].get("license", {}).get("name") \
        or Metadata.json()["data"]['latestVersion'].get('termsOfUse')
    print(license_info)

    # F-UJI
    if driver is None:
        print("\nAvalueu el dataset manualment a F-UJI: https://www.f-uji.net/")
    else:
        driver.get("https://www.f-uji.net/")
        driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/p/a').click()
        driver.find_element(By.XPATH, '//*[@id="pid"]').send_keys(doi)
        driver.find_element(By.XPATH, '//*[@id="assessment_form"]/div/form/div[4]/button').click()


# =======================
# EXECUTE SCRIPT
# =======================
if __name__ == "__main__":
    Meta(doi, token, driver, opcions)
