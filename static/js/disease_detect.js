/**
 * Crop Disease Detection Client Script
 * Rythu Mithra
 */

document.addEventListener('DOMContentLoaded', function () {
    const dropZone = document.getElementById('dropZone');
    const imageInput = document.getElementById('imageInput');
    const previewContainer = document.getElementById('previewContainer');
    const imagePreview = document.getElementById('imagePreview');
    const removeImageBtn = document.getElementById('removeImageBtn');
    const fileInfo = document.getElementById('fileInfo');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const btnSpinner = document.getElementById('btnSpinner');
    const btnText = document.getElementById('btnText');
    const diseaseForm = document.getElementById('diseaseForm');

    const resultCard = document.getElementById('resultCard');
    const resultImage = document.getElementById('resultImage');
    const detectedCropDisease = document.getElementById('detectedCropDisease');
    const teluguName = document.getElementById('teluguName');
    const hindiName = document.getElementById('hindiName');
    const confidenceText = document.getElementById('confidenceText');
    const confidenceBar = document.getElementById('confidenceBar');
    const severityBadge = document.getElementById('severityBadge');
    const symptomsText = document.getElementById('symptomsText');
    const organicText = document.getElementById('organicText');
    const chemicalText = document.getElementById('chemicalText');
    const modelNoticeCard = document.getElementById('modelNoticeCard');
    const modelNoticeMessage = document.getElementById('modelNoticeMessage');

    let selectedFile = null;

    // 1. Drag and Drop Listeners
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.add('dragover');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.remove('dragover');
        });
    });

    dropZone.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        if (files && files.length > 0) {
            handleFileSelection(files[0]);
        }
    });

    // 2. File Input Selection
    imageInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files.length > 0) {
            handleFileSelection(e.target.files[0]);
        }
    });

    function handleFileSelection(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please select a valid image file (JPG, PNG, WEBP).');
            return;
        }

        if (file.size > 16 * 1024 * 1024) {
            alert('Image file exceeds the 16MB limit.');
            return;
        }

        selectedFile = file;

        // Display preview
        const reader = new FileReader();
        reader.onload = function (e) {
            imagePreview.src = e.target.result;
            previewContainer.classList.remove('d-none');
            dropZone.classList.add('d-none');
            analyzeBtn.disabled = false;

            const sizeMb = (file.size / (1024 * 1024)).toFixed(2);
            fileInfo.textContent = `${file.name} (${sizeMb} MB)`;
        };
        reader.readAsDataURL(file);
    }

    // 3. Remove Image Handler
    removeImageBtn.addEventListener('click', () => {
        selectedFile = null;
        imageInput.value = '';
        previewContainer.classList.add('d-none');
        dropZone.classList.remove('d-none');
        analyzeBtn.disabled = true;
        resultCard.classList.add('d-none');
        modelNoticeCard.classList.add('d-none');
    });

    // 4. Submit Image to API
    diseaseForm.addEventListener('submit', (e) => {
        e.preventDefault();
        if (!selectedFile) return;

        const formData = new FormData();
        formData.append('file', selectedFile);

        // UI loading state
        analyzeBtn.disabled = true;
        btnSpinner.classList.remove('d-none');
        btnText.textContent = 'Analyzing Leaf...';
        resultCard.classList.add('d-none');
        modelNoticeCard.classList.add('d-none');

        fetch('/api/disease/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            analyzeBtn.disabled = false;
            btnSpinner.classList.add('d-none');
            btnText.innerHTML = '<i class="bi bi-search me-1"></i> Diagnose Plant';

            if (!data.success) {
                alert(data.error || 'Failed to analyze crop image.');
                return;
            }

            // Case A: Model weights are not mounted yet
            if (data.model_ready === false) {
                modelNoticeMessage.textContent = data.message;
                modelNoticeCard.classList.remove('d-none');
                modelNoticeCard.scrollIntoView({ behavior: 'smooth' });
                return;
            }

            // Case B: Model inference succeeded
            resultImage.src = data.image_url;
            detectedCropDisease.textContent = `${data.crop} - ${data.disease}`;
            teluguName.textContent = `తెలుగు: ${data.telugu_name || 'N/A'}`;
            hindiName.textContent = `हिन्दी: ${data.hindi_name || 'N/A'}`;

            confidenceText.textContent = `${data.confidence}%`;
            confidenceBar.style.width = `${data.confidence}%`;

            severityBadge.textContent = `Severity: ${data.severity || 'Moderate'}`;
            severityBadge.className = `badge px-3 py-2 ${
                data.severity === 'Critical' ? 'bg-danger' :
                data.severity === 'High' ? 'bg-warning text-dark' : 'bg-success'
            }`;

            symptomsText.textContent = (data.symptoms && (data.symptoms.en || data.symptoms.te)) || 'None noted.';
            organicText.textContent = (data.organic_remedies && (data.organic_remedies.en || data.organic_remedies.te)) || 'Maintain standard cultural practices.';
            chemicalText.textContent = (data.chemical_treatment && (data.chemical_treatment.en || data.chemical_treatment.te)) || 'Consult local Krishi Vigyan Kendra.';

            resultCard.classList.remove('d-none');
            resultCard.scrollIntoView({ behavior: 'smooth' });
        })
        .catch(err => {
            analyzeBtn.disabled = false;
            btnSpinner.classList.add('d-none');
            btnText.innerHTML = '<i class="bi bi-search me-1"></i> Diagnose Plant';
            console.error('Error during disease detection:', err);
            alert('A network or server error occurred while processing the image.');
        });
    });
});
