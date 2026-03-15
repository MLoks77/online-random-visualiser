# 🎬 Online Random Visualiser

Ce projet permet de transformer un fichier audio en une expérience visuelle dynamique. Il utilise l'analyse de rythme (beat detection) pour faire apparaître des médias (images/vidéos) de manière aléatoire en synchronisation avec la musique.

# PROJET POSSIBLE GRACE A :
```bash
https://codeberg.org/Lelio/random-visualiser-generator
```

## Installation

1. **Prérequis** :
   - Python 3.10+
   - FFmpeg (nécessaire pour MoviePy)

2. **Installation des dépendances** :
   ```bash
   pip install -r python/requirements.txt
   pip install flask flask-cors
   ```

## Utilisation

1. **Lancer le serveur Backend** :
   ```bash
   python app.py
   ```

2. **Lancer l'interface Frontend** :
   Ouvre le fichier `index.html`

3. **Générer une vidéo** :
   - Sélectionne un fichier audio.
   - Sélectionne plusieurs images ou vidéos.
   - Ajuste la **Sensibilité Beats** (Delta) : plus elle est basse, plus il y aura d'images.
   - Clique sur **Générer**. La vidéo apparaîtra une fois le rendu terminé.

## 📂 Structure du projet
- `app.py` : Serveur Flask (pont entre le Web et Python).
- `index.html` / `main.js` : Interface utilisateur et logique frontend.
- `python/visualiser.py` : Cœur algorithmique de traitement vidéo.
- `temp_uploads/` : Stockage temporaire des fichiers envoyés par l'utilisateur.
- `outputs/` : Dossier contenant les vidéos générées.
