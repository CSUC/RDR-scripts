# @title Introduir DOI (doi:10.34810/dataXXX), el token i el nom complet de la institució. Clicar botó d'executar cel·la &#x25B6;
from datetime import date
from pyDataverse.api import NativeApi, DataAccessApi
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys
import numpy as np
import os
from collections import Counter
import textwrap
import pprint
from IPython.display import HTML, display
import argparse




def save_selection_institucions(change):
    global opcions
    selected = set(change['new'])

    if 'Totes les institucions' in selected:
        opcions = set(institucions)  # Select all institutions if 'Totes les institucions' is chosen
    else:
        opcions.update(selected)  # Update the set with new selections

    print(f"Institucions: {list(opcions)}")

# Function to clear the selection and reset the institutions widget
def restart_selection_institucions(button):
    global opcions
    #institucions_widget.value = []  # Clear the selections in the widget
    opcions.clear()  # Clear the global opcions set
    print("La selecció de la institució s'ha restablert.")

#### Metadata reading
def set_css():
  display(HTML('''
  <style>
    pre {
        white-space: pre-wrap;
    }
  </style>
  '''))

def Meta(doi, token, driver, opcions):
    today = date.today()
    print("Data:", today)
#    print("Dataset DOI: ", doi)

    base_url = 'https://dataverse.csuc.cat/'
    api = NativeApi(base_url,token)
    Metadata = api.get_dataset(doi)
    c_doi = Metadata.json()["data"]["latestVersion"]['datasetPersistentId']

    fields_metadata = Metadata.json()["data"]["latestVersion"]["metadataBlocks"]["citation"]["fields"]
    len_metadata = len(fields_metadata)
    Metadata_min_req = ['title', 'datasetContact', 'dsDescription', 'keyword', 'subject', 'kindOfData', 'author']

    metadata_repositori = []
    #today = date.today()

    i = 0
    while i <= len_metadata:
        metadata_repositori.append(fields_metadata[i]["typeName"])
        i +=1
        if i == len_metadata:
            break


    intersect_metadata = list(set(metadata_repositori) & set(Metadata_min_req))# Comprobamos la coincidencia  de campos
    same_metadata = len(list(set(Metadata_min_req)^set(intersect_metadata)))# 0 --> have minimum of metadata

    print('\nConté les metadades mínimes obligatòries?')
    Metadata_min = []  #####################################################################################
    Metadata_faltante = []
    if same_metadata !=0:
        #print("NO\nFalta la medata:", list(set(Metadata_min_req)^set(intersect_metadata)))
        Metadata_faltante.append(list(set(Metadata_min_req)^set(intersect_metadata)))
        print("NO", Metadata_faltante)
    else:
        #print("SÍ")
        #Metadata_min.append("SÍ")
        print("SÍ")

    index_title = metadata_repositori.index('title')
    print("\nTítol dataset:\n{}\n".format( fields_metadata[index_title]["value"]))
    titol = fields_metadata[index_title]["value"]
    titol_1 = titol.split(":")
    #print(titol[22:])
    #print(titol_1)

    ###### Related publication

    relatedpublication = 'publication'
    #print("RELATION PUBLICATION:")
    print("En el cas que el dataset tingui una publicació relacionada, inclou la citació?")

    if relatedpublication in metadata_repositori:
        print("SÍ")
        Rel_pub = []

        index_publication = metadata_repositori.index(relatedpublication)
        for i in fields_metadata[index_publication]["value"]:
            Rel_pub.append(i["publicationCitation"]["value"])
            print(i["publicationCitation"]["value"])

        #print("Related publication:", Rel_pub)

        if ("Replication Data for" in titol_1) & (len(titol_1) > 1):
            only_title = titol[21:]
            print("\nEl títol inclou: Replication data for")
            ##Comprobamos que tengan el mismo titulo:
            for i in Rel_pub[0].split("."):
                #print (i)
                if (only_title.casefold() == i.casefold()):
                    print("Els títols coincideixen")
        else: print("\nNo és rèplica de l'article")

    else: print("\nNo té publicacions relacionades")


    index_author = metadata_repositori.index('author')
    author_id = []
    afiliacion = []
    institucion = []

    for i in range(len(fields_metadata[index_author]["value"])):
        for j in (list(fields_metadata[index_author]["value"][i].keys())):
            if (j == 'authorAffiliation'):
                if "expandedvalue" in fields_metadata[index_author]["value"][i]['authorAffiliation']:
                    afiliacion.append(fields_metadata[index_author]["value"][i]['authorAffiliation']["expandedvalue"]["termName"])
                else:
                    afiliacion.append(fields_metadata[index_author]["value"][i]['authorAffiliation']["value"])
            if (j == 'authorIdentifier'):
                author_id.append("SÍ")


    ##At least one of the authors belongs to the institution where it is deposited
    for i in afiliacion:
        ins = i.split(".")
        for centre in opcions:
          if centre in ins:
              institucion.append("SÍ")
          else: institucion.append("NO")


    print("\nAlmenys un/a dels/les autors/es pertany a la institució on es diposita: ", "SÍ" if "SÍ" in institucion else "NO")
    ## At least one of the authors reports their ORCID
    print("Almenys un/a dels/les autors/es informa del seu ORCID?")
    print("ORCID: ", "SÍ" if "SÍ" in author_id else "NO")


    ###### Description
    index_descripcion = metadata_repositori.index('dsDescription')
    descripcion = []
    print("\nDescripció")
    descripcion.append(fields_metadata[index_descripcion]["value"][0]['dsDescriptionValue']["value"])
    print(descripcion[0])



    print("\nFormat de fitxers")
    total_files = len(Metadata.json()['data']['latestVersion']['files'])
    files = []
    files_extension = []

    for i in range(total_files):
        #if i == "Readme.txt" or i == "readme.txt":
            #print(os.path.splitext(Metadata.json()['data']['latestVersion']['files'][i]['dataFile']['filename'])[1])
            #print(Metadata.json()['data']['latestVersion']['files'][i]['dataFile']['filename'])
            files_extension.append(os.path.splitext(Metadata.json()['data']['latestVersion']['files'][i]['dataFile']['filename'])[1])
            files.append(Metadata.json()['data']['latestVersion']['files'][i]['dataFile']['filename'])


    print(Counter(files_extension))

    lowercase_files = list(map(lambda x: x.lower(), files))
    for j in lowercase_files:
        if j == "readme.txt":
            print("Sí que conté el fitxer readme.txt")


    ###### License
    print("\nLlicència:")
    if 'license' in Metadata.json()["data"]['latestVersion'].keys():
        print(Metadata.json()["data"]['latestVersion']["license"]["name"])
    else:
        print(Metadata.json()["data"]['latestVersion']['termsOfUse'])


