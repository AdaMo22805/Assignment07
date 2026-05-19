"""Clean an events CSV: drop invalid rows and normalize timestamps to ISO 8601."""

import csv
import os
import sys
from datetime import datetime

print('cleaning...')

VALID_EVENT_TYPES = {"click", "login", "view", "scroll", "purchase"}

TIMESTAMP_FORMATS = (
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d %H:%M:%S.%f",
    "%Y-%m-%d %H:%M:%S",
    "%m/%d/%Y %H:%M:%S",
)

FIELDNAMES = ["user_id", "timestamp", "event_type", "duration_seconds"]


def normalize_timestamp(value: str) -> str | None:
    """Parse a timestamp in any known format and return YYYY-MM-DDTHH:MM:SS."""
    for fmt in TIMESTAMP_FORMATS:
        try:
            return datetime.strptime(value, fmt).strftime("%Y-%m-%dT%H:%M:%S")
        except ValueError:
            continue
    return None


def clean(input_path: str, output_path: str) -> None:
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(input_path, newline="") as infile, open(output_path, "w", newline="") as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=FIELDNAMES)
        writer.writeheader()

        for row in reader:
            if any(row.get(field) is None or not row[field].strip() for field in FIELDNAMES):
                continue

            event_type = row["event_type"].strip()
            if event_type not in VALID_EVENT_TYPES:
                continue

            try:
                duration = int(row["duration_seconds"])
            except ValueError:
                continue
            if duration <= 0:
                continue

            timestamp = normalize_timestamp(row["timestamp"].strip())
            if timestamp is None:
                continue

            writer.writerow({
                "user_id": row["user_id"].strip(),
                "timestamp": timestamp,
                "event_type": event_type,
                "duration_seconds": duration,
            })


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python clean.py <input_csv> <output_csv>", file=sys.stderr)
        sys.exit(1)
    clean(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
