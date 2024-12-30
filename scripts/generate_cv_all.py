import json
import os
import sys
from pathlib import Path

def load_cv_data(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def clean_text(text):
    """Nettoie le texte pour LaTeX"""
    if isinstance(text, (list, dict)):
        return text
    
    # Traitement spécial pour "Top X%"
    if "%" in str(text) and "Top" in str(text):
        return text.replace("%", "\\%")
    
    text = str(text)
    text = text.replace("'", "'")
    
    replacements = {
        '&': '\\&',
        '%': '\\%',
        '$': '\\$',
        '#': '\\#',
        '_': '\\_',
        '{': '\\{',
        '}': '\\}',
        '~': '\\textasciitilde{}',
        '^': '\\textasciicircum{}',
        '\\': '\\textbackslash{}',
        '@': '\\@',
        '<': '\\textless{}',
        '>': '\\textgreater{}',
        '|': '\\textbar{}',
        '`': '\\`{}',
        '"': "''",
        '--': '---'
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text

def generate_header(personal):
    header = []
    header.append("\\begin{center}")
    header.append(f"    \\small \\faPhone\\ \\texttt{{{personal['phone']}}} \\hspace{{1pt}} $|$")
    header.append(f"    \\hspace{{1pt}} \\faEnvelope\\ \\texttt{{{personal['email']}}} \\hspace{{1pt}} $|$")
    header.append(f"    \\hspace{{1pt}} \\faLinkedin\\ \\href{{https://linkedin.com/in/{personal['linkedin']}}}{{\\texttt{{{personal['linkedin']}}}}} \\hspace{{1pt}} $|$")
    header.append(f"    \\hspace{{1pt}} \\faGithub\\ \\href{{https://{personal['github']}}}{{\\texttt{{{personal['github']}}}}} \\hspace{{1pt}} $|$")
    header.append(f"    \\hspace{{1pt}} \\faMapMarker\\ {personal['location']}")
    header.append("\\end{center}")
    return "\n".join(header)

def generate_skills(skills):
    sections = []
    
    # Langages de programmation
    if 'langages' in skills:
        langs = [f"\\texttt{{{lang.replace('#', '\\#')}}}" for lang in skills['langages']]
        sections.append(f"\\textbf{{Langages de programmation:}} {', '.join(langs)} \\\\")

    # Data Engineering
    if 'data_engineering' in skills:
        data_eng = [f"\\texttt{{{tool}}}" for tool in skills['data_engineering']]
        sections.append(f"\\textbf{{Data Engineering:}} {', '.join(data_eng)} \\\\")

    # Cloud & Databases
    if 'cloud_databases' in skills:
        cloud_db = [f"\\texttt{{{db}}}" for db in skills['cloud_databases']]
        sections.append(f"\\textbf{{Cloud \\& Databases:}} {', '.join(cloud_db)} \\\\")

    # Machine Learning
    if 'machine_learning' in skills:
        ml = [f"\\texttt{{{tool}}}" for tool in skills['machine_learning']]
        sections.append(f"\\textbf{{Machine Learning:}} {', '.join(ml)} \\\\")

    # DevOps
    if 'devops' in skills:
        devops = [f"\\texttt{{{tool}}}" for tool in skills['devops']]
        sections.append(f"\\textbf{{DevOps:}} {', '.join(devops)} \\\\")

    # Soft Skills
    if 'soft_skills' in skills:
        soft = [f"\\textit{{{skill}}}" for skill in skills['soft_skills']]
        sections.append(f"\\textbf{{Soft Skills:}} {', '.join(soft)} \\\\")

    return '\n'.join(sections)

def generate_languages(languages):
    if not languages:
        return ""
    # Si les langues sont une liste simple de chaînes
    if isinstance(languages[0], str):
        lang_str = ", ".join(languages)
    # Si les langues sont une liste de dictionnaires
    else:
        lang_str = ", ".join([f"{lang['name']} ({lang['level']})" for lang in languages])
    return f"\\textbf{{Langues:}} {lang_str} \\\\"

def generate_education(education):
    sections = []
    for entry in education:
        date = entry.get('date', '')
        degree = clean_text(entry.get('degree', ''))
        school = clean_text(entry.get('school', ''))
        location = clean_text(entry.get('location', ''))
        gpa = clean_text(entry.get('gpa', ''))
        
        sections.append("\\resumeSubheading")
        sections.append("{" + degree + "}{" + date + "}")
        sections.append("{" + school + "}{" + location + "}")
        if gpa:
            sections.append("\\item " + gpa)
        sections.append("")
    return "\n".join(sections)

def generate_experience(experience):
    sections = []
    for entry in experience:
        title = clean_text(entry.get('title', ''))
        company = clean_text(entry.get('company', ''))
        date = entry.get('date', '')
        location = clean_text(entry.get('location', ''))
        
        sections.append("\\resumeSubheading")
        sections.append("{" + title + "}{" + date + "}")
        sections.append("{" + company + "}{" + location + "}")
        
        for detail in entry.get('details', []):
            sections.append("\\item " + clean_text(detail))
        sections.append("")
    return "\n".join(sections)

def generate_projects(projects):
    if not projects:
        return ""
    
    sections = []
    for project in projects:
        title = project.get('title', '')
        description = project.get('description', '')
        sections.append(f"\\item \\textbf{{{title}}} - {clean_text(description)} \\\\")
    
    return '\n'.join(sections)

def generate_cv(template_path, output_path, cv_data):
    with open(template_path, 'r', encoding='utf-8') as file:
        template = file.read()

    personal = cv_data.get('personal', {})
    skills = cv_data.get('skills', {})
    education = cv_data.get('education', [])
    experience = cv_data.get('experience', [])
    projects = cv_data.get('projects', [])

    header = generate_header(personal)
    skills_section = generate_skills(skills)
    languages_section = ""
    if 'langues' in skills:
        languages_section = generate_languages(skills['langues'])
    education_section = generate_education(education)
    experience_section = generate_experience(experience)
    projects_section = generate_projects(projects)

    # Insérer le contenu généré à l'endroit approprié
    content = f"""
{header}

\\vspace{{10pt}}
\\section{{Résumé}}
{clean_text(personal.get('summary', ''))}

\\vspace{{10pt}}
\\section{{Compétences}}
{skills_section}
{languages_section}

\\vspace{{10pt}}
\\section{{Formation}}
\\resumeSubHeadingListStart
{education_section}
\\resumeSubHeadingListEnd

\\vspace{{10pt}}
\\section{{Expérience Professionnelle}}
\\resumeSubHeadingListStart
{experience_section}
\\resumeSubHeadingListEnd

\\vspace{{10pt}}
\\section{{Projets}}
\\resumeItemListStart
{projects_section}
\\resumeItemListEnd
"""

    # Remplacer les variables dans le template
    cv_content = template.replace("{{name}}", personal.get('name', ''))
    cv_content = cv_content.replace("{{title}}", personal.get('title', ''))
    cv_content = cv_content.replace("%==== CONTENU GÉNÉRÉ ICI ====", content)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(cv_content)

def main():
    if len(sys.argv) != 2:
        print("Usage: python generate_cv_all.py <json_file>")
        sys.exit(1)

    json_file = sys.argv[1]
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    # Construire les chemins
    json_path = os.path.join(project_root, 'data', json_file)
    template_path = os.path.join(project_root, 'templates', 'cv_template.tex')
    
    # Créer le nom du fichier de sortie basé sur le nom du fichier JSON
    output_name = Path(json_file).stem.replace('cv_data_', 'cv_')
    output_path = os.path.join(project_root, 'output', f"{output_name}.tex")

    print(f"Génération du CV à partir de : {json_file}")
    print(f"Lecture des données depuis : {json_path}")
    print(f"Utilisation du template : {template_path}")
    print(f"Génération du fichier : {output_path}")

    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Fichier de données non trouvé : {json_path}")
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template non trouvé : {template_path}")

    cv_data = load_cv_data(json_path)
    generate_cv(template_path, output_path, cv_data)
    print(f"CV généré avec succès dans : {output_path}")

if __name__ == "__main__":
    main() 