###### F-UJI
    if driver is None:
        print("\nAvalueu el dataset manualment a F-UJI: https://www.f-uji.net/")

    else:
        driver.get("https://www.f-uji.net/")
        driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/p/a').click()
        driver.find_element(By.XPATH, '//*[@id="pid"]').send_keys(doi)
        driver.find_element(By.XPATH, '//*[@id="assessment_form"]/div/form/div[4]/button').click()



# Provide input values
identifier = ""  # @param {type:"string"}
token = ""  # @param {type:"string"}
driver = None ## triar (webdriver.Chrome(), webdriver.Firefox() or None) per evaluar el daset a F-uji. Trieu None si useu l'script a Colab.
doi = identifier

#Choose an institution
institucions = [
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
opcions = set(institucions)  # Select all institutions if 'Totes les institucions' is chosen


# Set up argument parsing
parser = argparse.ArgumentParser(description="Parse arguments and call Meta function.")
parser.add_argument("--doi", required=True, help="DOI string")
parser.add_argument("--token", required=True, help="Authentication token")
#parser.add_argument("--driver", required=True, help="Driver type")
driver = None
#parser.add_argument("--opcions", required=True, help="Options in JSON format")


# Parse arguments
args = parser.parse_args()

Meta(args.doi, args.token, driver, opcions)
