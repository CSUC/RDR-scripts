[![ca](https://img.shields.io/badge/lang-ca-blue.svg)](https://github.com/CSUC/RDR-scripts/blob/main/transform_excel/Readme.md)
[![en](https://img.shields.io/badge/lang-en-green.svg)](https://github.com/CSUC/RDR-scripts/blob/main/transform_excel/Readme_ENG.md)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CSUC/RDR-scripts/blob/main/transform_excel/transform_excel.ipynb)
# Transformar fitxer en format Excel a format CSV

Per a qualsevol consulta sobre el codi, contacta amb rdr-contacte@csuc.cat 

## Visió general
Aquest script està dissenyat per convertir fitxers d'Excel a format CSV. Permet als usuaris carregar un fitxer d'Excel (.xlsx), que després es processa per generar fitxers CSV per a cada full de càlcul del llibre d'Excel. L'script ofereix opcions per separar taules a cada full de càlcul en diferents fitxers CSV o convertir cada full en un únic fitxer CSV.

## Requisits
- Python 3.x
- Biblioteca pandas
- Biblioteca ipywidgets
- Google Colab (per a ús interactiu)

## Ús
1. **Carregar fitxer Excel**:
    - Fes clic al botó "Carregar" per seleccionar un fitxer Excel (.xlsx) per a la conversió.

2. **Processar fitxer Excel**:
    - Si se t'hi demana, tria si vols separar les taules a cada full de càlcul en diferents fitxers CSV.
    - Fes clic a "Processar Excel" per iniciar el procés de conversió.

3. **Descarregar fitxers CSV**:
    - Un cop completada la conversió, es descarregarà automàticament un fitxer zip que conté els fitxers CSV generats.

## Estructura de fitxers
- `transform_excel.ipynb`: El script principal per convertir fitxers d'Excel a format CSV.
- `exemple.xlsx`: Exemple de fitxer Excel per a propòsits de prova.
- `exemple_sortida.zip`: Exemple de sortida que conté els fitxers CSV generats.

## Exemple d'ús
```python
# Executa l'script i segueix les instruccions per carregar un fitxer Excel.
# Tria si vols separar les taules a cada full de càlcul en diferents fitxers CSV.
# L'script convertirà el fitxer Excel a format CSV i descarregarà els fitxers generats.
