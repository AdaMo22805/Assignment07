"""Add `duration_minutes` and `weekday` feature columns."""

import csv
import sys
from datetime import date

print('creating features...')

def features(input_path: str, output_path: str) -> None:
    with open(input_path, newline="") as infile, open(output_path, "w", newline="") as outfile:
        reader = csv.DictReader(infile)
        fieldnames = [*reader.fieldnames, "duration_minutes", "weekday"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            row["duration_minutes"] = int(row["duration_seconds"]) / 60
            row["weekday"] = date.fromisoformat(row["date"]).strftime("%A")
            writer.writerow(row)


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python features.py <input_csv> <output_csv>", file=sys.stderr)
        sys.exit(1)
    features(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
