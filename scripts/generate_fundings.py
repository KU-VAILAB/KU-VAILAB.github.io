import os
import yaml

def generate_fundings_yaml():
    base_path = '/Users/woosung/Desktop/KU/LabIntern/vai-lab-website'
    fundings_dir = os.path.join(base_path, 'images/research/Fundings')
    output_file = os.path.join(base_path, '_data/fundings.yml')

    if not os.path.exists(fundings_dir):
        print(f"Directory not found: {fundings_dir}")
        return

    # List all image files in the Fundings directory
    valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')
    funding_images = []

    for filename in sorted(os.listdir(fundings_dir)):
        if filename.lower().endswith(valid_extensions):
            # Paths in Jekyll should be relative to the site root or use relative_url
            # Here we store them as absolute-from-root paths
            funding_images.append(f"/images/research/Fundings/{filename}")

    # Write to fundings.yml
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(funding_images, f, allow_unicode=True, default_flow_style=False)
        print(f"Successfully generated {output_file} with {len(funding_images)} items.")
    except Exception as e:
        print(f"Error writing YAML: {e}")

if __name__ == "__main__":
    generate_fundings_yaml()
