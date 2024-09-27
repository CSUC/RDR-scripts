[![ca](https://img.shields.io/badge/lang-ca-blue.svg)](https://github.com/CSUC/RDR-scripts/blob/main/README.md)
[![en](https://img.shields.io/badge/lang-en-green.svg)](https://github.com/CSUC/RDR-scripts/blob/main/README_ENG.md)
# Extreure metadades de multiples datasets per institució

Aquest script permet processar i agregar metadades de diferents institucions i categories com citacions, metadades geoespacials, socials, astronòmiques, biomèdiques, revistes i altres. Els resultats s'exporten en un fitxer Excel que es pot descarregar automàticament.

## Descripció
L'script ofereix la capacitat de seleccionar una o més institucions i metadades per processar les dades corresponents als conjunts de dades associats a aquestes institucions. Un cop processades les dades, s'agreguen i s'exporten en format Excel, amb metadades associades als seus identificadors DOI.

## Requisits
- Python 3.x
- Llibreria `ipywidgets`
- Llibreria `pandas`
- Llibreria `openpyxl`
- Google Colab (per a ús interactiu)

## Ús

1. **Carregar Institucions i Metadades**:
    - Selecciona una o més institucions i categories de metadades (citacions, geoespacials, socials, etc.) utilitzant els widgets interactius.

2. **Processar Metadades**:
    - L'script processarà les dades per a cada conjunt de dades de les institucions seleccionades i agregarà les metadades corresponents als seus DOI.

3. **Generar un Fitxer Excel**:
    - Un cop completat el processament, l'script crearà un fitxer Excel amb els DOI, institucions i les metadades seleccionades. El fitxer es pot descarregar automàticament.

## Estructura dels Fitxers

- `metadata_processor.ipynb`: L'script principal per processar i agregar les metadades.
- `estudi_metadades.xlsx`: Fitxer Excel generat amb les dades processades.

## Exemple d'Ús
```python
# Executeu l'script en Google Colab i seguiu les instruccions per seleccionar institucions i metadades.
# L'script generarà un fitxer Excel amb les dades processades i el descarregarà automàticament.
