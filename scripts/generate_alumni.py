import pandas as pd
from datetime import date
import os
import re
import hashlib

def slugify(text):
    """
    Convert text to a URL-friendly slug.
    """
    text = text.lower()
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'[^\w\-]', '', text)
    return text

def create_alumni_posts():
    # Define absolute paths
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_path, '_data/alumni.csv')
    output_dir = os.path.join(base_path, '_pages/team/_posts')

    # Ensure output directory exists and cleanup old alumni files
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        # Delete existing alumni files to avoid duplication/leftovers
        for filename in os.listdir(output_dir):
            if filename.endswith(".md"):
                file_path = os.path.join(output_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        if 'category: alumni' in f.read():
                            os.remove(file_path)
                except Exception:
                    pass

    # Read the alumni CSV data
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    for _, row in df.iterrows():
        name = str(row['영문 이름']).strip().title()

        # Use "비고" for affiliation and translate
        remark = str(row['비고 (영문)']).strip()
        if remark.lower() == 'nan' or not remark:
            remark = ''

        # Prepare the frontmatter
        content = f"""---
layout: member
category: alumni
name: {name}
title: {name}
affiliation: {remark}
---
"""

        # Generate a unique filename: YYYY-MM-DD-researcher-slugifiedname-hash.md
        timestamp = '2026-02-12'

        # Using name for hash as email might be empty for some alumni.
        name_hash = hashlib.md5(name.encode()).hexdigest()[:4]
        slug_name = slugify(name)
        filename = f"{timestamp}-researcher-{slug_name}-{name_hash}.md"
        file_path = os.path.join(output_dir, filename)

        # Write the file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Created {filename}")
        except Exception as e:
            print(f"Error writing file {filename}: {e}")

if __name__ == "__main__":
    create_alumni_posts()
