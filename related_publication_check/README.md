[![ca](https://img.shields.io/badge/lang-ca-blue.svg)](https://github.com/CSUC/RDR-scripts/blob/main/REVISAT/README.md)
[![en](https://img.shields.io/badge/lang-en-green.svg)](https://github.com/CSUC/RDR-scripts/blob/main/REVISAT/README_ENG.md)
# Script per a la Generació de Metadades de Publicacions Relacionades
Per a qualsevol consulta sobre el codi, poseu-vos en contacte amb rdr-contacte@csuc.cat

## Objectiu de l'Script

Aquest script permet avaluar i generar un tauler de metadades relacionades amb les publicacions associades a conjunts de dades. L'objectiu és extreure i agregar metadades específiques de cada conjunt de dades per a la seva posterior visualització i anàlisi en un fitxer Excel. A continuació, es presenta una guia detallada sobre com utilitzar l'script i les seves funcionalitats.

## Descripció de l'Script

L'script realitza les següents tasques:

1. **Extracció de Metadades:**
    - Extreu metadades específiques (com el tipus de relació de publicació, la citació de la publicació, ID de publicació, etc.) de diferents conjunts de dades utilitzant l'API.
    - Filtra les metadades a partir de les opcions seleccionades pel usuari.

2. **Agregació de Metadades:**
    - Les metadades s'agrupen per DOI per tal de combinar els valors associats a cada conjunt de dades.
    - S'assegura que els valors per cada DOI estan formats correctament i es mostren com a llistes concatenades quan es repeteixen.

3. **Creació d'un Tauler de Metadades:**
    - Crea un DataFrame a partir de les metadades agregades, mostrant les metadades seleccionades i les institucions associades a cada DOI.
    - Ordena els resultats per DOI i formata els enllaços DOI per a la seva visualització.

4. **Exportació a Excel:**
    - Un cop generat el tauler de metadades, l'script guarda les dades en un fitxer Excel per facilitar la seva consulta i ús posterior.

## Instruccions

1. **Valors d'Entrada:**
    - **Opcions de Metadades:** Seleccioneu les metadades que voleu extreure (ex. `publicationRelationType`, `publicationCitation`, etc.).
    - **DOIs i Institucions:** L'script obté les dades a partir de les institucions i els DOIs associats als conjunts de dades.

2. **Execució:**
    - Executeu l'script després de proporcionar les opcions de metadades i la llista de conjunts de dades.
    - L'script farà les operacions de filtrat i agregació de metadades per crear el tauler.

3. **Descarregar el Fitxer Excel:**
    - Un cop generat el tauler, l'script us proporcionarà un enllaç per descarregar el fitxer Excel amb les metadades generades.

4. **Format del Fitxer Excel:**
    - El fitxer contindrà les següents columnes: DOI, Institució, i les metadades seleccionades.

## Exemple de Sortida

| DOI                                | Institució | publicationRelationType | publicationCitation | publicationIDType | publicationIDNumber | publicationURL |
|------------------------------------|-------------|-------------------------|---------------------|--------------------|----------------------|----------------|
| https://doi.org/10.34810/dataXXX   | UB          | ...                     | ...                 | ...                | ...                  | ...            |
| https://doi.org/10.34810/dataXXX   | UAB         | ...                     | ...                 | ...                | ...                  | ...            |

## Limitacions i Consideracions

- L'script depèn de les dades proporcionades pels conjunts de dades associats als DOIs.
- Pot ser necessari adaptar l'script si s'han de seleccionar metadades addicionals no contemplades inicialment.

Per a qualsevol consulta o problema relatiu al procés, poseu-vos en contacte amb el mantenidor de l'script.
