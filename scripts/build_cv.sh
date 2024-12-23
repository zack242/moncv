#!/bin/bash

# Générer le fichier .tex
python3 scripts/generate_cv.py

# Vérifier si le fichier .tex a été généré
if [ ! -f output/cv.tex ]; then
    echo "Erreur : Le fichier cv.tex n'a pas été généré"
    exit 1
fi

# Copier les images dans le dossier output
mkdir -p output/images
cp images/* output/images/

# Compiler le PDF
cd output
pdflatex cv.tex
pdflatex cv.tex  # Deuxième passage pour les références
cd ..

# Vérifier si le PDF a été généré
if [ ! -f output/cv.pdf ]; then
    echo "Erreur : La compilation du PDF a échoué"
    exit 1
fi

echo "CV généré avec succès !" 