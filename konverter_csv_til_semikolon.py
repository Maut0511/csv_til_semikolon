from pathlib import Path
import csv
import sys

SOURCE_DELIMITER = "\x1f"   # U+001F / Unit Separator
TARGET_DELIMITER = ";"      # Excel-venlig separator


def convert_file(input_file, output_file=None):
    input_path = Path(input_file)

    if not input_path.exists():
        print(f"Fejl: Filen findes ikke:\n{input_file}")
        input("\nTryk Enter for at lukke...")
        sys.exit(1)

    if not input_path.is_file():
        print(f"Fejl: Dette er ikke en fil:\n{input_file}")
        input("\nTryk Enter for at lukke...")
        sys.exit(1)

    if output_file is None:
        output_path = input_path.with_name(input_path.stem + "_excel.csv")
    else:
        output_path = Path(output_file)

    row_count = 0

    try:
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
                writer.writerow(row)
                row_count += 1

    except Exception as e:
        print("Der opstod en fejl under konverteringen:")
        print(str(e))
        input("\nTryk Enter for at lukke...")
        sys.exit(1)

    print("Færdig!")
    print(f"Antal rækker: {row_count}")
    print(f"Ny fil oprettet:\n{output_path}")
    input("\nTryk Enter for at lukke...")

    return output_path


def main():
    if len(sys.argv) < 2:
        print("Brug programmet ved at trække en CSV-fil hen på .exe-filen.")
        print("Du kan også køre det fra kommandolinjen med et filnavn som parameter.")
        input("\nTryk Enter for at lukke...")
        sys.exit(1)

    input_file = sys.argv[1]
    convert_file(input_file)


if __name__ == "__main__":
    main()