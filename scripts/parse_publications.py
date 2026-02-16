import csv
import json
import os

def parse_authors(author_str):
    """
    Parses a semicolon-separated string of authors into a list of dictionaries with 'family' and 'given' names.
    """
    authors = []
    # Split by semicolon as seen in the CSV
    names = [n.strip() for n in author_str.split(';')]
    for name in names:
        if not name:
            continue
        parts = name.split(' ')
        if len(parts) > 1:
            # Assume the last part is the family name
            family = parts[-1]
            given = " ".join(parts[:-1])
        else:
            family = name
            given = ""
        authors.append({"family": family, "given": given})
    return authors

def convert_csv_to_json(csv_path, json_path):
    """
    Converts a publications CSV file to a JSON file in CSL-JSON format.
    """
    publications = []

    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return

    with open(csv_path, mode='r', encoding='utf-8') as f:
        # The CSV header is: Title,Authors,Conference,Link
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            # Extract basic info
            title = row.get("Title", "").strip()
            authors_str = row.get("Authors", "").strip()
            conference = row.get("Conference", "").strip()
            link = row.get("Link", "").strip()

            # Create the JSON object structure based on the format in _data/publications.json
            pub = {
                "id": f"paper_{i+1}", # Generate a simple ID
                "type": "paper-conference", # Default type
                "title": title,
                "container-title": conference,
                "URL": link,
                "author": parse_authors(authors_str),
                # Empty properties as requested/seen in existing format
                "page": "",
                "volume": "",
                "issue": "",
                "source": "",
                "abstract": "",
                "DOI": "",
                "issued": {
                    "date-parts": [
                        [
                            # Extract year from conference name if possible (e.g., "WACV 2026")
                            "".join(filter(str.isdigit, conference))[:4] if any(char.isdigit() for char in conference) else "2025"
                        ]
                    ]
                }
            }
            publications.append(pub)

    # Write the resulting list to the JSON file
    with open(json_path, mode='w', encoding='utf-8') as f:
        json.dump(publications, f, indent=4, ensure_ascii=False)

    print(f"Successfully converted {len(publications)} publications to {json_path}")

if __name__ == "__main__":
    # Define paths relative to the project root or absolute as requested
    # Determine the project root (parent directory of the 'scripts' folder)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_file = os.path.join(base_dir, "_data/raw_publications.csv")
    json_file = os.path.join(base_dir, "_data/publications.json")

    convert_csv_to_json(csv_file, json_file)
