#!/bin/bash

# Obtenir le chemin absolu du répertoire du script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( dirname "$SCRIPT_DIR" )"

# Créer le dossier mescvs s'il n'existe pas
mkdir -p "$PROJECT_ROOT/mescvs"

# Fonction pour nettoyer les fichiers temporaires
clean_temp_files() {
    local tex_file=$1
    local base_name=$(basename "$tex_file" .tex)
    cd "$PROJECT_ROOT/output"
    rm -f "${base_name}.aux" \
          "${base_name}.log" \
          "${base_name}.out" \
          "${base_name}.toc" \
          "${base_name}.nav" \
          "${base_name}.snm" \
          "${base_name}.synctex.gz" \
          "${base_name}.fls" \
          "${base_name}.fdb_latexmk"
    cd "$PROJECT_ROOT"
}

# Pour chaque fichier JSON dans le dossier data
for json_file in "$PROJECT_ROOT/data"/cv_data_*.json; do
    # Extraire le nom de base du fichier
    base_name=$(basename "$json_file")
    
    echo "Traitement de $base_name"
    
    # Générer le fichier TEX
    python "$SCRIPT_DIR/generate_cv_all.py" "$base_name"
    
    if [ $? -eq 0 ]; then
        # Obtenir le nom du fichier TEX généré
        tex_file="output/$(basename "$base_name" .json).tex"
        tex_file=${tex_file/cv_data_/cv_}
        
        # Compiler le fichier TEX en PDF
        cd "$PROJECT_ROOT/output"
        pdflatex "$(basename "$tex_file")"
        
        if [ $? -eq 0 ]; then
            # Copier le PDF dans le dossier mescvs
            pdf_file="${tex_file%.tex}.pdf"
            cp "$(basename "$pdf_file")" "$PROJECT_ROOT/mescvs/"
            echo "CV généré avec succès : $pdf_file"
            
            # Nettoyer les fichiers temporaires
            clean_temp_files "$(basename "$tex_file")"
        else
            echo "Erreur lors de la compilation du PDF pour $tex_file"
        fi
        
        cd "$PROJECT_ROOT"
    else
        echo "Erreur lors de la génération du TEX pour $json_file"
    fi
done

echo "Tous les CVs ont été générés dans le dossier mescvs/" 