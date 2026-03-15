
import argparse
from pathlib import Path
import random
from random import shuffle
import os

from moviepy.editor import *
import PIL
from PIL import Image
PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
import numpy as np
import librosa

import mimetypes

def effects(
    width= int, 
    height= int, 
    output_name= Path, 
    audio_file= Path, 
    media_folder= Path,
    bg_color= str,
    min_width= int,
    max_width= int,
    img_duration= float,
    delta=float,
    ):

    # ----------------- AUDIO = DÉTECTION DES BEATS -----------------

    # Insérer l'audio 2 fois : (c'est crado mais pour l'instant c'est comme ça)
    # - une pour générer la vidéo avec MoviePy (AudioFileClip)
    # - une pour détecter les beats de l'audio avec Librosa

    # ----------------- AUDIO = BEAT DETECTION -----------------

    # Inserting 2 times the audio (so dirty, I know)
    # - once to generate the video with MoviePy (AudioFileClip)
    # - twice to detect beats from the audio with Librosa
    clip_audio = AudioFileClip(str(audio_file))
    y, sr = librosa.load(audio_file, sr=None)

    # Détecter les pics dans le spectre audio
    # Detect peaks in audio waveform
    def detect_onsets(y: np.ndarray, sr: int) -> np.ndarray:
        """Return an array of onset times (in seconds) detected in the audio file."""
        return librosa.onset.onset_detect(y=y,
                                sr=sr, units='time', 
                                hop_length=512, 
                                backtrack=True, # Backtrack to the nearest peak for better sync
                                pre_max=5,
                                post_max=5,
                                pre_avg=10,
                                post_avg=10,
                                delta=delta,
                                wait=10) # Small wait to avoid double-triggers on the same hit

    # Calculer le tempo juste pour le fun
    # Calculate tempo for fun
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    np.set_printoptions(precision=1)
    print("BPM :", tempo)

    onset_times = detect_onsets(y, sr)
    print(onset_times)
    print("Beats detected :", len(onset_times))


    # ----------------- TRAITEMENT VIDEO/IMAGE -----------------
    # ----------------- VIDEO/IMAGE PROCESSING -----------------

    # Stocker les fichiers du dossier
    # Store the files from folder
    print("Indexing media...")
    clips = []  

    IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".heic", ".heif"}
    VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".gif"}

    media_paths = []
    for filename in os.listdir(media_folder):
        path = os.path.join(media_folder, filename)
        ext = Path(filename).suffix.lower()
        if ext in IMAGE_EXTENSIONS or ext in VIDEO_EXTENSIONS:
            media_paths.append(path)

    if not media_paths:
        raise ValueError(
            f"No valid media found in folder: {media_folder}\n"
            f"Supported images: {IMAGE_EXTENSIONS}\n"
            f"Supported videos: {VIDEO_EXTENSIONS}"
        )

    print("Loading selected media...")
    for path in media_paths:
        filename = Path(path).name
        ext = Path(path).suffix.lower()

        try:
            if ext in IMAGE_EXTENSIONS:
                img = Image.open(path).convert("RGB")
                clip = ImageClip(np.array(img)).set_duration(img_duration)
                clips.append(clip)

            elif ext in VIDEO_EXTENSIONS:
                clip = VideoFileClip(path)
                clips.append(clip)

        except Exception as e:
            print(f"Error loading {filename}: {e}")

    if not clips:
        raise ValueError("No media could be loaded successfully from selected files.")

    print(f"{len(clips)} media loaded")
    random.shuffle(clips)


    # TAILLE & POSITION RANDOM
    # RANDOM SIZE & POSITION
    processed_clips = []

    for clip in clips:
        new_width = random.randint(min_width, max_width)
        w, h = clip.size
        new_height = int((new_width / w) * h)

        clip = clip.resize((new_width, new_height))

        x = random.randint(0, width - new_width)
        y = random.randint(0, height - new_height)

        clip = clip.set_position((x, y))
        processed_clips.append(clip)



    # APPARITION SYNCHRO SUR BEAT
    # SPAWNING SYNCED ON BEAT
    clips_timed = []

    # ON BOUCLE SUR TOUT LES BEATS
    # SI PAS ASSEZ D'IMAGES, ON RECOMMENCE
    for i, beat in enumerate(onset_times):
        original_clip = processed_clips[i % len(processed_clips)]
        clips_timed.append(original_clip.set_start(beat))

    print(f"{len(clips_timed)} clips synchronisés sur {len(onset_times)} beats")



    # ENCODAGE
    # ENCODING
    final_clip = CompositeVideoClip(clips_timed, size=(width, height), bg_color=bg_color)

    final_clip = final_clip.set_duration(clip_audio.duration)

    final_clip.audio = clip_audio

    final_clip.write_videofile(
        str(output_name), 
        codec="libx264",
        audio_codec="aac",
        fps=24,
        threads=max(1, (os.cpu_count() or 4) - 1),
        audio=True,
        ffmpeg_params=["-preset", "veryfast"],)

    final_clip.close()
    clip_audio.close()
    for c in clips_timed:
        try:
            c.close()
        except:
            pass



# ----------------- ARGUMENTS DANS LE CMD -----------------
# ----------------- CLI ARGUMENTS -----------------

def _parse_args():
    p = argparse.ArgumentParser(description="Vidéos placées aléatoirement synchros avec un fichier audio")

    p.add_argument("-o", "--output", type=Path, default=Path("randomvids.mp4"), help="Nom du fichier vidéo output")
    p.add_argument("-wi", "--output-width", type=int, default=1080, help="Largeur du fichier vidéo en pixels")
    p.add_argument("-he", "--output-height", type=int, default=1920, help="Hauteur du fichier vidéo en pixels")
    
    p.add_argument("-a", "--audio-file", type=Path, help="Fichier audio à utiliser")
    p.add_argument("-i", "--input-folder", type=Path, default=Path("media"), help="Dossier de médias à utiliser")

    p.add_argument("-imgmin", "--min-img-width", type=int, default=150, help="Taille minimum des médias en pixels")
    p.add_argument("-imgmax","--max-img-width", type=int, default=600, help="Taille maximum des médias en pixels")

    p.add_argument("-imgd", "--img-duration", type=float, default=20, help="Durée des images en secondes")

    p.add_argument("-b", "--bg-color", nargs=3, type=int, default=[255, 255, 255], help="Couleur du fond pour la vidéo")

    p.add_argument("-d", "--delta", type=float, default=0.17, help="Seuil de détection des pics audio (0.1 pour un seuil bas et une détection large, jusqu'à 1 pour une détection plus sélective)")

    return p.parse_args()

def main():
    args = _parse_args()

    effects(
        width=args.output_width, 
        height=args.output_height, 
        output_name=args.output, 
        audio_file=args.audio_file, 
        media_folder=args.input_folder,
        bg_color=args.bg_color,
        min_width=args.min_img_width,
        max_width=args.max_img_width,
        img_duration=args.img_duration,
        delta=args.delta,
    )

if __name__ == "__main__":
    main()
