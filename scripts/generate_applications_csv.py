"""Generate applications.csv from CMS-managed YAML files."""

import csv
from pathlib import Path

import yaml


CONTENT_DIR = Path("content/applications")
OUTPUT_CSV = Path("spreadsheets/applications.csv")

FIELDNAMES = [
    "image",
    "alt",
    "category_title",
    "project_name",
    "modal_id",
    "caption",
    "partners",
    "description",
    "funding",
    "homepage_url",
    "project_href",
]


def main():
    """Read application YAML files and generate the CSV."""

    applications = []

    for path in CONTENT_DIR.glob("*.yml"):
        with path.open(encoding="utf-8") as file:
            application = yaml.safe_load(file)

        row = {
            field: application.get(field, "") or ""
            for field in FIELDNAMES
        }

        row["order"] = int(application.get("order", 9999))
        applications.append(row)

    if not applications:
        raise ValueError("No application YAML files found.")

    # Preserve the original card order.
    applications.sort(key=lambda row: row["order"])

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_CSV.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()

        for application in applications:
            application.pop("order")
            writer.writerow(application)

    print(f"Generated {OUTPUT_CSV} with {len(applications)} applications.")


if __name__ == "__main__":
    main()
