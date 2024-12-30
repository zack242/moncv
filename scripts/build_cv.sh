#!/bin/bash

# Vérifier si un argument a été fourni
if [ $# -eq 0 ]; then
    echo "Usage: $0 <type_cv>"
    echo "Types disponibles : engineer, analyst, software, ia, dev, analytics"
    echo "(ajoutez _en ou _eng pour la version anglaise)"
    exit 1
fi

# Obtenir le chemin absolu du répertoire du script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( dirname "$SCRIPT_DIR" )"

# Créer les dossiers nécessaires s'ils n'existent pas
mkdir -p "$PROJECT_ROOT/output"
mkdir -p "$PROJECT_ROOT/mescvs"

# Type de CV
CV_TYPE="$1"
echo "Génération du CV type: $CV_TYPE"

# Générer le CV
python "$SCRIPT_DIR/generate_cv.py" "$CV_TYPE"

if [ $? -eq 0 ]; then
    # Compiler le PDF
    cd "$PROJECT_ROOT/output"
    pdflatex "cv_${CV_TYPE}.tex"
    
    if [ $? -eq 0 ]; then
        # Copier le PDF dans mescvs
        cp "cv_${CV_TYPE}.pdf" "../mescvs/"
        echo "CV $CV_TYPE généré avec succès"
        
        # Nettoyer les fichiers temporaires
        rm -f "cv_${CV_TYPE}.aux" \
             "cv_${CV_TYPE}.log" \
             "cv_${CV_TYPE}.out" \
             "cv_${CV_TYPE}.toc" \
             "cv_${CV_TYPE}.nav" \
             "cv_${CV_TYPE}.snm" \
             "cv_${CV_TYPE}.synctex.gz"
    else
        echo "Erreur lors de la compilation du PDF"
        exit 1
    fi
else
    echo "Erreur lors de la génération du CV"
    exit 1
fi 