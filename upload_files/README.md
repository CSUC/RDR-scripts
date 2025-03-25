[![ca](https://img.shields.io/badge/lang-ca-blue.svg)](https://github.com/CSUC/RDR-scripts/blob/main/upload_files/README.md)
[![en](https://img.shields.io/badge/lang-en-green.svg)](https://github.com/CSUC/RDR-scripts/blob/main/upload_files/README_ENG.md)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CSUC/RDR-scripts/blob/main/upload_files/upload_files_script.ipynb)
# Script per a la pujada automàtica de fitxers

Per a qualsevol consulta sobre el codi, poseu-vos en contacte amb rdr-contacte@csuc.cat

## Objectiu de l'script

Aquest script facilita la pujada automàtica de fitxers a un conjunt de dades al Dataverse utilitzant les metadades proporcionades en un fitxer Excel.

## Visió general de l'script

### Requisits previs
- Assegureu-vos que els fitxers de l'script i els fitxers a pujar es trobin al mateix directori.
- En Google Colab, pugeu el fitxer Excel utilitzant la icona "Penjar fitxers".

### Requisits del fitxer Excel de metadades
1. La primera fila serveix com a capçalera i ha de contenir els següents noms de variables en l'ordre especificat:
    - Nom del fitxer
    - Descripció
    - Ruta del fitxer
    - Etiqueta
2. Cada fila posterior correspon a un fitxer a pujar.
3. El nom del fitxer (Nom del fitxer) és obligatori i s'ha d'escriure correctament, incloent-hi l'extensió del fitxer.
4. Deixeu buida qualsevol cel·la si la informació corresponent no està disponible.
5. Si un valor de metadades conté un número, encerreu-lo entre cometes.
6. Per a la variable 'Etiqueta', si s'han d'aplicar diverses etiquetes, separeu-les amb una coma.

### Paràmetres de la funció
- `base_url`: URL base del repositori Dataverse.
- `token`: Token d'API per a l'autenticació.
- `doi`: DOI del conjunt de dades.
- `excel_file_name`: Nom del fitxer Excel que conté les metadades.

### Ús
- Executeu l'script proporcionant els valors d'entrada necessaris.
- L'script llegirà les metadades del fitxer Excel, verificarà l'existència del fitxer i pujarà els fitxers al conjunt de dades segons correspongui.
- En acabar, l'script mostrarà missatges que indiquen la correcta pujada dels fitxers o els errors detectats.
