[![ca](https://img.shields.io/badge/lang-ca-blue.svg)](https://github.com/CSUC/RDR-scripts/blob/main/move_dataset/README.md)
[![en](https://img.shields.io/badge/lang-en-green.svg)](https://github.com/CSUC/RDR-scripts/blob/main/move_dataset/README_ENG.md)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CSUC/RDR-scripts/blob/main/move_dataset/move_dataset_script.ipynb)
### Script de Moviment de Conjunts de Dades

Per a qualsevol consulta sobre el codi, contacteu amb rdr-contacte@csuc.cat.

## Objectiu del Script

Aquest script facilita el moviment d'un conjunt de dades d'una instància fins a una altre.

## Descripció

El script mou un conjunt de dades a una instància diferent utilitzant el DOI, el token API i l'alias de la instància de destinació proporcionats. Es comunica amb l'API de Dataverse per recuperar la informació del conjunt de dades i realitzar l'operació de moviment. En acabar, proporciona feedback sobre l'èxit o el fracàs de l'operació.

## Requeriments

Assegureu-vos que estan instal·lades les següents llibreries:
- pyDataverse
- requests

## Ús

1. **Valors d'Entrada:**
    - DOI: Introduïu el DOI del conjunt de dades.
    - Token: Proporcioneu el token API per a l'autenticació.
    - Alias: Especifiqueu l'alias de la instància de destinació.

2. **Execució:**
    - Executeu el script després de proporcionar els valors d'entrada necessaris.
    - El script intentarà moure el conjunt de dades a la instància especificada.
    - Mostrarà un missatge d'èxit o de fracàs segons el resultat de l'operació.
