from pathlib import Path
import csv
import sys

SOURCE_DELIMITER = "\x1f"   # U+001F
TARGET_DELIMITER = ";"      # Dansk Excel

def clean_field(value: str) -> str:
    if value is None:
        return ""
    # Gør linjeskift Excel-sikre
    value = value.replace("\r\n", " | ")
    value = value.replace("\n", " | ")
    value = value.replace("\r", " | ")
    return value.strip()

def convert_to_excel_csv(input_file, output_file=None):
    input_path = Path(input_file)

    if not input_path.exists():
        print(f"Fejl: Filen findes ikke: {input_file}")
        sys.exit(1)

    if output_file is None:
        output_path = input_path.with_name(input_path.stem + "_excelvenlig.csv")
    else:
        output_path = Path(output_file)

    row_count = 0

    with input_path.open("r", encoding="utf-8", newline="") as infile, \
         output_path.open("w", encoding="utf-8-sig", newline="") as outfile:

        reader = csv.reader(infile, delimiter=SOURCE_DELIMITER)
        writer = csv.writer(
            outfile,
            delimiter=TARGET_DELIMITER,
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL
        )

        for row in reader:
            cleaned_row = [clean_field(field) for field in row]
            writer.writerow(cleaned_row)
            row_count += 1

    print("Færdig!")
    print(f"Antal rækker skrevet: {row_count}")
    print(f"Ny fil: {output_path}")

def main():
    if len(sys.argv) < 2:
        print("Brug:")
        print("  python konverter_csv_til_semikolon.py <inputfil.csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) >= 3 else None

    convert_to_excel_csv(input_file, output_file)

if __name__ == "__main__":
    main()
