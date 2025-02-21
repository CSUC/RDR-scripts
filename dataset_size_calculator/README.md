[![ca](https://img.shields.io/badge/lang-ca-blue.svg)](https://github.com/CSUC/RDR-scripts/blob/main/dataset_size_calculator/README.md)  
[![en](https://img.shields.io/badge/lang-en-green.svg)](https://github.com/CSUC/RDR-scripts/blob/main/dataset_size_calculator/README_ENG.md)  

# Script per calcular la mida dels datasets d'una instància a Dataverse  
Per a qualsevol consulta sobre el codi, poseu-vos en contacte amb rdr-contacte@csuc.cat  

## Descripció  
Aquest script permet calcular la mida total dels conjunt de dades (datasets) allotjat a una instància del Repositori de Dades de Recerca (https://dataverse.csuc.cat/). Utilitza l'API de Dataverse per obtenir la mida de tots els fitxers associats als datasets d'una instància i retorna la mida total en bytes, KB, MB o GB.  

## Requisits  
- Python 3.x  
- Llibreria `requests` per fer crides a l'API de Dataverse  

## Ús  

1. **Paràmetres d'Entrada**:  
    - Token: Token d'autenticació per accedir al repositori Dataverse.  

2. **Configuració**:  
    - Especifica l'URL base de la instància Dataverse.  

3. **Obtenció de la mida del Dataset**:  
    - Recupera la informació de totes les mides els fitxers als datasets d'una instància.  
    - Suma la mida de cada fitxer per obtenir la mida total dels datasets.  

4. **Format de sortida**:  
    - Mostra la mida total en diferents unitats (bytes, KB, MB, GB) per facilitar la interpretació.  

5. **Opcions de Descàrrega**:  
    - Si s'executa en Google Colab, es pot descarregar un informe amb les mides del datasets.  
    - També es pot executar en altres entorns Python com Jupyter Notebook o localment.  

## Estructura de Fitxers  
- `dataset_size_calculator.ipynb`: Script per calcular les mides dels datasets.  
- `README.md`: Fitxer de documentació del script.  

## Exemple d'Ús  

# Estableix token
token = 'XXX-XXXX-XXXXX-XXXXX'

# Executa la funció per calcular la mida
L'script produeix un fitxer excel amb el nom  mida_datasets.xlsx i conté la següent informació:

| DOI  | Institution          | Original Size (Bytes) | Archival Size (Bytes) | Formatted Original Size | Unit (Original Size) | Formatted Archival Size | Unit (Archival Size) |
|------|----------------------|----------------------|----------------------|------------------------|----------------------|------------------------|----------------------|
| doi1 | Example Institution | 1024000             | 512000               | 1.00                   | MB                   | 500.00                 | KB                   |
| doi2 | Example Institution | 598424             | 896771               | 584.4                  | KB                   | 875.75                 | KB                   |

On:

- **Original Size (Bytes)**: és la mida en bytes del conjunt de fitxers del dataset en el seu format original.
- **Archival Size (Bytes)**: és la mida en bytes del conjunt de fitxers del dataset en el seu format tranformat durant la ingesta.
- **Formatted Original Size**: és la mida del conjunt de fitxers del dataset en el seu format original amb la unitat de mesura indicada a *Unit (Original Size)*.
- **Formatted Archival Size**: és la mida del conjunt de fitxers del dataset en el seu format tranformat durant la ingesta amb la unitat de mesura indicada a *Unit (Archival Size)*.

