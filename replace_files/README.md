[![ca](https://img.shields.io/badge/lang-ca-blue.svg)](README.md)
[![en](https://img.shields.io/badge/lang-en-green.svg)](README_ENG.md)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CSUC/RDR-scripts/blob/main/replace_files/replace_files.ipynb)

# Script per reemplaçar fitxers d'un dataset a Dataverse

Per a qualsevol consulta sobre el codi, poseu-vos en contacte amb rdr-contacte@csuc.cat

## Descripció

Aquest script està dissenyat per interactuar amb el Repositori de Dades de Recerca CORA.RDR (https://dataverse.csuc.cat/) i permet reemplaçar fitxers existents d'un dataset de Dataverse a partir del seu DOI.

El script utilitza la llibreria `pyDataverse` per recuperar les metadades dels fitxers del dataset i l'API nativa de Dataverse per realitzar el reemplaçament.

El procés identifica automàticament el fitxer corresponent dins del dataset a partir del nom del fitxer local. També té en compte els fitxers tabulars que Dataverse pot ingerir i convertir a format `.tab`. Per exemple, si al dataset hi ha un fitxer `dades.tab` generat a partir d'un fitxer Excel o CSV, el script pot identificar que un nou fitxer local `dades.xlsx` o `dades.csv` correspon a aquest fitxer i reemplaçar-lo correctament.

El script conserva, sempre que estiguin disponibles, les metadades següents del fitxer original:

- Descripció.
- Carpeta o `directoryLabel`.
- Categories o etiquetes del fitxer.

També compara el checksum dels fitxers quan existeix una coincidència exacta de nom per evitar reemplaçar fitxers que no han canviat.

## Requisits

- Google Colab.
- Python 3.x.
- Llibreria `pyDataverse`.
- Llibreria `requests`.
- Token API de Dataverse.
- Permisos suficients sobre el dataset per poder reemplaçar fitxers.

La llibreria `pyDataverse` s'instal·la automàticament en executar el notebook de Google Colab si no està disponible.

## Ús

1. **Executar el notebook**
    - Obriu el notebook a Google Colab.
    - Executeu la cel·la principal fent clic al botó ▶.

2. **Introduir el token API**
    - Introduïu el vostre token API de CORA.RDR.
    - El token es pot obtenir des de:
      https://dataverse.csuc.cat/dataverseuser.xhtml?selectTab=apiTokenTab
    - El token s'introdueix de manera oculta i no es mostra a la pantalla.

3. **Introduir el DOI**
    - Introduïu únicament la part numèrica final del DOI.
    - Per exemple, si el DOI és:

      `doi:10.34810/data3724`

      només cal introduir:

      `3724`

    - El script construeix automàticament el DOI complet.

4. **Seleccionar els fitxers**
    - Google Colab mostrarà una finestra per seleccionar els fitxers que es volen reemplaçar.
    - Es poden seleccionar diversos fitxers alhora.
    - El nom del fitxer local s'utilitza per identificar el fitxer corresponent dins del dataset.

5. **Identificació del fitxer a Dataverse**
    - En primer lloc, el script busca una coincidència exacta del nom del fitxer.
    - Si no existeix una coincidència exacta i el fitxer és un format tabular compatible, el script comprova si Dataverse l'ha ingerit com a fitxer `.tab`.

    Per exemple:

    `2609 curation_status_checkpoint.xlsx`

    pot correspondre a:

    `2609 curation_status_checkpoint.tab`

6. **Reemplaçament**
    - Si el fitxer corresponent existeix, el script utilitza l'endpoint de reemplaçament de fitxers de Dataverse.
    - Es mantenen la descripció, la carpeta i les categories del fitxer original.
    - Si el fitxer té una coincidència exacta i el checksum és idèntic, el fitxer no es reemplaça.

7. **Resultat**
    - El script mostra un missatge per a cada fitxer indicant el resultat de l'operació.

    Exemples:

    `✅ Replaced: dades.xlsx`

    `⏭️ Not replaced (identical): README.txt`

    `⚠️ Not replaced (no matching file): exemple.csv`

    `❌ Error replacing dades.xlsx: [missatge d'error]`

## Fitxers tabulars ingerits per Dataverse

Dataverse pot processar determinats formats tabulars i generar una representació interna en format `.tab`.

El script contempla els formats següents:

- `.xlsx`
- `.xls`
- `.csv`
- `.tsv`
- `.sav`
- `.por`
- `.dta`
- `.rdata`
- `.rda`

Per aquests formats, si no es troba el nom original dins del dataset, el script prova automàticament de localitzar un fitxer amb el mateix nom base i extensió `.tab`.

Per exemple:

| Fitxer local | Fitxer a Dataverse |
|---|---|
| `dades.xlsx` | `dades.tab` |
| `resultats.csv` | `resultats.tab` |
| `enquesta.sav` | `enquesta.tab` |

## Comprovació de fitxers idèntics

Quan el nom del fitxer local coincideix exactament amb el nom del fitxer de Dataverse, el script compara el checksum del fitxer local amb el checksum registrat al repositori.

Els algoritmes compatibles són:

- MD5
- SHA-1
- SHA-256
- SHA-512

Si els dos checksums són idèntics, el fitxer no es reemplaça.

Aquesta comprovació no s'aplica quan un fitxer original, com ara `.xlsx` o `.csv`, correspon a una representació ingerida `.tab`, ja que els dos fitxers tenen continguts i checksums diferents.

## Metadades preservades

Durant el reemplaçament, el script intenta mantenir les metadades següents del fitxer existent:

- `description`
- `directoryLabel`
- `categories`

El reemplaçament es realitza amb l'opció `forceReplace` activada per permetre el reemplaçament quan el tipus de fitxer detectat canvia.

## Consideracions importants

- El script només reemplaça fitxers que ja existeixen al dataset.
- No afegeix fitxers nous.
- La identificació es basa principalment en el nom del fitxer.
- Si hi ha diversos fitxers amb el mateix nom en carpetes diferents del dataset, cal revisar el comportament abans d'utilitzar el script.
- Els fitxers reemplaçats generen una nova versió del fitxer dins de la versió de treball corresponent del dataset, segons el comportament de Dataverse.
- És recomanable comprovar el dataset després d'un reemplaçament massiu de fitxers.
- Cal disposar dels permisos necessaris al dataset.

## Estructura de Fitxers

- `replace_files_script.ipynb`: Notebook principal de Google Colab per reemplaçar fitxers.
- `README.md`: Documentació en català.
- `README_ENG.md`: Documentació en anglès.

## Exemple d'Ús

Si el dataset té el DOI:

```text
doi:10.34810/data3724
```

quan el script demani els últims dígits del DOI cal introduir:

```text
3724
```

A continuació, se seleccionen els fitxers que es volen reemplaçar des de l'ordinador.

Per exemple, si es selecciona:

```text
2609 curation_status_checkpoint.xlsx
```

i a Dataverse existeix:

```text
2609 curation_status_checkpoint.tab
```

el script identifica automàticament la correspondència i utilitza l'identificador del fitxer `.tab` per realitzar el reemplaçament amb el nou fitxer Excel.

## Contacte

Per a qualsevol consulta sobre el funcionament o el codi del script:

**rdr-contacte@csuc.cat**

