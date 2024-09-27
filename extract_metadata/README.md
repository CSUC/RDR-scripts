# Script d'Exportació Automàtica de Metadades per dataset

Per a qualsevol consulta relacionada amb el codi, poseu-vos en contacte amb rdr-contacte@csuc.cat.

## Objectiu de l'Script
Aquest script automatitza l'extracció i exportació de metadades d'un conjunt de dades a Dataverse.

## Descripció

El script recupera les metadades d'un conjunt de dades especificat utilitzant el DOI i el token proporcionats. A continuació, organitza les metadades en un DataFrame i les exporta a un fitxer CSV. El script és capaç de funcionar tant a l'entorn de Google Colab com a Jupyter Notebook, oferint opcions còmodes per descarregar el fitxer de metadades.

## Requisits

Assegureu-vos que les següents llibreries estiguin instal·lades:
- pyDataverse
- html2text
- pandas
- ipywidgets (per a Google Colab)

## Ús

1. **Valors d'Entrada:**
    - DOI: Introduïu el DOI del conjunt de dades.
    - Token: Proporcioneu el token d'API per autenticació.
    - URL Base: Especifiqueu l'URL del repositori Dataverse.

2. **Execució:**
    - Executeu l'script després de proporcionar els valors d'entrada necessaris.
    - L'script extreura les metadades del conjunt de dades i les organitzarà en un DataFrame.
    - El DataFrame es guardarà com a fitxer CSV al directori especificat.

3. **Opcions de Descàrrega:**
    - **Google Colab:** Si s'està executant a Google Colab, es proporcionarà un botó de descàrrega per descarregar el fitxer de metadades.
    - **Jupyter Notebook:** A Jupyter Notebook, es mostrarà un enllaç de descàrrega per descarregar el fitxer de metadades.
