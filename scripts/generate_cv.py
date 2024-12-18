import os
import re
from typing import Dict, List
import json

class CVGenerator:
    def __init__(self):
        self.template_dir = "templates"
        self.output_dir = "output"
        self.input_dir = "input"
        self.data = self._load_cv_data()

    def _load_cv_data(self) -> Dict:
        """Charge les données du CV depuis un fichier JSON"""
        data_path = os.path.join(self.input_dir, "cv_data.json")
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def parse_job_offer(self, job_file: str) -> Dict[str, List[str]]:
        """Parse une offre d'emploi pour extraire les compétences requises"""
        skills = {
            'technical': [],
            'soft': [],
            'languages': []
        }
        
        with open(job_file, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            
            # Extraction des compétences techniques
            tech_patterns = [
                r'python', r'sql', r'java', r'scala',
                r'spark', r'hadoop', r'kafka',
                r'aws', r'gcp', r'azure',
                r'docker', r'kubernetes', r'airflow'
            ]
            
            for pattern in tech_patterns:
                if re.search(pattern, content):
                    skills['technical'].append(pattern)
                    
        return skills

    def generate_cv(self, job_file: str, output_name: str):
        """Génère un CV personnalisé basé sur une offre d'emploi"""
        required_skills = self.parse_job_offer(job_file)
        
        # Filtrer les sections en fonction des compétences requises
        filtered_data = self._filter_cv_data(required_skills)
        
        # Générer le CV LaTeX
        output_path = os.path.join(self.output_dir, output_name)
        self._generate_latex(filtered_data, output_path)
        
        return output_path

    def _filter_cv_data(self, required_skills: Dict) -> Dict:
        """Filtre les données du CV en fonction des compétences requises"""
        filtered = self.data.copy()
        
        # Filtrer les expériences pertinentes
        filtered['experience'] = [
            exp for exp in self.data['experience']
            if any(skill in exp['technologies'] 
                  for skill in required_skills['technical'])
        ]
        
        return filtered

    def _generate_latex(self, data: Dict, output_path: str):
        """Génère le fichier LaTeX final"""
        # Copier le template principal
        with open(os.path.join(self.template_dir, 'main.tex'), 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Générer chaque section
        sections = {
            'header': self._generate_header(data['personal']),
            'experience': self._generate_experience(data['experience']),
            'education': self._generate_education(data['education']),
            'skills': self._generate_skills(data['skills'])
        }
        
        # Créer les fichiers de section
        for section_name, content in sections.items():
            section_path = os.path.join(self.template_dir, 'sections', f'{section_name}.tex')
            with open(section_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        # Écrire le fichier final
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(template)

    def _generate_header(self, personal: Dict) -> str:
        return f"""
        \\begin{{center}}
            \\textbf{{\\Huge {personal['name']}}} \\\\ \\vspace{{5pt}}
            \\small 
            \\faPhone* \\texttt{{{personal['phone']}}} \\hspace{{1pt}} $|$
            \\faEnvelope \\hspace{{2pt}} \\texttt{{{personal['email']}}} \\hspace{{1pt}} $|$ 
            \\faGithub \\hspace{{2pt}} \\texttt{{{personal['github']}}} \\hspace{{1pt}} $|$
            \\faMapMarker* \\hspace{{2pt}}\\texttt{{{personal['location']}}}
            \\\\ \\vspace{{-3pt}}
        \\end{{center}}
        """

    # Ajouter les autres méthodes de génération (_generate_experience, _generate_education, _generate_skills)

if __name__ == "__main__":
    generator = CVGenerator()
    
    # Pour l'offre OpenAI
    generator.generate_cv(
        "input/jobs/openai_data_engineer.rtf",
        "cv_openai_data_engineer.tex"
    )
    
    # Pour l'offre Lincoln
    generator.generate_cv(
        "input/jobs/lincoln_data_engineer.rtf",
        "cv_lincoln_data_engineer.tex"
    ) 