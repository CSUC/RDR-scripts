[![ca](https://img.shields.io/badge/lang-ca-blue.svg)](https://github.com/CSUC/RDR-scripts/blob/main/verification_readme/README.md)
[![en](https://img.shields.io/badge/lang-en-green.svg)](https://github.com/CSUC/RDR-scripts/blob/main/verification_readme/README_ENG.md)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CSUC/RDR-scripts/blob/main/verification_readme/verification_readme_script.ipynb)

# Script per verificar si els datasets tenen fitxer Readme

Aquest script comprova automàticament si els datasets d’una institució en Dataverse tenen un fitxer de tipus Readme, i exporta aquesta informació a un fitxer Excel. També indica si el dataset està publicat o en estat esborrany.

## Objectiu

L’objectiu principal és facilitar la identificació dels datasets que compleixen el requisit mínim de documentació amb un fitxer `Readme`, cosa essencial per a la qualitat i comprensió de les dades publicades.

## Requeriments

Aquest script utilitza les següents llibreries:

- `pandas`
- `IPython.display` (per mostrar la taula i descarregar el fitxer en Colab)
- `google.colab` (opcional, per gestionar la descàrrega en entorns Colab)
- Una configuració prèvia amb l'API i l'institució (`config`, `opcions`, `base_url`, `token`)

## Instruccions d’ús

1. **Executar l’script en Google Colab:**
   - El codi està preparat per funcionar a Colab. Només cal copiar-lo i executar-lo cel·la a cel·la.

2. **Seleccionar la institució:**
   - Indica una o diverses institucions de la llista `opcions`.

3. **Executar la comprovació:**
   - L’script iterarà per tots els datasets de cada institució i analitzarà si tenen un fitxer `Readme`.

4. **Descarregar els resultats:**
   - Es genera un fitxer `datasets_sizes.xlsx` que es pot descarregar des del mateix Colab.

## Estructura del fitxer Excel

El fitxer Excel generat conté la següent informació:

- **DOI:** Enllaç persistent al dataset.
- **Published:** Indica si el dataset està publicat o no (`Published` o `Draft`).
- **Institution:** Alias de la institució analitzada.
- **Is there Readme?:** Sí (`Yes`) si s’ha trobat un fitxer que conté la paraula `readme`, No (`No`) en cas contrari.
- **Readme file name:** Nom(s) del(s) fitxer(s) `Readme` detectats.

## Exemple de sortida

| DOI                                  | Published | Institution | Is there Readme? | Readme file name    |
|-------------------------------------|-----------|-------------|------------------|----------------------|
| https://doi.org/10.34810/data1234   | Published | upf         | Yes              | readme_dataset.txt   |
| https://doi.org/10.34810/data1235   | Draft     | udl         | No               |                      |

## Consideracions

- El script busca el terme `readme` al nom del fitxer de manera insensible a majúscules/minúscules.
- Els datasets en esborrany (`Draft`) també són analitzats.

## Autor

Script creat per [CSUC](https://www.csuc.cat/) com a part dels scripts de manteniment i validació de repositoris de dades basats en Dataverse.

---
