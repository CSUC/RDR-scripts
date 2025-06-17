# ======================== PARAMETERS ========================
EXCEL_FILENAME = "your_excel_file.xlsx"   # Replace with your Excel file name
SEPARATE_TABLES = True  # Set to False if you want to save entire sheets without splitting
# ============================================================

import os
import shutil
import pandas as pd

def detect_and_save_tables(sheet_name, df):
    """
    Splits a DataFrame by empty rows into multiple CSV tables.
    """
    tables = []
    current_table = []

    for index, row in df.iterrows():
        if row.isnull().all():
            if current_table:
                tables.append(current_table.copy())
                current_table = []
        else:
            current_table.append(row)

    if current_table:
        tables.append(current_table.copy())

    csv_files = []
    for i, table in enumerate(tables):
        table_df = pd.DataFrame(table)
        csv_file = f"{sheet_name}_{i+1}.csv"
        table_df.to_csv(csv_file, index=False, header=False)
        csv_files.append(csv_file)

    return csv_files

def process_excel(file_path, separate_tables=True):
    """
    Processes the Excel file to extract sheets and convert them to CSV.
    Optionally splits sheets into separate tables.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Excel file '{file_path}' not found.")

    # Read Excel file
    try:
        xls_file = pd.ExcelFile(file_path)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    # Create directory based on file name
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    os.makedirs(base_name, exist_ok=True)

    for sheet_name in xls_file.sheet_names:
        df = pd.read_excel(xls_file, sheet_name=sheet_name, header=None)

        if separate_tables:
            csv_files = detect_and_save_tables(sheet_name, df)
        else:
            csv_file = f"{sheet_name}.csv"
            df.to_csv(csv_file, index=False, header=False)
            csv_files = [csv_file]

        for csv_file in csv_files:
            target_path = os.path.join(base_name, csv_file)
            if os.path.exists(target_path):
                os.remove(target_path)
            shutil.move(csv_file, target_path)

    # Create ZIP archive
    zip_filename = shutil.make_archive(base_name, 'zip', base_name)
    print(f"\n✅ Process complete. ZIP file created: {zip_filename}")

# Run the processing
process_excel(EXCEL_FILENAME, SEPARATE_TABLES)
