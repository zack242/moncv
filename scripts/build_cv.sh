#!/bin/bash

# Créer le dossier output s'il n'existe pas
mkdir -p output

# Générer le fichier .tex
python scripts/generate_cv.py

# Aller dans le dossier output
cd output

# Compiler le PDF
pdflatex cv.tex

# Nettoyer les fichiers temporaires
rm -f *.aux *.log *.out

echo "CV généré avec succès dans output/cv.pdf" 