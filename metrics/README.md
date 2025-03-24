[![ca](https://img.shields.io/badge/lang-ca-blue.svg)](https://github.com/CSUC/RDR-scripts/blob/main/metrics/README.md)
[![en](https://img.shields.io/badge/lang-en-green.svg)](https://github.com/CSUC/RDR-scripts/blob/main/metrics/README_ENG.md)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CSUC/RDR-scripts/blob/main/metrics/metrics_script.ipynb)
# Script per extreure mètriques dels datasets d'una instància

Aquest script permet extreure mètriques dels datasets d'una instància de Dataverse utilitzant l'API de Dataverse. Les mètriques inclouen visualitzacions totals, visualitzacions úniques, descàrregues totals, descàrregues úniques i citacions.

## Objectiu

L'objectiu principal és facilitar l'obtenció de mètriques dels datasets en una instància específica de Dataverse. Les dades es poden exportar a un fitxer Excel per a la seva posterior anàlisi.

## Requeriments

Aquest script requereix les següents llibreries:

- `pyDataverse`
- `numpy`
- `pandas`
- `openpyxl`
- `requests`

A més, cal disposar d'un compte amb permisos suficients en l'instància de Dataverse i un token privat per accedir a l'API.

## Instruccions d'ús

1. **Executar l'script en Google Colab:**
   - L'script està preparat per ser executat en Google Colab. Copia el codi en una cel·la de Google Colab i segueix les instruccions indicades a les cel·les de markdown i codi.

2. **Instal·lar les llibreries necessàries:**
   - Executa la cel·la amb el títol *"Instal·lar o actualitzar llibreries"*. Això instal·larà totes les dependències requerides.

3. **Introduir el token i l'alias de la institució:**
   - Proporciona el teu token privat i l'alias de la institució quan se't sol·liciti.

4. **Executar l'obtenció de mètriques:**
   - Executa les cel·les corresponents per extreure les mètriques dels datasets.

5. **Guardar les mètriques en un fitxer Excel:**
   - L'script genera un fitxer Excel amb les mètriques extretes. Executa la cel·la final per descarregar el fitxer al teu ordinador.

## Estructura del fitxer Excel

El fitxer Excel tindrà les següents columnes:

- **DOI:** Identificador persistent del dataset.
- **Total Views:** Total de visualitzacions del dataset.
- **Unique Views:** Total de visualitzacions úniques del dataset.
- **Total Downloads:** Total de descàrregues del dataset.
- **Unique Downloads:** Total de descàrregues úniques del dataset.
- **Citations:** Nombre total de citacions.

## Exemples d'ús

### Obtenció de mètriques

1. Introduir l'alias de la institució i el token:
