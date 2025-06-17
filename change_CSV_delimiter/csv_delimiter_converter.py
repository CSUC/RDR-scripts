import os
import csv
import shutil
import chardet
from io import StringIO

# -------------------- PARAMETERS --------------------
# Directory containing original CSV files
input_directory = "csv_input"      # <-- Make sure this folder exists and contains the original CSV files

# Directory to save processed CSV files
output_directory = "processed_csv_files"

# ----------------------------------------------------

# Detect encoding using chardet
def detect_encoding(byte_content):
    result = chardet.detect(byte_content)
    return result['encoding'] or 'utf-8'

# Process CSV content: convert ; → , and quote fields with commas
def process_csv(byte_content, original_filename):
    encoding = detect_encoding(byte_content)
    print(f"Detected encoding for {original_filename}: {encoding}")

    decoded_text = byte_content.decode(encoding, errors='replace')

    input_io = StringIO(decoded_text)
    reader = csv.reader(input_io, delimiter=';', quotechar='"')

    output_lines = []

    for row in reader:
        new_fields = []
        for field in row:
            field = field.strip()
            if ',' in field or '"' in field:
                field = field.replace('"', '""')
                field = f'"{field}"'
            new_fields.append(field)
        output_lines.append(','.join(new_fields))

    return '\n'.join(output_lines)

# Main processing function
def process_files():
    if not os.path.exists(input_directory):
        print(f"❌ Input directory '{input_directory}' does not exist.")
        return

    os.makedirs(output_directory, exist_ok=True)
    processed_count = 0

    for filename in os.listdir(input_directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_directory, filename)
            with open(file_path, 'rb') as f:
                byte_content = f.read()

            new_filename = os.path.splitext(filename)[0] + "_converted.csv"
            processed_content = process_csv(byte_content, filename)

            if processed_content:
                output_path = os.path.join(output_directory, new_filename)
                with open(output_path, 'w', encoding='utf-8-sig', newline='') as out_file:
                    out_file.write(processed_content)
                processed_count += 1

    if processed_count == 0:
        print("⚠️ No .csv files were processed.")
    else:
        zip_path = shutil.make_archive(output_directory, 'zip', output_directory)
        print(f"✅ Successfully processed {processed_count} file(s).")
        print(f"📦 Zipped output available at: {zip_path}")

if __name__ == "__main__":
    print("=== CSV Converter ===")
    print(f"Reading files from: {input_directory}")
    print(f"Processed files will be saved in: {output_directory}")
    process_files()
