import json
import os
from jinja2 import Template

def load_cv_data(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

def generate_cv(template_path, json_path, output_path):
    # Charger les données
    cv_data = load_cv_data(json_path)
    
    # Charger le template
    with open(template_path, 'r', encoding='utf-8') as f:
        template = Template(f.read())
    
    # Générer le CV
    cv_content = template.render(**cv_data)
    
    # Créer le dossier output s'il n'existe pas
    ensure_dir(output_path)
    
    # Sauvegarder le résultat
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cv_content)

if __name__ == "__main__":
    generate_cv(
        "templates/cv_template.tex",
        "data/cv_data.json",
        "output/cv.tex"
    ) 