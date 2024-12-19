import json
import os

def load_cv_data(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def clean_text(text):
    """Nettoie le texte pour LaTeX"""
    # Traitement spécial pour "Top X%"
    if "%" in text and "Top" in text:
        text = text.replace("%", "\\%")
        return text
    
    # Remplacer d'abord les apostrophes par un espace
    text = text.replace("'", " ")
    text = text.replace("'", " ")
    
    # Remplacer les caractères spéciaux par leur version LaTeX
    replacements = {
        '&': ' et ',
        '%': '\\%',
        '$': '\\$',
        '#': '\\#',
        '_': '\\textunderscore{}',
        '{': '\\{',
        '}': '\\}',
        '~': '\\textasciitilde{}',
        '^': '\\textasciicircum{}',
        '\\': '\\textbackslash{}',
        '"': "''",
        '–': '--',
        '—': '---',
        '…': '...',
        '/': ' ',
        '(': '',
        ')': '',
        '@': 'at'
    }
    
    # Traitement spécial pour "C#"
    text = text.replace('C#', 'C\\#')
    
    for old, new in replacements.items():
        if old != '#':  # Skip le # car on l'a déjà traité pour C#
            text = text.replace(old, new)
    
    # Nettoyer les caractères accentués
    accents = {
        'é': '\\\'{e}',
        'è': '\\`{e}',
        'à': '\\`{a}',
        'ù': '\\`{u}',
        'ê': '\\^{e}',
        'â': '\\^{a}',
        'î': '\\^{i}',
        'ô': '\\^{o}',
        'û': '\\^{u}',
        'ë': '\\"{e}',
        'ï': '\\"{i}',
        'ü': '\\"{u}',
        'ç': '\\c{c}',
        'É': '\\\'{E}',
        'È': '\\`{E}',
        'À': '\\`{A}',
        'Ê': '\\^{E}',
        'Î': '\\^{I}',
        'Ô': '\\^{O}',
        'Û': '\\^{U}',
        'Ë': '\\"{E}',
        'Ï': '\\"{I}',
        'Ü': '\\"{U}',
        'Ç': '\\c{C}'
    }
    
    for old, new in accents.items():
        text = text.replace(old, new)
    
    return text

def generate_header(personal):
    header = []
    header.append("\\begin{center}")
    header.append(f"    \\textbf{{\\Huge {personal['name']}}} \\\\ \\vspace{{3pt}}")
    header.append(f"    \\Large Data Engineer \\\\ \\vspace{{5pt}}")
    header.append(f"    \\small \\faPhone\\ \\texttt{{{personal['phone']}}} \\hspace{{1pt}} $|$")
    header.append(f"    \\hspace{{1pt}} \\faEnvelope\\ \\texttt{{{personal['email']}}} \\hspace{{1pt}} $|$")
    header.append(f"    \\hspace{{1pt}} \\faLinkedin\\ \\texttt{{{personal['linkedin']}}} \\hspace{{1pt}} $|$")
    header.append(f"    \\hspace{{1pt}} \\texttt{{{personal['contract']}}} \\hspace{{1pt}} $|$")
    header.append(f"    \\hspace{{1pt}} \\faMapMarker\\ \\texttt{{{personal['location']}}}")
    header.append("    \\\\ \\vspace{10pt}")
    header.append("\\end{center}")
    return "\n".join(header)

def generate_profile(personal):
    profile_str = []
    profile_str.append("\\begin{itemize}[leftmargin=0in, label={}]")
    profile_str.append("\\small{\\item{")
    profile_str.append(clean_text(personal['summary']))
    profile_str.append("}}")
    profile_str.append("\\end{itemize}")
    return "\n".join(profile_str)

def generate_experience(experience):
    experience_str = []
    experience_str.append("\\section{EXPERIENCE}")
    experience_str.append("\\resumeSubHeadingListStart")
    
    for exp in experience:
        # Nettoyer les données
        company = clean_text(exp['company'])
        position = clean_text(exp['position'])
        location = clean_text(exp['location'])
        dates = clean_text(exp['dates'])
        
        # Construire l'entrée
        experience_str.append("    \\resumeSubheading")
        experience_str.append(f"      {{{company}}}{{{dates}}}")
        experience_str.append(f"      {{{position}}}{{{location}}}")
        experience_str.append("      \\resumeItemListStart")
        
        for highlight in exp['highlights']:
            highlight = clean_text(highlight)
            experience_str.append(f"        \\resumeItem{{{highlight}}}")
        
        experience_str.append("      \\resumeItemListEnd")
    
    experience_str.append("  \\resumeSubHeadingListEnd")
    return "\n".join(experience_str)

def generate_projects(projects):
    projects_str = []
    projects_str.append("\\section{PROJECTS}")
    projects_str.append("\\resumeSubHeadingListStart")
    
    for project in projects:
        projects_str.append("      \\resumeProjectHeading")
        projects_str.append(f"          {{\\textbf{{{project['name']}}} \\small{{({project['technologies']})}}}} {{}}")
        projects_str.append("          \\resumeItemListStart")
        
        for highlight in project['highlights']:
            projects_str.append(f"            \\resumeItem{{{highlight}}}")
        
        projects_str.append("          \\resumeItemListEnd")
    
    projects_str.append("    \\resumeSubHeadingListEnd")
    return "\n".join(projects_str)

def generate_education(education):
    education_str = []
    education_str.append("\\section{EDUCATION}")
    education_str.append("\\resumeSubHeadingListStart")
    
    for edu in education:
        # Ajouter l'en-tête
        education_str.append("    \\resumeSubheading")
        education_str.append(f"      {{{edu['school']}}}{{{edu['date']}}}")
        education_str.append(f"      {{{edu['degree']}}}{{{edu['location']}}}")
        
        # Ajouter les highlights
        if edu.get('highlights'):
            education_str.append("      \\resumeItemListStart")
            for highlight in edu['highlights']:
                # Traiter chaque highlight séparément
                cleaned_highlight = clean_text(highlight)
                # S'assurer que le highlight est bien formaté
                education_str.append(f"        \\resumeItem{{{cleaned_highlight}}}")
            education_str.append("      \\resumeItemListEnd")
    
    education_str.append("  \\resumeSubHeadingListEnd")
    return "\n".join(education_str)

def generate_skills(skills):
    skills_str = []
    skills_str.append("\\section{COMPETENCES}")
    skills_str.append("\\begin{itemize}[leftmargin=0in, label={}]")
    skills_str.append("\\small{\\item{")
    
    skill_lines = []
    for category, items in skills.items():
        category_name = category.replace('_', ' ').title()
        # Nettoyer chaque compétence individuellement
        cleaned_items = [clean_text(item) for item in items]
        skill_line = f"     \\textbf{{{category_name}}} {{: {', '.join(cleaned_items)}}}"
        skill_lines.append(skill_line)
    
    skills_str.append("\\vspace{2pt} \\\\\n".join(skill_lines))
    skills_str.append("}}")
    skills_str.append("\\end{itemize}")
    return "\n".join(skills_str)

def generate_cv(template_path, output_path, cv_data):
    # Créer le dossier output s'il n'existe pas
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Read the template
    with open(template_path, 'r', encoding='utf-8') as file:
        template = file.read()

    # Generate each section
    header = generate_header(cv_data['personal'])
    profile = generate_profile(cv_data['personal'])
    skills = generate_skills(cv_data['skills'])
    experience = generate_experience(cv_data['experience'])
    projects = generate_projects(cv_data['projects'])
    education = generate_education(cv_data['education'])

    # Find the marker for where to insert the content
    content_start = template.find("\\begin{document}") + len("\\begin{document}")
    content_end = template.find("\\end{document}")

    # Combine all parts
    final_cv = (
        template[:content_start] + "\n\n" +
        header + "\n\n" +
        profile + "\n\n" +
        skills + "\n\n" +
        experience + "\n\n" +
        projects + "\n\n" +
        education + "\n\n" +
        template[content_end:]
    )

    # Write the output
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(final_cv)

def main():
    # Define paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, '..', 'data', 'cv_data.json')
    template_path = os.path.join(current_dir, '..', 'templates', 'cv_template.tex')
    output_path = os.path.join(current_dir, '..', 'output', 'cv.tex')

    # Load CV data
    cv_data = load_cv_data(json_path)
    
    # Generate CV
    generate_cv(template_path, output_path, cv_data)

if __name__ == "__main__":
    main()