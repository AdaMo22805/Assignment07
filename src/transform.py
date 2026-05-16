"""Add a `date` column derived from the `timestamp` column."""

import csv
import os
import sys

print('transforming...')

def transform(input_path: str, output_path: str) -> None:
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(input_path, newline="") as infile, open(output_path, "w", newline="") as outfile:
        reader = csv.DictReader(infile)
        fieldnames = [*reader.fieldnames, "date"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            row["date"] = row["timestamp"].split("T", 1)[0]
            writer.writerow(row)


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python transform.py <input_csv> <output_csv>", file=sys.stderr)
        sys.exit(1)
    transform(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
