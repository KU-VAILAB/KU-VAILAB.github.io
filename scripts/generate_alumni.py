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
    base_path = '/Users/woosung/Desktop/KU/LabIntern/vai-lab-website'
    csv_path = os.path.join(base_path, '_data/alumni.csv')
    output_dir = os.path.join(base_path, '_pages/team/_posts')

    # Name translation mapping
    name_map = {
        "정혜지": "Hyeji Jeong",
        "박노경": "Nokyung Park",
        "정유진": "Yujin Jeong",
        "박성범": "Sungbeom Park",
        "장민철": "Mincheol Chang",
        "우현": "Hyun Woo",
        "윤현주": "Hyunjoo Yoon",
        "채대원": "Daewon Chae",
        "박홍빈": "Hongbeen Park",
        "서다빈": "Dabin Seo",
        "박민정": "Minjeong Park"
    }

    # "비고" translation mapping
    affiliation_map = {
        "UBC 박사 유학": "Ph.D. Student at UBC",
        "네이버 입사": "Naver",
        "독일 박사 유학": "Ph.D. Student in TU-Darmstadt",
        "LG CNS": "LG CNS",
        "미시간 박사": "Ph.D. Student at University of Michigan",
        "펜실베니아 박사": "Ph.D. Student at University of Pennsylvania",
        "TBD": ""
    }

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

    # Use today's date for the filename prefix
    today_str = date.today().strftime('%Y-%m-%d')

    for _, row in df.iterrows():
        korean_name = str(row['이름']).strip()
        name = name_map.get(korean_name, korean_name)

        # Use "비고" for affiliation and translate
        remark = str(row['비고']).strip()
        if remark.lower() == 'nan' or not remark:
            affiliation = ''
        else:
            affiliation = affiliation_map.get(remark, remark)

        # Prepare the frontmatter
        content = f"""---
layout: member
category: alumni
name: {name}
title: {name}
affiliation: {affiliation}
---
"""

        # Generate a unique filename: YYYY-MM-DD-researcher-slugifiedname-hash.md
        # Using name for hash as email might be empty for some alumni.
        name_hash = hashlib.md5(name.encode()).hexdigest()[:4]
        slug_name = slugify(name)
        filename = f"{today_str}-researcher-{slug_name}-{name_hash}.md"
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
