import os
import uuid
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from python.visualiser import effects
from pathlib import Path
import shutil

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'temp_uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/process', methods=['POST'])
def process_video():
    try:
        # parametres
        width = int(request.form.get('width', 1080))
        height = int(request.form.get('height', 1920))
        delta = float(request.form.get('delta', 0.17))
        img_duration = float(request.form.get('img_duration', 1.0))
        
        # audio
        if 'audio' not in request.files:
            return jsonify({'error': 'Fichier audio manquant'}), 400
        
        audio_file = request.files['audio']
        job_id = str(uuid.uuid4())
        job_dir = os.path.join(UPLOAD_FOLDER, job_id)
        media_dir = os.path.join(job_dir, 'media')
        os.makedirs(media_dir, exist_ok=True)
        
        audio_path = os.path.join(job_dir, audio_file.filename)
        audio_file.save(audio_path)
        
        # media
        media_files = request.files.getlist('media')
        use_picsum = request.form.get('use_picsum') == 'true'
        picsum_count = int(request.form.get('picsum_count', 10))

        if not media_files and not use_picsum:
            return jsonify({'error': 'Aucun fichier média fourni'}), 400
            
        for f in media_files:
            if f.filename:
                f.save(os.path.join(media_dir, f.filename))

        if use_picsum:
            print(f"Téléchargement de {picsum_count} images Picsum...")
            for i in range(picsum_count):
                try:
                    response = requests.get(f"https://picsum.photos/1080/1920?random={i}", timeout=5)
                    if response.status_code == 200:
                        with open(os.path.join(media_dir, f"picsum_{i}.jpg"), 'wb') as f:
                            f.write(response.content)
                except Exception as e:
                    print(f"Erreur téléchargement Picsum {i}: {e}")
        
        # execution
        output_filename = f"result_{job_id}.mp4"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        
        print(f"Démarrage du rendu pour {job_id}...")
        
        effects(
            width=width,
            height=height,
            output_name=Path(output_path),
            audio_file=Path(audio_path),
            media_folder=Path(media_dir),
            bg_color=[0, 0, 0],
            min_width=150,
            max_width=width // 2,
            img_duration=img_duration,
            delta=delta
        )
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'video_url': f'/download/{output_filename}'
        })
        
    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
