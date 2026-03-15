// lien vers l'api : https://publicapi.dev/lorem-picsum-api

const form = document.getElementById('vis-form');
const statusDiv = document.getElementById('status');
const statusText = document.getElementById('status-text');
const resultDiv = document.getElementById('result');
const preview = document.getElementById('video-preview');
const downloadLink = document.getElementById('download-link');
const submitBtn = document.getElementById('submit-btn');
const picsumCheckbox = document.getElementById('use-picsum');
const picsumConfig = document.getElementById('picsum-config');
const picsumCount = document.getElementById('picsum-count');

picsumCheckbox.addEventListener('change', (e) => {
    picsumConfig.classList.toggle('hidden', !e.target.checked);
});

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const audioFile = document.getElementById('audio').files[0];
    const mediaFiles = document.getElementById('media').files;
    const usePicsum = picsumCheckbox.checked;

    if (!audioFile || (mediaFiles.length === 0 && !usePicsum)) {
        alert('Veuillez sélectionner un fichier audio et au moins un média (ou utiliser des images stocks).');
        return;
    }

    statusDiv.classList.remove('hidden');
    resultDiv.classList.add('hidden');
    submitBtn.disabled = true;
    statusText.textContent = "Génération en cours...";

    const formData = new FormData();
    formData.append('audio', audioFile);

    // Valeurs par défaut optimisées pour le rythme
    formData.append('delta', '0.07'); // Très sensible pour capter tous les beats
    formData.append('img_duration', '2.5'); // Durée équilibrée pour l'empilement

    formData.append('use_picsum', usePicsum);
    formData.append('picsum_count', picsumCount.value);

    for (let i = 0; i < mediaFiles.length; i++) {
        formData.append('media', mediaFiles[i]);
    }

    try {
        const response = await fetch('http://localhost:5000/process', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            const videoUrl = `http://localhost:5000${data.video_url}`;
            preview.src = videoUrl;
            downloadLink.href = videoUrl;

            statusDiv.classList.add('hidden');
            resultDiv.classList.remove('hidden');

            resultDiv.scrollIntoView({ behavior: 'smooth' });
        } else {
            throw new Error(data.error || 'Erreur inconnue');
        }
    } catch (error) {
        console.error(error);
        alert(`Erreur : ${error.message}`);
        statusDiv.classList.add('hidden');
    } finally {
        submitBtn.disabled = false;
    }
});
