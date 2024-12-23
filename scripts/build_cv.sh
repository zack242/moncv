#!/bin/bash

# Liste des types de CV disponibles
CV_TYPES=("engineer" "analyst" "software")

# Obtenir le chemin absolu du répertoire du script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( dirname "$SCRIPT_DIR" )"

# Fonction pour compiler un CV
compile_cv() {
    local cv_type=$1
    echo "Génération du CV type: $cv_type"
    
    # Générer le fichier .tex en utilisant le chemin absolu
    python "$SCRIPT_DIR/generate_cv.py" "$cv_type"
    
    if [ $? -ne 0 ]; then
        echo "Erreur lors de la génération du fichier .tex pour le CV $cv_type"
        return 1
    fi
    
    # Compiler le fichier .tex en PDF
    cd "$PROJECT_ROOT/output"
    pdflatex "cv_${cv_type}.tex"
    
    if [ $? -ne 0 ]; then
        echo "Erreur lors de la compilation du PDF pour le CV $cv_type"
        cd "$PROJECT_ROOT"
        return 1
    fi
    
    # Nettoyer les fichiers intermédiaires
    rm -f "cv_${cv_type}.aux" "cv_${cv_type}.log"
    cd "$PROJECT_ROOT"
    
    echo "CV $cv_type généré avec succès"
}

# Si un argument est fourni, compiler uniquement ce type de CV
if [ $# -eq 1 ]; then
    if [[ " ${CV_TYPES[@]} " =~ " $1 " ]]; then
        compile_cv "$1"
    else
        echo "Type de CV invalide. Options disponibles : ${CV_TYPES[*]}"
        exit 1
    fi
else
    # Compiler tous les types de CV
    for cv_type in "${CV_TYPES[@]}"; do
        compile_cv "$cv_type"
    done
fi 