[![ca](https://img.shields.io/badge/lang-ca-blue.svg)](https://github.com/CSUC/RDR-scripts/blob/main/REVISAT/README.md)
[![en](https://img.shields.io/badge/lang-en-green.svg)](https://github.com/CSUC/RDR-scripts/blob/main/REVISAT/README_ENG.md)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CSUC/RDR-scripts/blob/main/REVISAT/REVISAT_script.ipynb)

# Script d'Avaluació de datasets (REVISAT)
Per a qualsevol consulta sobre el codi, poseu-vos en contacte amb rdr-contacte@csuc.cat

## Objectiu de l'Script

Aquest script permet als usuaris avaluar un conjunt de dades abans de la publicació per garantir el compliment de les millors pràctiques d'accés obert. Realitza diversos controls i avaluacions sobre la metadada i el contingut del conjunt de dades. A continuació, es presenta una guia detallada sobre com utilitzar l'script i les seves funcionalitats.

## Descripció de l'Script

L'script realitza els següents controls i avaluacions sobre el conjunt de dades:

1. **Requisits Mínims de Metadades:**
    - Valida si el conjunt de dades conté els camps de metadades mínims requerits.
    - Mostra si el conjunt de dades conté tots els camps de metadades obligatoris.

2. **Títol i Publicació Relacionada:**
    - Verifica el títol del conjunt de dades.
    - Comprova si el conjunt de dades té alguna publicació relacionada i assegura que s'inclou la citació de la publicació.
    - Compara el títol del conjunt de dades amb el títol de la publicació relacionada si és aplicable.

3. **Afiliació dels Autors i ORCID:**
    - Comprova si almenys un autor està afiliat a la institució especificada.
    - Determina si almenys un autor proporciona el seu ORCID.

4. **Descripció:**
    - Mostra la descripció del conjunt de dades.

5. **Formats de Fitxers:**
    - Compta les ocurrències de diferents extensions de fitxers al conjunt de dades.
    - Comprova si el conjunt de dades conté un fitxer `readme.txt`.

6. **Llicència:**
    - Mostra la llicència del conjunt de dades o els termes d'ús.

7. **Avaluació F-UJI (Opcional):**
    - Si s'especifica, l'script pot obrir F-UJI (Fair Use and Justification for Use of Infrastructures) per a una avaluació manual del conjunt de dades.

## Instruccions

1. **Valors d'Entrada:**
    - **DOI (Identificador del Conjunt de Dades):** Introduïu el DOI del conjunt de dades.
    - **Token (Token de l'API):** Proporcioneu el token de l'API per a l'autenticació.
    - **Institució:** Introduïu el nom complet de la institució on es troba el conjunt de dades.
    - **WebDriver (Opcional):** Trieu un WebDriver (p. ex., Chrome o Firefox) si esteu avaluant el conjunt de dades a F-UJI.

2. **Execució:**
    - Executeu l'script després de proporcionar els valors d'entrada necessaris.
    - L'script realitzarà els controls i avaluacions sobre el conjunt de dades.

3. **Interpretació dels Resultats:**
    - Reviseu la sortida de cada control per garantir el compliment de les millors pràctiques d'accés obert.

Per a qualsevol consulta o problema relatiu al procés d'avaluació, poseu-vos en contacte amb el mantenidor de l'script.


## Terminal usage (no iPython Notebook) 

### Install virtual environment
```shell
cd REVISAT
python3 -m venv venv
```

### Install dependencies (through requirements.txt)
```shell
venv/bin/pip3 install -r requirements.txt
```

### Run script and extract data
Extract API token from Dataverse profile, create the file `DATAVERSE.txt` with the token in it (using file is not 
recorded in terminal history!).

```shell
TOKEN="$(cat secrets/DATAVERSE.txt)"
venv/bin/python3 main.py --doi doi:67.37297/data2103 --token "${TOKEN}" > README_new.md
```


