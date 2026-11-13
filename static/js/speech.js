/**
 * Web Speech API Voice Input & Multilingual Advisory Controller
 * Rythu Mithra
 */

document.addEventListener('DOMContentLoaded', function () {
    const micBtn = document.getElementById('micBtn');
    const micIcon = document.getElementById('micIcon');
    const queryInput = document.getElementById('queryInput');
    const languageSelect = document.getElementById('languageSelect');
    const listeningStatus = document.getElementById('listeningStatus');
    const listeningText = document.getElementById('listeningText');
    const submitQueryBtn = document.getElementById('submitQueryBtn');
    const advisorySpinner = document.getElementById('advisorySpinner');
    const clearBtn = document.getElementById('clearBtn');
    const advisoryResultCard = document.getElementById('advisoryResultCard');
    const displayQuery = document.getElementById('displayQuery');
    const advisoryAnswer = document.getElementById('advisoryAnswer');
    const advisoryCategory = document.getElementById('advisoryCategory');
    const advisoryTimestamp = document.getElementById('advisoryTimestamp');
    const modelEngineBadge = document.getElementById('modelEngineBadge');
    const speakResponseBtn = document.getElementById('speakResponseBtn');
    const speechSupportBadge = document.getElementById('speechSupportBadge');

    let recognition = null;
    let isListening = false;
    let lastInputMode = 'text'; // 'voice' or 'text'
    let currentResponseText = '';
    let currentSpeechTag = 'te-IN';

    // Language mapping for Web Speech API
    const SPEECH_LANG_MAP = {
        'te': 'te-IN',
        'hi': 'hi-IN',
        'en': 'en-IN',
        'ta': 'ta-IN',
        'kn': 'kn-IN'
    };

    // 1. Check Web Speech API Availability
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        if (speechSupportBadge) {
            speechSupportBadge.className = 'badge bg-warning-subtle text-warning-emphasis border border-warning-subtle px-3 py-2';
            speechSupportBadge.innerHTML = '<i class="bi bi-exclamation-circle me-1"></i> Voice input not supported in this browser (Use Chrome or Edge)';
        }
        if (micBtn) {
            micBtn.disabled = true;
            micBtn.title = "Speech recognition is not supported in this browser. Please type your query.";
        }
    } else {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;

        recognition.onstart = function () {
            isListening = true;
            lastInputMode = 'voice';
            micBtn.classList.add('listening-pulse');
            micIcon.className = 'bi bi-mic-mute-fill fs-4';
            listeningStatus.classList.remove('d-none');
            const langName = languageSelect.options[languageSelect.selectedIndex].text;
            listeningText.textContent = `Listening... Speak now in ${langName}`;
        };

        recognition.onresult = function (event) {
            let transcript = '';
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                transcript += event.results[i][0].transcript;
            }
            queryInput.value = transcript;
        };

        recognition.onerror = function (event) {
            console.error('Speech recognition error:', event.error);
            stopListening();
            alert(`Voice recognition error: ${event.error}. Please try again or type manually.`);
        };

        recognition.onend = function () {
            stopListening();
            // If text was recognized, auto-enable submission or trigger submit
            if (queryInput.value.trim().length > 0) {
                submitQuery();
            }
        };

        micBtn.addEventListener('click', function () {
            if (isListening) {
                recognition.stop();
            } else {
                startListening();
            }
        });
    }

    function startListening() {
        if (!recognition) return;
        const selectedLang = languageSelect.value;
        recognition.lang = SPEECH_LANG_MAP[selectedLang] || 'te-IN';
        try {
            recognition.start();
        } catch (e) {
            console.warn("Recognition already started or error:", e);
        }
    }

    function stopListening() {
        isListening = false;
        if (micBtn) micBtn.classList.remove('listening-pulse');
        if (micIcon) micIcon.className = 'bi bi-mic-fill fs-4';
        if (listeningStatus) listeningStatus.classList.add('d-none');
    }

    // 2. Clear Button Handler
    if (clearBtn) {
        clearBtn.addEventListener('click', function () {
            queryInput.value = '';
            advisoryResultCard.classList.add('d-none');
            if (window.speechSynthesis) window.speechSynthesis.cancel();
        });
    }

    // 3. Sample Query Chips
    document.querySelectorAll('.sample-chip').forEach(button => {
        button.addEventListener('click', function () {
            const lang = this.getAttribute('data-lang');
            const text = this.getAttribute('data-text');
            if (languageSelect) languageSelect.value = lang;
            if (queryInput) queryInput.value = text;
            lastInputMode = 'text';
            submitQuery();
        });
    });

    // 4. Submit Advisory Query via AJAX
    if (submitQueryBtn) {
        submitQueryBtn.addEventListener('click', function () {
            lastInputMode = 'text';
            submitQuery();
        });
    }

    function submitQuery() {
        const query = queryInput.value.trim();
        if (!query) {
            alert("Please enter or speak an agricultural query.");
            return;
        }

        const selectedLang = languageSelect.value;

        // UI loading state
        submitQueryBtn.disabled = true;
        advisorySpinner.classList.remove('d-none');

        fetch('/api/advisory/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: query,
                language: selectedLang,
                input_type: lastInputMode
            })
        })
        .then(response => response.json())
        .then(data => {
            submitQueryBtn.disabled = false;
            advisorySpinner.classList.add('d-none');

            if (!data.success) {
                alert(data.error || 'Failed to fetch advisory.');
                return;
            }

            // Render result
            displayQuery.textContent = data.query;
            advisoryAnswer.textContent = data.response;
            advisoryCategory.textContent = data.category;
            advisoryTimestamp.textContent = data.timestamp;

            currentResponseText = data.response;
            currentSpeechTag = data.speech_tag || 'te-IN';

            if (data.nlp_status) {
                modelEngineBadge.innerHTML = `<i class="bi bi-cpu me-1"></i> ${data.nlp_status.model_type} (${data.nlp_status.info})`;
            }

            advisoryResultCard.classList.remove('d-none');
            advisoryResultCard.scrollIntoView({ behavior: 'smooth' });
        })
        .catch(err => {
            submitQueryBtn.disabled = false;
            advisorySpinner.classList.add('d-none');
            console.error('Advisory API error:', err);
            alert("An error occurred communicating with the server.");
        });
    }

    // 5. Text-to-Speech (TTS) for Farmers
    if (speakResponseBtn) {
        speakResponseBtn.addEventListener('click', function () {
            if (!('speechSynthesis' in window)) {
                alert("Text-to-speech is not supported in this browser.");
                return;
            }

            window.speechSynthesis.cancel(); // Stop any ongoing speech

            if (!currentResponseText) return;

            const utterance = new SpeechSynthesisUtterance(currentResponseText);
            utterance.lang = currentSpeechTag;
            utterance.rate = 0.95; // Slightly slower for clarity
            utterance.pitch = 1.0;

            window.speechSynthesis.speak(utterance);
        });
    }
});
