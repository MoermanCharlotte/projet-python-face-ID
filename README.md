# 🍽️ Reconnaissance Faciale - Restaurant Scolaire

## Description Simple

Application très simple pour reconnaître les étudiants par leur visage et créditer des repas.

## Installation

```bash
pip install -r requirements.txt
python main.py
```

## Utilisation

### Mode Administrateur
1. Cliquez sur "ADMINISTRATEUR"
2. Entrez le nom d'un étudiant
3. Cliquez "AJOUTER" → Capturez 10 photos (SPACE = photo, ESC = arrêter)
4. Vous pouvez aussi "LISTER" ou "SUPPRIMER" des personnes

### Mode Identification
1. Cliquez sur "M'IDENTIFIER"
2. Regardez la webcam
3. Si reconnu → Message de bienvenue + crédit repas
4. ESC pour arrêter

## Structure des dossiers

```
data/
  ├── Jean/
  │   ├── photo_0.jpg
  │   ├── photo_1.jpg
  │   └── ... (10 photos)
  └── Marie/
      ├── photo_0.jpg
      └── ...
```

## Code Commenté

**Chaque ligne du code est expliquée en français pour que tu puisses comprendre et l'expliquer.**

- Importer les bibliothèques
- Créer l'interface
- Capturer les photos
- Reconnaître les visages
- Créditer les repas

## Notes

- Photos sauvegardées en niveaux de gris (plus rapide)
- Détection avec Haar Cascade (rapide et fiable)
- Reconnaissance avec LBPH (simple et efficace)
- Aucune librairie complexe

**Tout est SUPER simple !** 📚
