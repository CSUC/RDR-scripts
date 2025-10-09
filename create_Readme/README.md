[![ca](https://img.shields.io/badge/lang-ca-blue.svg)](https://github.com/CSUC/RDR-scripts/blob/main/create_Readme/README.md)
[![en](https://img.shields.io/badge/lang-en-green.svg)](https://github.com/CSUC/RDR-scripts/blob/main/create_Readme/README_ENG.md)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CSUC/RDR-scripts/blob/main/create_Readme/create_Readme_script.ipynb)

# Script per crear un fitxer Readme d'un dataset a Dataverse
Per a qualsevol consulta sobre el codi, poseu-vos en contacte amb rdr-contacte@csuc.cat

## Descripció
Aquest script està dissenyat per interactuar amb el Repositori de dades de recerca (https://dataverse.csuc.cat/), específicament per exportar metadades de conjunts de dades identificats amb Identificadors d'Objectes Digitals (DOI). Utilitza la llibreria pyDataverse per accedir i extreure metadades, que s'utilitzen per generar un fitxer README proporcionant informació detallada sobre els conjunts de dades. NO llegeix les metadades Darwin Core.

## Requisits
- Python 3.x
- Llibreria pyDataverse

## Ús
1. **Paràmetres d'Entrada**:
    - DOI: Identificador Digital de l'Objecte (DOI) del conjunt de dades.
    - Token: Token d'autenticació per accedir al repositori Dataverse.

2. **Configuració**:
    - Inicialitza l'URL base de la instància Dataverse.
    - Autentica l'API amb el token proporcionat.

3. **Exportar Metadades**:
    - Recupera metadades per al conjunt de dades especificat.
    - Extreu diverses categories de metadades com detalls de citació, informació geoespacial, metadades de ciències socials, etc.
    - Extreu metadades dels fitxers associats al conjunt de dades.

4. **Crear README**:
    - Genera un fitxer README que conté informació detallada sobre el conjunt de dades.
    - Inclou seccions per a informació general, informació d'accés, tipus de metadades i revisió de fitxers.
    - Escriu les metadades extretes al fitxer README.

5. **Descarregar README**:
    - Proporciona opcions per descarregar el fitxer README generat.
    - En Google Colab, es proporciona un botó de descàrrega.
    - En Jupyter Notebook, es proporciona un enllaç de descàrrega.

## Estructura de Fitxers
- `create_Readme_script.ipynb`: El script principal per exportar metadades i generar el fitxer README.
- `README.md`: El fitxer README generat que conté informació detallada sobre el conjunt de dades.

## Exemple d'Ús
```python
# Estableix el DOI i el token
doi = 'XYZ'
token = 'el_teu_propi_token'

# Executa l'script
