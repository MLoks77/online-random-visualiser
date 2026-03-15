# Générateur de visualisers aléatoires

Génère une vidéo où les médias d'un dossier sont placés une taille et une position aléatoires, en rythme avec un fichier audio.
Le placement des médias supporte les fichiers images, vidéos, et les gifs.

Je ne suis pas un dev !!! Ce script est surement très mal optimisé, mal écrit et buggé, mais c'est mon premier gros projet python et c'était fun :)

## Exemple de commande à utiliser !

```bash
python visualiser.py -o finalvideo.mp4 -i media -a audiotrack.wav -wi 1920 -he 1080 -imgd 10 -b 0 0 255
```

## Paramètres

La plupart des paramètres incluent une valeur par défaut, il n'y a pas à tous les remplir :
La taille de la vidéo en sortie est un format vertical 9:16 en 1080p.
Les largeurs minimum et maximum des médias sont 150 - 600 px, ça marche bien avec le ratio 9:16
Les images restent 20 secondes avant de disparaître. 
La couleur du fond est blanche, il est aussi possible de le rendre transparent en bricolant le code, MoviePy a une option pour ça mais je l'ai pas encore intégré.

• Nom du fichier vidéo en sortie (un chemin mp4)
```bash
"-o yay.mp4" "--output yay.mp4"
```
 
• Largeur (en pixels) de la vidéo en sortie
```bash
"-wi 1080" "--output-width 1080"
```

• Hauteur (en pixels) de la vidéo en sortie
```bash
"-he 1920" "--output-height 1920"
```

• Fichier audio à utiliser :
```bash
"-a audiotrack.wav" "--audio-file audiotrack.wav"
```

• Dossier de médias à utiliser :
```bash
"-i media" "--input-folder media"
```

• Largeur minimum (en pixels) des médias placés :
```bash
"-imgmin 150" "--min-img-width 150"
```

• Largeur maximum (en pixels) des médias placés :
```bash
"-imgmax 600" "--max-img-width 600"
```

• Temps que les images restent à l'écran :
```bash
"-imgd 20" "--img-duration 20"
```

• Couleur du fond (en format RGB, donc 3 arguments) :
```bash
"-b 255 255 255" "--bg-color 255 255 255"
```

## Installation

```bash
python -m venv .venv
source venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

