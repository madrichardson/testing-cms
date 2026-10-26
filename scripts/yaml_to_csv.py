"""Convert CMS-managed project information from YAML to CSV."""

import csv
from pathlib import Path

import yaml


def main():
    """Convert the project records into a CSV file."""

    input_path = Path("content/projects.yml")
    output_path = Path("data/projects.csv")

    with input_path.open(encoding="utf-8") as file:
        content = yaml.safe_load(file)

    projects = content["projects"]

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["name", "status", "last_updated"],
        )

        writer.writeheader()
        writer.writerows(projects)


if __name__ == "__main__":
    main()
