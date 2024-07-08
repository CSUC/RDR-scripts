# Convertidor de Delimitador CSV

Per a qualsevol consulta sobre el codi, contacteu amb [rdr-contacte@csuc.cat](mailto:rdr-contacte@csuc.cat)

## Descripció
Aquest script està dissenyat per convertir fitxers CSV separats per punts i comes a fitxers CSV separats per comes. Permet als usuaris carregar un o diversos fitxers CSV separats per punts i comes, que després es processen i es guarden amb delimitadors de comes. Els fitxers processats es comprimeixen junts i es posen a disposició per a la descàrrega.

## Requisits
- Python 3.x
- Llibreria ipywidgets
- Google Colab (per a ús interactiu)

## Ús
1. **Carregar Fitxers CSV**:
    - Feu clic al botó "Upload" per seleccionar un o més fitxers CSV separats per punts i comes per a la conversió.

2. **Processar Fitxers CSV**:
    - L'script convertirà automàticament els fitxers carregats a format CSV separat per comes.
    - Cada fitxer processat es guardarà amb el sufix `_new.csv`.

3. **Descarregar Fitxers Processats**:
    - Un cop completada la conversió, es descarregarà automàticament un fitxer zip que conté tots els fitxers CSV processats.

## Estructura dels Fitxers
- `csv_delimiter_converter.ipynb`: L'script principal per convertir fitxers CSV de delimitador per punt i coma a delimitador per coma.
- `example_semicolon.csv`: Exemple de fitxer CSV separat per punts i comes per a proves.
- `processed_csv_files.zip`: Exemple de sortida que conté els fitxers CSV generats separats per comes.

## Exemple d'Ús
```python
# Executeu l'script i seguiu les instruccions per carregar fitxers CSV separats per punts i comes.
# L'script convertirà cada fitxer carregat a format separat per comes i descarregarà els fitxers generats com a un arxiu zip.
