[![ca](https://img.shields.io/badge/lang-ca-blue.svg)](https://github.com/CSUC/RDR-scripts/blob/main/persistent_link/README.md)
[![en](https://img.shields.io/badge/lang-en-green.svg)](https://github.com/CSUC/RDR-scripts/blob/main/persistent_link/README_ENG.md)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CSUC/RDR-scripts/blob/main/persistent_link/extract_persistent_link.ipynb)
# Extracció d'Enllaços Persistents de Conjunts de Dades

Per a qualsevol consulta sobre el codi, poseu-vos en contacte amb rdr-contacte@csuc.cat

## Descripció

Aquest script de Python està dissenyat per extreure els enllaços persistents dels fitxers en conjunts de dades allotjats a Dataverse. Els enllaços persistents són útils per referenciar dades específiques de manera constant, fins i tot si les dades es mouen o s'actualitzen en el futur.

## Requisits

- Python 3.x
- Biblioteques Python: `pyDataverse`, `xlsxwriter`, `pandas`

## Ús

1. **Instal·lació de Biblioteques**: Feu clic al botó "Install Libraries" per instal·lar o actualitzar les biblioteques necessàries.

2. **Introduir Informació**: Proporcioneu el token de l'API, el DOI del conjunt de dades i la URL del repositori.

3. **Executar el Script**: Feu clic al botó de reproducció per executar la cel·la i extreure els enllaços persistents.

4. **Descarregar Resultats**: Es generarà un fitxer Excel amb els enllaços persistents. Podeu descarregar el fitxer fent clic a l'enllaç proporcionat.

## Estructura de Fitxers
- `persistent_link.ipynb`: El script principal per exportar metadades i generar el fitxer README.
- `excel_name.xlsx`: El fitxer excel amb nom excel_name generat que conté informació detallada sobre els links persistents conjunt de dades.

## Exemple d'Ús
```python
# Estableix el DOI i el token
doi = 'doi:10.34810/dataXXX'
token = 'el_teul_propi_token'

# Executa l'script
