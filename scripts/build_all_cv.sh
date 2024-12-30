#!/bin/bash

echo "Génération de tous les CV..."

echo "1. CV Engineer (FR)"
./scripts/build_cv.sh engineer

echo "2. CV Engineer (EN)"
./scripts/build_cv.sh engineer_en

echo "3. CV Analyst"
./scripts/build_cv.sh analyst

echo "4. CV Software"
./scripts/build_cv.sh software

echo "5. CV IA (FR)"
./scripts/build_cv.sh ia

echo "6. CV IA (EN)"
./scripts/build_cv.sh ia_eng

echo "7. CV Dev (FR)"
./scripts/build_cv.sh dev

echo "8. CV Dev (EN)"
./scripts/build_cv.sh dev_eng

echo "9. CV Analytics (FR)"
./scripts/build_cv.sh analytics

echo "10. CV Analytics (EN)"
./scripts/build_cv.sh analytics_eng

echo "Génération terminée !" 