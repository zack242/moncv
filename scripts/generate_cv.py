import json
import os
import sys

def load_cv_data(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def clean_text(text):
    """Nettoie le texte pour LaTeX"""
    if isinstance(text, (list, dict)):
        return text
    
    text = str(text)
    
    replacements = {
        '\\': '$\\backslash$',
        '%': '\\%',
        '_': '\\_',
        '&': '\\&',
        '$': '\\$',
        '#': '\\#',
        '{': '\\{',
        '}': '\\}',
        '~': '\\textasciitilde{}',
        '^': '\\textasciicircum{}',
        '|': '\\textbar{}'
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text

def generate_header(personal):
    header = []
    header.append("\\begin{center}")
    header.append(f"    \\small \\faPhone\\ \\texttt{{{personal['phone']}}} \\hspace{{1pt}} $|$")
    header.append(f"    \\hspace{{1pt}} \\faEnvelope\\ \\texttt{{{personal['email']}}} \\hspace{{1pt}} $|$")
    header.append(f"    \\hspace{{1pt}} \\faLinkedin\\ \\texttt{{{personal['linkedin']}}} \\hspace{{1pt}} $|$")
    header.append(f"    \\hspace{{1pt}} \\faMapMarker\\ \\texttt{{{personal['location']}}} \\hspace{{1pt}} $|$")
    header.append(f"    \\hspace{{1pt}} \\faGithub\\ \\texttt{{{personal['github']}}} \\\\ \\vspace{{0pt}}")
    header.append("\\end{center}")
    return "\n".join(header)

def generate_summary(personal):
    return f"""\\begin{{itemize}}[leftmargin=0in, label={{}}]
\\footnotesize{{\\item{{
{clean_text(personal['summary'])}
}}}}
\\end{{itemize}}"""

def generate_skills(skills):
    skills_str = []
    skills_str.append("\\begin{itemize}[leftmargin=0in, label={}]")
    skills_str.append("\\footnotesize{\\item{")
    
    # Liste pour stocker toutes les lignes de compétences
    skill_lines = []
    
    for category, items in skills.items():
        category_name = category.replace('_', ' ').title()
        # Traduction spéciale pour "programmation"
        if category_name == "Programmation":
            category_name = "Programmation"
        
        # Regrouper Data Engineering et Cloud Databases
        if category_name in ["Data Engineering", "Cloud Databases"]:
            continue
        
        # Nettoyer chaque compétence individuellement
        cleaned_items = []
        for item in items:
            if item == "C#":
                cleaned_items.append("C{\\#}")
            else:
                cleaned_items.append(clean_text(item))
        
        skill_line = f"{{\\footnotesize\\textbf{{{category_name}}}:}} {{\\footnotesize {', '.join(cleaned_items)}}}"
        skill_lines.append(skill_line)
    
    # Ajouter la nouvelle catégorie regroupée
    data_items = []
    if 'data_engineering' in skills:
        data_items.extend(skills['data_engineering'])
    if 'cloud_databases' in skills:
        data_items.extend(skills['cloud_databases'])
    
    if data_items:
        data_items = [clean_text(item) for item in data_items]
        skill_line = f"{{\\footnotesize\\textbf{{Data \\& Cloud Engineering}}:}} {{\\footnotesize {', '.join(data_items)}}}"
        skill_lines.append(skill_line)
    
    # Joindre toutes les lignes avec \\ et \vspace
    skills_content = " \\\\\n\\vspace{3pt}\n".join(skill_lines)
    
    # Ajouter le contenu à skills_str
    skills_str.append(skills_content)
    
    # Fermer les accolades correctement
    skills_str.append("}")  # Ferme \item{
    skills_str.append("}")  # Ferme \footnotesize{
    skills_str.append("\\end{itemize}")
    
    return "\n".join(skills_str)

def generate_education(education):
    edu_str = []
    edu_str.append("\\resumeSubHeadingListStart")
    
    for edu in education:
        # Nettoyer toutes les données avant de les utiliser
        school = clean_text(edu['school'])
        degree = clean_text(edu['degree'])
        date = clean_text(edu['date'])
        distinction = clean_text(edu['distinction'])
        specialization = clean_text(edu['specialization'])
        
        # Construire la structure correctement
        edu_str.append("    \\resumeSubheading")
        edu_str.append(f"      {{{school}}}")
        edu_str.append(f"      {{{date}}}")
        edu_str.append(f"      {{{degree}}}")
        edu_str.append(f"      {{{distinction}}}")
        
        # Ajouter la spécialisation comme un item séparé
        edu_str.append("      \\resumeItemListStart")
        edu_str.append(f"        \\resumeItem{{{specialization}}}")
        edu_str.append("      \\resumeItemListEnd")
    
    edu_str.append("  \\resumeSubHeadingListEnd")
    return "\n".join(edu_str)

def generate_experience(experience):
    exp_str = []
    exp_str.append("\\resumeSubHeadingListStart")
    
    for exp in experience:
        exp_str.append("    \\resumeSubheading")
        exp_str.append(f"      {{{clean_text(exp['company'])}}}{{{clean_text(exp['dates'])}}}")
        exp_str.append(f"      {{{clean_text(exp['position'])}}}{{{clean_text('Paris')}}}") # Ajout de la ville
        exp_str.append("      \\resumeItemListStart")
        
        for highlight in exp['highlights']:
            exp_str.append(f"        \\resumeItem{{{clean_text(highlight)}}}")
        
        exp_str.append("      \\resumeItemListEnd")
    
    exp_str.append("  \\resumeSubHeadingListEnd")
    return "\n".join(exp_str)

def generate_projects(projects):
    proj_str = []
    proj_str.append("\\resumeSubHeadingListStart")
    
    for project in projects:
        proj_str.append("    \\resumeProjectHeading")
        proj_str.append(f"      {{{clean_text(project['name'])}}} {{{clean_text(project['date'])}}}")
        proj_str.append("      \\resumeItemListStart")
        
        for highlight in project['highlights']:
            proj_str.append(f"        \\resumeItem{{{clean_text(highlight)}}}")
        
        proj_str.append("      \\resumeItemListEnd")
    
    proj_str.append("\\resumeSubHeadingListEnd")
    return "\n".join(proj_str)

def generate_cv(template_path, output_path, cv_data):
    with open(template_path, 'r', encoding='utf-8') as file:
        template = file.read()

    # Déterminer la langue du CV basée sur le nom du fichier
    is_english = output_path.endswith('_en.tex')
    
    # Définir les titres des sections selon la langue
    section_titles = {
        'skills': 'SKILLS' if is_english else 'COMPETENCES',
        'education': 'EDUCATION' if is_english else 'FORMATIONS',
        'experience': 'EXPERIENCE' if is_english else 'EXPERIENCES',
        'projects': 'PROJECTS' if is_english else 'PROJETS'
    }

    # Remplacer les variables dans le template
    template = template.replace("{{name}}", cv_data['personal']['name'])
    template = template.replace("{{title}}", cv_data['personal']['title'])

    # Générer chaque section
    header = generate_header(cv_data['personal'])
    summary = generate_summary(cv_data['personal'])
    skills = generate_skills(cv_data['skills'])
    education = generate_education(cv_data['education'])
    experience = generate_experience(cv_data['experience'])
    projects = generate_projects(cv_data['projects'])

    # Remplacer le marqueur de contenu avec les sections et leurs titres traduits
    content = f"""
{header}

{summary}

\\section{{{section_titles['skills']}}}
{skills}

\\section{{{section_titles['education']}}}
{education}

\\section{{{section_titles['experience']}}}
{experience}

\\section{{{section_titles['projects']}}}
{projects}
"""

    # Insérer le contenu dans le template
    final_cv = template.replace("%==== CONTENU GÉNÉRÉ ICI ====", content)

    # Créer le dossier output s'il n'existe pas
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Écrire le fichier final
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(final_cv)

def main():
    # Récupérer l'argument de ligne de commande pour le type de CV
    if len(sys.argv) > 1:
        cv_type = sys.argv[1]
    else:
        cv_type = "engineer"  # valeur par défaut

    # Obtenir le chemin du répertoire courant
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Détecter si c'est une version anglaise et extraire le type de base
    is_english = False
    base_type = cv_type
    if cv_type.endswith('_en'):
        is_english = True
        base_type = cv_type[:-3]
    elif cv_type.endswith('_eng'):
        is_english = True
        base_type = cv_type[:-4]

    # Mapping des types de CV vers les noms de fichiers
    cv_types = {
        "engineer": "cv_data_engineer{}.json",
        "analyst": "cv_data_analyst{}.json",
        "software": "cv_data_software{}.json",
        "ia": "cv_data_science_ia{}.json" if is_english else "cv_data_ia{}.json",
        "dev": "cv_data_dev{}.json",
        "analytics": "cv_data_analytics{}.json",
        "consultant": "cv_data_consultant{}.json",
        "ml": "cv_data_ml{}.json",
        "ds": "cv_data_ds{}.json"
    }

    # Vérifier si le type de base de CV est valide
    if base_type not in cv_types:
        print(f"Type de CV invalide. Options disponibles : {', '.join(cv_types.keys())} (ajoutez _en ou _eng pour la version anglaise)")
        sys.exit(1)

    # Ajouter le suffixe _en ou _eng selon le fichier
    suffix = ""
    if is_english:
        # Vérifier d'abord si le fichier _eng existe, sinon utiliser _en
        if os.path.exists(os.path.join(current_dir, '..', 'data', cv_types[base_type].format('_eng'))):
            suffix = "_eng"
        else:
            suffix = "_en"
    json_filename = cv_types[base_type].format(suffix)

    json_path = os.path.join(current_dir, '..', 'data', json_filename)
    template_path = os.path.join(current_dir, '..', 'templates', 'cv_template.tex')
    output_path = os.path.join(current_dir, '..', 'output', f'cv_{cv_type}.tex')

    print(f"Génération du CV type: {cv_type}")
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