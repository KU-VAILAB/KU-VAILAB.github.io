import csv
import json
import os
import re

def parse_authors(author_str):
    """
    Parses a comma-separated string of authors into a list of dictionaries with 'family' and 'given' names.
    """
    authors = []
    # Split by comma as seen in the new CSV
    names = [n.strip() for n in author_str.split(',')]
    for name in names:
        if not name:
            continue
        # Replace special spaces (like \u2004) with regular spaces
        clean_name = re.sub(r'\s+', ' ', name).strip()
        parts = clean_name.split(' ')
        if len(parts) > 1:
            # Assume the last part is the family name
            family = parts[-1]
            given = " ".join(parts[:-1])
        else:
            family = clean_name
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

    with open(csv_path, mode='r', encoding='utf-8-sig') as f:
        # The new CSV headers are: 연도,학회명,Oral 등,논문 제목,링크,저자 목록
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            # Extract basic info
            year = row.get("연도", "").strip()
            conf_name = row.get("학회명", "").strip()
            oral_info = row.get("Oral 등", "").strip()
            title = row.get("논문 제목", "").strip()
            link = row.get("링크", "").strip()
            authors_str = row.get("저자 목록", "").strip()

            if not title: # Skip empty rows
                continue

            # Construct container-title: {학회명} {연도} ({Oral 등})
            container_title = f"{conf_name} {year}"
            if oral_info:
                container_title += f" ({oral_info})"

            # Create the JSON object structure based on the format in _data/publications.json
            pub = {
                "id": f"paper_{i+1}",
                "type": "paper-conference",
                "title": title,
                "container-title": container_title,
                "URL": link,
                "author": parse_authors(authors_str),
                "page": "",
                "volume": "",
                "issue": "",
                "source": "",
                "abstract": "",
                "DOI": "",
                "issued": {
                    "date-parts": [
                        [year]
                    ]
                }
            }
            publications.append(pub)

    # Sort publications: primary by year (descending), secondary by title (ascending)
    publications.sort(key=lambda x: (-int(x['issued']['date-parts'][0][0] or 0), x['title']))

    # Re-assign IDs after sorting to maintain sequential order (paper_1, paper_2, ...)
    for i, pub in enumerate(publications):
        pub["id"] = f"paper_{i+1}"

    # Write the resulting list to the JSON file
    with open(json_path, mode='w', encoding='utf-8') as f:
        json.dump(publications, f, indent=4, ensure_ascii=False)

    print(f"Successfully converted {len(publications)} publications to {json_path}")

if __name__ == "__main__":
    # Define paths relative to the project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_file = os.path.join(base_dir, "_data/new_raw_publications.csv")
    json_file = os.path.join(base_dir, "_data/publications.json")

    convert_csv_to_json(csv_file, json_file)
