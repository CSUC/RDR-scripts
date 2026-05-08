[![ca](https://img.shields.io/badge/lang-ca-blue.svg)](https://github.com/CSUC/RDR-scripts/blob/main/delete_files/README.md)
[![en](https://img.shields.io/badge/lang-en-green.svg)](https://github.com/CSUC/RDR-scripts/blob/main/delete_files/README_ENG.md)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CSUC/RDR-scripts/blob/main/delete_files/delete_files.ipynb)

# Script per eliminar fitxers d'un dataset a Dataverse

Per a qualsevol consulta sobre el codi, poseu-vos en contacte amb rdr-contacte@csuc.cat

## Descripció

Aquest script està dissenyat per interactuar amb el Repositori de Dades de Recerca (https://dataverse.csuc.cat/) i permet eliminar fitxers d’un conjunt de dades de Dataverse identificat mitjançant un DOI.

El script utilitza la llibreria `pyDataverse` per recuperar la informació del dataset i la llibreria `requests` per executar les peticions d’eliminació mitjançant l’API de Dataverse.

L’usuari pot escollir si vol eliminar:

- tots els fitxers del dataset
- els fitxers d’una carpeta específica
- els fitxers d’una subcarpeta específica

Abans d’eliminar els fitxers, el script mostra una previsualització dels fitxers seleccionats i demana una confirmació explícita escrivint `Yes`.

## Requisits

- Python 3.x
- Llibreria `pyDataverse`
- Llibreria `requests`
- Llibreria `pandas`
- Llibreria `ipywidgets`
- Un token d’API de Dataverse amb permisos suficients per modificar el dataset

## Ús

1. **Paràmetres d'entrada**:
    - DOI: Identificador Digital de l'Objecte (DOI) del conjunt de dades.
    - Token: Token d'autenticació per accedir al repositori Dataverse.

2. **Configuració**:
    - Inicialitza l’URL base de la instància Dataverse.
    - Autentica l’API amb el token proporcionat.

3. **Lectura dels fitxers del dataset**:
    - Recupera la metadada del dataset especificat.
    - Extreu la llista de fitxers disponibles.
    - Mostra l’identificador del fitxer, el nom del fitxer i la carpeta o subcarpeta on es troba.

4. **Selecció dels fitxers a eliminar**:
    - Permet seleccionar entre eliminar tots els fitxers o només els fitxers d’una carpeta/subcarpeta.
    - Mostra una llista desplegable amb les carpetes disponibles.

5. **Confirmació**:
    - Mostra els fitxers seleccionats abans de l’eliminació.
    - Demana a l’usuari que escrigui exactament `Yes` per confirmar.
    - Si l’usuari no escriu `Yes`, l’operació es cancel·la.

6. **Eliminació dels fitxers**:
    - Envia una petició `DELETE` a l’API de Dataverse per a cada fitxer seleccionat.
    - Mostra un resum amb els fitxers eliminats correctament i possibles errors.

## Estructura de Fitxers

- `delete_dataset_files_script.ipynb`: Script principal per seleccionar i eliminar fitxers d’un dataset.
- `README.md`: Documentació del script en català.
- `README_ENG.md`: Documentació del script en anglès.

## Exemple d'Ús

```python
# Introduïu el token d'API
API_TOKEN = "YOUR_API_TOKEN"

# Introduïu el DOI del dataset
DOI = "doi:10.34810/data2432"
