/**
 * ==============================================================================
 * Rythu Mithra (రైతు మిత్ర) - Core Application Client Controller (app.js)
 * Manages:
 * 1. Multilingual translation rendering & persistence.
 * 2. Mobile sidebar drawer toggling & active nav highlights.
 * 3. Dynamic date display in local formats.
 * 4. Web Speech API (te-IN & en-IN) with live mic visualizer.
 * 5. Prediction AJAX workflow & rich result rendering.
 * 6. History table real-time search & filters.
 * 7. Password visibility toggle.
 * 8. Text-to-Speech (TTS) audio narration for advisory.
 * ==============================================================================
 */

(function () {
    'use strict';

    // Helper to get cookie value
    function getCookie(name) {
        const matches = document.cookie.match(new RegExp('(?:^|; )' + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + '=([^;]*)'));
        return matches ? decodeURIComponent(matches[1]) : null;
    }

    // Resolve initial language preference
    const urlParams = new URLSearchParams(window.location.search);
    const urlLang = urlParams.get('lang');
    const htmlLang = document.documentElement.getAttribute('lang');
    let currentLang = (urlLang === 'en' || urlLang === 'te')
        ? urlLang
        : ((htmlLang === 'en' || htmlLang === 'te')
            ? htmlLang
            : (getCookie('rythu_lang') || localStorage.getItem('rythu_lang') || 'te'));

    if (currentLang !== 'en' && currentLang !== 'te') {
        currentLang = 'te';
    }

    // --------------------------------------------------------------------------
    // 1. Language Localization Engine
    // --------------------------------------------------------------------------
    function getTranslationsObj() {
        if (typeof window !== 'undefined' && window.TRANSLATIONS) {
            return window.TRANSLATIONS;
        }
        if (typeof TRANSLATIONS !== 'undefined') {
            return TRANSLATIONS;
        }
        return null;
    }

    window.t = function (key, fallback = '') {
        const allTrans = getTranslationsObj();
        if (allTrans && allTrans[currentLang] && allTrans[currentLang][key] !== undefined) {
            return allTrans[currentLang][key];
        }
        return fallback || key;
    };

    window.getCurrentLanguage = function () {
        return currentLang;
    };

    function applyTranslations(lang, notifyServer = true) {
        if (!lang || (lang !== 'te' && lang !== 'en')) {
            lang = 'te';
        }

        const allTrans = getTranslationsObj();
        if (!allTrans || !allTrans[lang]) {
            console.warn(`Translation dictionary for '${lang}' not loaded.`);
            return;
        }

        const dict = allTrans[lang];
        currentLang = lang;

        // Persist locally in localStorage
        localStorage.setItem('rythu_lang', lang);

        // Persist in Cookie so server-side rendering picks up preference
        document.cookie = `rythu_lang=${lang}; path=/; max-age=31536000; SameSite=Lax`;

        // Update root html element lang attribute
        document.documentElement.setAttribute('lang', lang);

        // Update elements with data-i18n (text content)
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (dict[key] !== undefined) {
                el.textContent = dict[key];
            }
        });

        // Update elements with data-i18n-html (inner HTML)
        document.querySelectorAll('[data-i18n-html]').forEach(el => {
            const key = el.getAttribute('data-i18n-html');
            if (dict[key] !== undefined) {
                el.innerHTML = dict[key];
            }
        });

        // Update input & textarea placeholders
        document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
            const key = el.getAttribute('data-i18n-placeholder');
            if (dict[key] !== undefined) {
                el.setAttribute('placeholder', dict[key]);
            }
        });

        // Update element tooltips & titles
        document.querySelectorAll('[data-i18n-title]').forEach(el => {
            const key = el.getAttribute('data-i18n-title');
            if (dict[key] !== undefined) {
                el.setAttribute('title', dict[key]);
            }
        });

        // Toggle bilingual content blocks if present on page
        document.querySelectorAll('.lang-te-content').forEach(el => {
            if (lang === 'te') {
                el.classList.remove('d-none');
            } else {
                el.classList.add('d-none');
            }
        });
        document.querySelectorAll('.lang-en-content').forEach(el => {
            if (lang === 'en') {
                el.classList.remove('d-none');
            } else {
                el.classList.add('d-none');
            }
        });

        // Update active state on all language toggle buttons across UI
        document.querySelectorAll('.lang-toggle-btn').forEach(btn => {
            if (btn.getAttribute('data-lang') === lang) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });

        // Update TTS button label if present
        const ttsBtnText = document.getElementById('ttsBtnText');
        if (ttsBtnText) {
            ttsBtnText.textContent = lang === 'te' ? 'వినండి (Listen)' : 'Listen (Audio)';
        }

        // Dynamically update prediction CTA button if prediction result is visible
        const advisoryBtn = document.getElementById('res-advisory-btn');
        if (advisoryBtn) {
            const isFollowUp = advisoryBtn.getAttribute('data-is-followup') === 'true';
            if (isFollowUp) {
                advisoryBtn.innerHTML = `<i class="bi bi-patch-question-fill me-2"></i> ${dict['res_btn_followup'] || 'Review Diagnostic Questions & Guidance'}`;
            } else {
                advisoryBtn.innerHTML = `<i class="bi bi-book-half me-2"></i> ${dict['res_btn_advisory'] || 'View Treatment & Spray Advisory'}`;
            }
        }

        // Update all relative navigation links to persist current language
        document.querySelectorAll('a[href]').forEach(a => {
            try {
                const href = a.getAttribute('href');
                if (href && !href.startsWith('#') && !href.startsWith('javascript:') && !href.startsWith('http://') && !href.startsWith('https://')) {
                    const u = new URL(href, window.location.origin);
                    u.searchParams.set('lang', lang);
                    a.setAttribute('href', u.pathname + u.search + u.hash);
                }
            } catch (e) {}
        });

        // Update date display
        updateCurrentDateDisplay();

        // Notify Flask server asynchronously to sync session and DB
        if (notifyServer) {
            fetch('/api/set-language', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ language: lang })
            }).catch(err => {
                console.debug('Asynchronous language sync to server:', err);
            });
        }

        // Dispatch language change event for custom components
        document.dispatchEvent(new CustomEvent('languageChanged', { detail: { language: lang } }));
    }

    window.switchLanguage = function (lang) {
        if (!lang || (lang !== 'te' && lang !== 'en')) {
            lang = 'te';
        }
        currentLang = lang;
        localStorage.setItem('rythu_lang', lang);
        document.cookie = `rythu_lang=${lang}; path=/; max-age=31536000; SameSite=Lax`;
        document.documentElement.setAttribute('lang', lang);
        applyTranslations(lang, true);

        // Always reload/navigate with ?lang= to guarantee 100% server + client rendering parity
        try {
            const url = new URL(window.location.href);
            url.searchParams.set('lang', lang);
            window.location.href = url.toString();
        } catch (e) {
            window.location.reload();
        }
    };

    // --------------------------------------------------------------------------
    // 2. Dynamic Date Display
    // --------------------------------------------------------------------------
    function updateCurrentDateDisplay() {
        const dateEl = document.getElementById('currentDateDisplay');
        if (!dateEl) return;

        const now = new Date();
        const options = { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' };
        if (currentLang === 'te') {
            dateEl.textContent = now.toLocaleDateString('te-IN', options);
        } else {
            dateEl.textContent = now.toLocaleDateString('en-US', options);
        }
    }

    // --------------------------------------------------------------------------
    // 3. Mobile Sidebar Drawer Controller
    // --------------------------------------------------------------------------
    window.toggleMobileSidebar = function () {
        const sidebar = document.getElementById('appSidebar');
        const overlay = document.getElementById('sidebarBackdrop');
        if (!sidebar) return;

        sidebar.classList.toggle('show');
        if (overlay) {
            overlay.classList.toggle('d-none');
        }
    };

    window.closeMobileSidebar = function () {
        const sidebar = document.getElementById('appSidebar');
        const overlay = document.getElementById('sidebarBackdrop');
        if (sidebar) sidebar.classList.remove('show');
        if (overlay) overlay.classList.add('d-none');
    };

    // --------------------------------------------------------------------------
    // 4. Web Speech API Voice Recognition (Telugu & English)
    // --------------------------------------------------------------------------
    let recognitionInstance = null;
    let isListening = false;

    window.startSpeechRecognition = function (targetTextareaId, langCode, statusElementId) {
        const textarea = document.getElementById(targetTextareaId);
        const statusEl = document.getElementById(statusElementId);
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        if (!SpeechRecognition) {
            const msg = currentLang === 'te'
                ? "మీ బ్రౌజర్‌లో వాయిస్ రికగ్నిషన్ సదుపాయం లేదు. దయచేసి Google Chrome లేదా Edge బ్రౌజర్ ఉపయోగించండి."
                : "Web Speech API is not supported in this browser. Please use Google Chrome or Edge.";
            alert(msg);
            return;
        }

        if (isListening && recognitionInstance) {
            recognitionInstance.stop();
            return;
        }

        try {
            recognitionInstance = new SpeechRecognition();
            recognitionInstance.lang = langCode; // 'te-IN' or 'en-IN'
            recognitionInstance.interimResults = true;
            recognitionInstance.maxAlternatives = 1;
            recognitionInstance.continuous = false;

            recognitionInstance.onstart = function () {
                isListening = true;
                if (statusEl) {
                    statusEl.classList.remove('d-none');
                    statusEl.innerHTML = `
                        <div class="d-flex align-items-center gap-2 text-danger fw-bold py-1">
                            <span class="spinner-grow spinner-grow-sm text-danger" role="status"></span>
                            <span>${currentLang === 'te' ? 'వాయిస్ వింటోంది... మాట్లాడండి' : 'Listening... Speak your symptoms'} (${langCode})</span>
                            <button type="button" class="btn btn-sm btn-outline-danger ms-auto rounded-pill py-0 px-2" onclick="stopSpeechRecognition('${statusElementId}')">Stop</button>
                        </div>
                    `;
                }

                document.querySelectorAll('.btn-voice-modern').forEach(b => {
                    if (b.getAttribute('data-lang-code') === langCode) {
                        b.classList.add('listening-pulse');
                    }
                });
            };

            recognitionInstance.onresult = function (event) {
                let finalTranscript = '';
                for (let i = event.resultIndex; i < event.results.length; ++i) {
                    if (event.results[i].isFinal) {
                        finalTranscript += event.results[i][0].transcript;
                    }
                }

                if (finalTranscript && textarea) {
                    const currentVal = textarea.value.trim();
                    textarea.value = currentVal ? currentVal + " " + finalTranscript : finalTranscript;
                    textarea.focus();
                }
            };

            recognitionInstance.onerror = function (event) {
                console.error("Speech recognition error:", event.error);
                if (statusEl) {
                    let errMsg = event.error;
                    if (event.error === 'not-allowed') {
                        errMsg = currentLang === 'te' ? 'మైక్రోఫోన్ అనుమతి నిరాకరించబడింది.' : 'Microphone permission denied.';
                    } else if (event.error === 'no-speech') {
                        errMsg = currentLang === 'te' ? 'ఎలాంటి వాయిస్ వినిపించలేదు. మళ్లీ ప్రయత్నించండి.' : 'No speech detected. Please try again.';
                    }
                    statusEl.innerHTML = `<span class="text-danger small"><i class="bi bi-exclamation-triangle me-1"></i> ${errMsg}</span>`;
                }
                resetListeningState();
            };

            recognitionInstance.onend = function () {
                resetListeningState();
                if (statusEl) {
                    setTimeout(() => {
                        if (!isListening) statusEl.classList.add('d-none');
                    }, 3500);
                }
            };

            recognitionInstance.start();

        } catch (err) {
            console.error("Speech initialization exception:", err);
            resetListeningState();
        }
    };

    window.stopSpeechRecognition = function (statusElementId) {
        if (recognitionInstance) {
            recognitionInstance.stop();
        }
        resetListeningState();
        const statusEl = document.getElementById(statusElementId);
        if (statusEl) statusEl.classList.add('d-none');
    };

    function resetListeningState() {
        isListening = false;
        document.querySelectorAll('.btn-voice-modern').forEach(b => b.classList.remove('listening-pulse'));
    }

    // --------------------------------------------------------------------------
    // 5. Prediction Form AJAX Workflow & Dynamic Quick Add (POST /api/predict)
    // --------------------------------------------------------------------------
    window.initPredictionForm = function () {
        const form = document.getElementById('disease-prediction-form');
        if (!form) return;

        const cropSelect = document.getElementById('crop_select');
        const stageSelect = document.getElementById('stage_select');
        const symptomInput = document.getElementById('symptom_description');
        const submitBtn = document.getElementById('submit-predict-btn');
        const loadingIndicator = document.getElementById('predict-loading-indicator');
        const resultsSection = document.getElementById('prediction-results-section');
        const errorAlert = document.getElementById('predict-error-alert');
        const quickAddContainer = document.getElementById('quick-add-container');
        const quickAddChips = document.getElementById('quick-add-chips');
        const quickAddCropLabel = document.getElementById('quick-add-crop-label');

        // Track active chips so toggling works cleanly
        let activeChips = new Set();

        // Dynamic Crop Symptoms Quick Add Loader
        async function loadCropSymptoms(cropName) {
            if (!quickAddContainer || !quickAddChips) return;
            if (!cropName) {
                quickAddContainer.classList.add('d-none');
                quickAddChips.innerHTML = '';
                activeChips.clear();
                return;
            }

            try {
                const res = await fetch(`/api/crop-symptoms?crop=${encodeURIComponent(cropName)}&lang=${currentLang}`);
                const data = await res.json();

                if (!res.ok || !data.available || !Array.isArray(data.symptoms) || data.symptoms.length === 0) {
                    quickAddContainer.classList.add('d-none');
                    quickAddChips.innerHTML = '';
                    activeChips.clear();
                    return;
                }

                if (quickAddCropLabel) {
                    quickAddCropLabel.textContent = currentLang === 'te' ? (data.crop_te || data.crop) : data.crop;
                }

                quickAddChips.innerHTML = '';
                activeChips.clear();

                data.symptoms.forEach(item => {
                    const btn = document.createElement('button');
                    btn.type = 'button';
                    btn.className = 'btn btn-sm btn-outline-success rounded-pill px-3 py-2 fw-semibold d-inline-flex align-items-center gap-1 shadow-sm';
                    const labelText = currentLang === 'te' ? (item.label_te || item.label_en) : item.label_en;
                    const snippetText = currentLang === 'te' ? (item.symptom_te || item.symptom_en) : item.symptom_en;

                    btn.setAttribute('data-id', item.id);
                    btn.setAttribute('data-snippet', snippetText);
                    btn.innerHTML = `<i class="bi bi-plus-circle"></i> <span>${labelText}</span>`;

                    btn.addEventListener('click', function () {
                        const snippet = this.getAttribute('data-snippet');
                        const chipId = this.getAttribute('data-id');

                        if (activeChips.has(chipId)) {
                            // Unselect chip: Remove snippet from textarea
                            activeChips.delete(chipId);
                            this.classList.remove('btn-success', 'text-white');
                            this.classList.add('btn-outline-success');
                            this.querySelector('i').className = 'bi bi-plus-circle';

                            if (symptomInput) {
                                let cur = symptomInput.value;
                                cur = cur.replace(snippet, '').replace(/\s{2,}/g, ' ').trim();
                                symptomInput.value = cur;
                            }
                        } else {
                            // Select chip: Append snippet to textarea
                            activeChips.add(chipId);
                            this.classList.remove('btn-outline-success');
                            this.classList.add('btn-success', 'text-white');
                            this.querySelector('i').className = 'bi bi-check-circle-fill';

                            if (symptomInput) {
                                const cur = symptomInput.value.trim();
                                if (cur && !cur.includes(snippet)) {
                                    symptomInput.value = `${cur} ${snippet}`;
                                } else if (!cur) {
                                    symptomInput.value = snippet;
                                }
                            }
                        }
                    });

                    quickAddChips.appendChild(btn);
                });

                quickAddContainer.classList.remove('d-none');
            } catch (err) {
                console.debug("Crop symptoms fetch error:", err);
                quickAddContainer.classList.add('d-none');
            }
        }

        // Bind crop change listener
        if (cropSelect) {
            cropSelect.addEventListener('change', function () {
                loadCropSymptoms(this.value);
            });
            // Initial load if already selected
            if (cropSelect.value) {
                loadCropSymptoms(cropSelect.value);
            }
        }

        // Re-load symptoms when language changes
        document.addEventListener('languageChanged', function (e) {
            if (cropSelect && cropSelect.value) {
                loadCropSymptoms(cropSelect.value);
            }
        });

        // Form Submit Handler
        form.addEventListener('submit', async function (e) {
            e.preventDefault();

            if (errorAlert) errorAlert.classList.add('d-none');
            if (resultsSection) resultsSection.classList.add('d-none');

            const description = symptomInput ? symptomInput.value.trim() : '';
            const crop = cropSelect ? cropSelect.value : '';
            const cropStage = stageSelect ? stageSelect.value : '';

            if (!description) {
                showError(
                    currentLang === 'te'
                        ? "దయచేసి మీ పంట లక్షణాలను వివరించండి లేదా వాయిస్ ద్వారా చెప్పండి."
                        : "Please describe your crop symptoms or use voice input."
                );
                symptomInput.focus();
                return;
            }

            if (description.length < 3) {
                showError(
                    currentLang === 'te'
                        ? "లక్షణాల వివరణ చాలా చిన్నదిగా ఉంది. దయచేసి మరిన్ని వివరాలు ఇవ్వండి."
                        : "Symptom description is too short. Please provide more details."
                );
                symptomInput.focus();
                return;
            }

            if (submitBtn) submitBtn.disabled = true;
            if (loadingIndicator) loadingIndicator.classList.remove('d-none');

            try {
                const response = await fetch('/api/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({
                        description: description,
                        crop: crop,
                        crop_stage: cropStage,
                        language: currentLang
                    })
                });

                const data = await response.json();

                if (!response.ok || !data.success) {
                    throw new Error(data.message || data.error || "Failed to generate prediction.");
                }

                renderPredictionResults(data, crop);

            } catch (err) {
                console.error("Prediction API error:", err);
                showError(err.message || "An unexpected error occurred during prediction.");
            } finally {
                if (submitBtn) submitBtn.disabled = false;
                if (loadingIndicator) loadingIndicator.classList.add('d-none');
            }
        });

        function showError(msg) {
            const errorAlert = document.getElementById('predict-error-alert');
            if (errorAlert) {
                errorAlert.textContent = msg;
                errorAlert.classList.remove('d-none');
                errorAlert.scrollIntoView({ behavior: 'smooth', block: 'center' });
            } else {
                alert(msg);
            }
        }

        function renderPredictionResults(data, cropName) {
            const resultsSection = document.getElementById('prediction-results-section');
            if (!resultsSection) return;

            const predDiseaseEl = document.getElementById('res-predicted-disease');
            const scientificRow = document.getElementById('res-scientific-row');
            const scientificNameEl = document.getElementById('res-scientific-name');
            const cropNameEl = document.getElementById('res-crop-name');
            const severityBadge = document.getElementById('res-severity-badge');
            const severityText = document.getElementById('res-severity-text');
            const predScoreEl = document.getElementById('res-prediction-score');
            const predScoreBar = document.getElementById('res-score-progress-bar');
            const scoreExplanationEl = document.getElementById('res-score-explanation');
            const topListEl = document.getElementById('res-top-predictions-list');
            const warningAlert = document.getElementById('res-warning-alert');
            const messageEl = document.getElementById('res-message-text');
            const advisoryBtn = document.getElementById('res-advisory-btn');
            const refineContainer = document.getElementById('res-refine-container');
            const refineQuestionsList = document.getElementById('res-refine-questions-list');
            const refineBtn = document.getElementById('btn-refine-diagnosis');

            // 1. Identified Pathogen
            if (predDiseaseEl) {
                predDiseaseEl.textContent = data.prediction || "Requires further diagnosis";
            }

            // 2. Scientific Name
            if (scientificRow && scientificNameEl) {
                if (data.scientific_name) {
                    scientificNameEl.textContent = data.scientific_name;
                    scientificRow.classList.remove('d-none');
                } else {
                    scientificRow.classList.add('d-none');
                }
            }

            // 3. Crop Name
            if (cropNameEl) {
                cropNameEl.textContent = data.crop || cropName || "General Crop";
            }

            // 4. Severity Badge
            const severityVal = (data.advisory && data.advisory.severity) ? data.advisory.severity : (data.score >= 0.8 ? "High" : "Moderate");
            if (severityBadge && severityText) {
                severityText.textContent = `${severityVal} Severity`;
                if (severityVal.toLowerCase().includes('high')) {
                    severityBadge.className = 'badge bg-danger-subtle text-danger px-3 py-2 rounded-pill fw-bold border border-danger-subtle';
                } else if (severityVal.toLowerCase().includes('mod') || severityVal.toLowerCase().includes('med')) {
                    severityBadge.className = 'badge bg-warning-subtle text-warning-emphasis px-3 py-2 rounded-pill fw-bold border border-warning-subtle';
                } else {
                    severityBadge.className = 'badge bg-success-subtle text-success px-3 py-2 rounded-pill fw-bold border border-success-subtle';
                }
            }

            // 5. Prediction Score & Progress Bar
            const scoreVal = typeof data.score === 'number' ? data.score : 0.0;
            const pct = Math.min(100, Math.round(scoreVal <= 1.0 ? scoreVal * 100 : scoreVal));
            if (predScoreEl) predScoreEl.textContent = `${pct}%`;
            if (predScoreBar) {
                predScoreBar.style.width = `${pct}%`;
                predScoreBar.className = `progress-bar-modern ${pct >= 75 ? 'bg-success' : pct >= 45 ? 'bg-warning' : 'bg-danger'}`;
            }
            if (scoreExplanationEl && data.score_explanation) {
                scoreExplanationEl.textContent = data.score_explanation;
            }

            // 6. Message text
            if (messageEl) {
                messageEl.textContent = data.message || "";
            }

            // 7. Uncertainty Warning & Interactive Refinement
            if (data.needs_further_diagnosis) {
                if (warningAlert) warningAlert.classList.remove('d-none');

                if (refineContainer && refineQuestionsList) {
                    refineQuestionsList.innerHTML = '';
                    const questions = Array.isArray(data.diagnostic_questions)
                        ? data.diagnostic_questions
                        : (data.diagnostic_questions && data.diagnostic_questions[currentLang]) || [];

                    if (questions.length > 0) {
                        questions.forEach((q, qIdx) => {
                            const qText = typeof q === 'object' ? (q.question || q.label || JSON.stringify(q)) : q;
                            const qDiv = document.createElement('div');
                            qDiv.className = 'form-check p-3 bg-white rounded-3 border shadow-sm';
                            qDiv.innerHTML = `
                                <input class="form-check-input ms-0 me-3 refine-q-checkbox" type="checkbox" id="refine_q_${qIdx}" value="${qText}">
                                <label class="form-check-label text-dark fw-semibold small" for="refine_q_${qIdx}">
                                    ${qText}
                                </label>
                            `;
                            refineQuestionsList.appendChild(qDiv);
                        });

                        refineContainer.classList.remove('d-none');

                        // Bind Refine Submit Button
                        if (refineBtn) {
                            refineBtn.onclick = async function () {
                                const checkedBoxes = refineQuestionsList.querySelectorAll('.refine-q-checkbox:checked');
                                const selectedAnswers = Array.from(checkedBoxes).map(cb => cb.value);

                                if (selectedAnswers.length === 0) {
                                    alert(currentLang === 'te' ? "దయచేసి కనీసం ఒక లక్షణాన్ని లేదా సమాధానాన్ని ఎంచుకోండి." : "Please select at least one observed sign to refine diagnosis.");
                                    return;
                                }

                                refineBtn.disabled = true;
                                refineBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-1"></span> ${currentLang === 'te' ? "విశ్లేషిస్తోంది..." : "Refining..."}`;

                                try {
                                    const refResponse = await fetch('/api/predict', {
                                        method: 'POST',
                                        headers: { 'Content-Type': 'application/json' },
                                        body: JSON.stringify({
                                            description: symptomInput ? symptomInput.value.trim() : '',
                                            crop: cropSelect ? cropSelect.value : (data.crop || ''),
                                            crop_stage: stageSelect ? stageSelect.value : '',
                                            language: currentLang,
                                            answers: selectedAnswers
                                        })
                                    });

                                    const refData = await refResponse.json();
                                    if (refData.success) {
                                        renderPredictionResults(refData, cropName);
                                    }
                                } catch (err) {
                                    console.error("Refinement error:", err);
                                } finally {
                                    refineBtn.disabled = false;
                                    refineBtn.innerHTML = `<i class="bi bi-arrow-clockwise me-1"></i> ${window.t('btn_refine_diagnosis', 'Refine Diagnosis with Answers')}`;
                                }
                            };
                        }
                    } else {
                        refineContainer.classList.add('d-none');
                    }
                }
            } else {
                if (warningAlert) warningAlert.classList.add('d-none');
                if (refineContainer) refineContainer.classList.add('d-none');
            }

            // 8. Top 3 Predictions Breakdown
            if (topListEl && Array.isArray(data.top_predictions)) {
                topListEl.innerHTML = '';
                data.top_predictions.forEach((item, idx) => {
                    const itemScore = typeof item.score === 'number' ? item.score : 0.0;
                    const itemPct = item.percentage || Math.min(100, Math.round(itemScore <= 1.0 ? itemScore * 100 : itemScore));
                    const scientific = item.scientific ? `<span class="text-muted fst-italic small">(${item.scientific})</span>` : '';
                    const div = document.createElement('div');
                    div.className = 'mb-2 p-3 rounded-3 bg-white border';
                    div.innerHTML = `
                        <div class="d-flex justify-content-between align-items-center mb-1">
                            <div>
                                <span class="fw-bold text-dark">${idx + 1}. ${item.label}</span>
                                ${scientific}
                            </div>
                            <span class="badge bg-success-subtle text-success-emphasis fw-bold px-2 py-1">${itemPct}%</span>
                        </div>
                        <div class="progress-track-modern">
                            <div class="progress-bar-modern" style="width: ${itemPct}%"></div>
                        </div>
                    `;
                    topListEl.appendChild(div);
                });
            }

            // Populate Farmer Reported Symptoms Card
            const farmerSymptomsEl = document.getElementById('res-farmer-symptoms-text');
            if (farmerSymptomsEl) {
                farmerSymptomsEl.textContent = (symptomInput ? symptomInput.value.trim() : '') || data.symptom_description || "N/A";
            }

            // 9. Full Actionable Agricultural Solutions Accordion (13-Part Visual Hierarchy)
            const adv = data.advisory || {};
            const immStructured = adv.immediate_action_structured;
            const whatProblemEl = document.getElementById('sol-what-is-problem');
            const whyOccursEl = document.getElementById('sol-why-it-occurs');
            const immStepsList = document.getElementById('sol-immediate-steps');
            const urgencyEl = document.getElementById('sol-action-urgency');

            if (whatProblemEl) {
                whatProblemEl.textContent = (immStructured && immStructured.what_is_problem) || (currentLang === 'te' ? adv.advisory_te : adv.advisory_en) || "--";
            }
            if (whyOccursEl) {
                whyOccursEl.textContent = (immStructured && immStructured.why_it_occurs) || (currentLang === 'te' ? "వాతావరణ పరిస్థితులు, అధిక తేమ మరియు నిర్వహణ లోపాలు తెగులుకు కారణం కావచ్చు." : "Weather conditions, humidity, and management factors may trigger symptom development.");
            }
            if (immStepsList) {
                immStepsList.innerHTML = '';
                const steps = (immStructured && Array.isArray(immStructured.steps) && immStructured.steps.length > 0)
                    ? immStructured.steps
                    : [adv.immediate_actions || (currentLang === 'te' ? "పొలాన్ని పరిశీలించి నిలిచిన నీటిని తీసివేయండి." : "Inspect the field and drain excess standing water.")];
                steps.forEach(step => {
                    const li = document.createElement('li');
                    li.className = 'mb-1';
                    li.textContent = step;
                    immStepsList.appendChild(li);
                });
            }
            if (urgencyEl) {
                urgencyEl.textContent = (immStructured && immStructured.urgency) || (currentLang === 'te' ? "మధ్యస్థ అత్యవసరం: 48 గంటల్లో నివారణ చర్యలు చేపట్టండి." : "Moderate Urgency: Initiate corrective measures within 48 hours.");
            }

            // Chemical Control Structured Fields
            const chemStructured = adv.chemical_structured;
            const chemVerifiedBox = document.getElementById('sol-chem-verified-box');
            const chemUnverifiedBox = document.getElementById('sol-chem-unverified-box');
            const chemProductEl = document.getElementById('sol-chem-product');
            const chemDosageEl = document.getElementById('sol-chem-dosage');
            const chemWaterEl = document.getElementById('sol-chem-water');
            const chemMethodEl = document.getElementById('sol-chem-method');
            const chemPhiEl = document.getElementById('sol-chem-phi');
            const chemSafetyEl = document.getElementById('sol-chem-safety');
            const chemUnverifiedMsg = document.getElementById('sol-chem-unverified-msg');

            if (chemStructured && chemStructured.has_verified_chemical && !data.needs_further_diagnosis) {
                if (chemVerifiedBox) chemVerifiedBox.classList.remove('d-none');
                if (chemUnverifiedBox) chemUnverifiedBox.classList.add('d-none');
                if (chemProductEl) chemProductEl.textContent = chemStructured.product || "--";
                if (chemDosageEl) chemDosageEl.textContent = chemStructured.dosage || "--";
                if (chemWaterEl) chemWaterEl.textContent = chemStructured.water_quantity || (currentLang === 'te' ? "ఎకరాకు 200 లీటర్ల నీరు" : "200 Litres water / acre");
                if (chemMethodEl) chemMethodEl.textContent = chemStructured.application_method || (currentLang === 'te' ? "ఆకులపై పిచికారీ" : "Foliar spray");
                if (chemPhiEl) chemPhiEl.textContent = chemStructured.waiting_period_phi || (currentLang === 'te' ? "లేబుల్ సూచనలు పాటించండి" : "Follow CIBRC product label");
                if (chemSafetyEl) chemSafetyEl.textContent = chemStructured.safety_precaution || (currentLang === 'te' ? "చేతి తొడుగులు, మాస్క్ ధరించండి" : "Wear protective PPE; do not spray against wind");
            } else {
                if (chemVerifiedBox) chemVerifiedBox.classList.add('d-none');
                if (chemUnverifiedBox) chemUnverifiedBox.classList.remove('d-none');
                const fallbackMsg = (chemStructured && chemStructured.unverified_message) ||
                    (currentLang === 'te'
                        ? "ఈ నిర్ధారణకు ధృవీకరించబడిన రసాయన సిఫారసు అందుబాటులో లేదు. ఖచ్చితమైన నిర్ధారణ లేకుండా పురుగుమందులు వాడవద్దు."
                        : "No verified chemical recommendation is available for this diagnosis. Do not spray chemicals without confirmed pathogen identification.");
                if (chemUnverifiedMsg) chemUnverifiedMsg.textContent = fallbackMsg;
            }

            // Prevention Structured Recommendations & Next Season Sub-section
            const prevStructured = adv.prevention_structured;
            const prevStepsList = document.getElementById('sol-prevention-steps');
            const nextSeasonText = document.getElementById('sol-next-season-text');

            if (prevStepsList) {
                prevStepsList.innerHTML = '';
                const pSteps = (prevStructured && Array.isArray(prevStructured.steps) && prevStructured.steps.length > 0)
                    ? prevStructured.steps
                    : [adv.prevention || (currentLang === 'te' ? "నాణ్యమైన విత్తన శుద్ధి చేయండి, పంట మార్పిడి పాటించండి." : "Use certified treated seed and practice crop rotation.")];
                pSteps.forEach(st => {
                    const li = document.createElement('li');
                    li.className = 'mb-1';
                    li.textContent = st;
                    prevStepsList.appendChild(li);
                });
            }
            if (nextSeasonText) {
                nextSeasonText.textContent = (prevStructured && prevStructured.next_season) ||
                    (currentLang === 'te' ? "వేసవిలో లోతు దుక్కులు చేసి తెగులు శేషాలను నాశనం చేయండి మరియు విత్తన శుద్ధి తప్పనిసరిగా చేయండి." : "Conduct deep summer plowing to solarize fungal spores and ensure certified seed treatment.");
            }

            // Organic, Biological, Cultural, Safety
            const solOrganic = document.getElementById('sol-organic-text');
            const solBio = document.getElementById('sol-bio-text');
            const solCultural = document.getElementById('sol-cultural-text');
            const solSafety = document.getElementById('sol-safety-text');

            if (solOrganic) solOrganic.textContent = adv.organic_management || (currentLang === 'te' ? "5% వేప గింజల కషాయం పిచికారీ చేయండి." : "Apply 5% Neem Seed Kernel Extract (NSKE) or organic botanicals.");
            if (solBio) solBio.textContent = adv.biological_control || (currentLang === 'te' ? "జిగురు అట్టలు అమర్చండి లేదా ట్రైకోడెర్మా వాడండి." : "Install sticky traps or apply Trichoderma viride.");
            if (solCultural) solCultural.textContent = adv.cultural_control || (currentLang === 'te' ? "పొలం పరిశుభ్రత మరియు సమతుల్య ఎరువుల వాడకం పాటించండి." : "Maintain field sanitation and balanced fertilization.");
            if (solSafety) solSafety.textContent = adv.safety_precautions || (currentLang === 'te' ? "చేతి తొడుగులు, మాస్క్ ధరించండి. గాలికి ఎదురుగా పిచికారీ చేయవద్దు." : "Wear protective gloves and mask. Never spray against the wind.");

            // 10. Advisory Redirect Link
            if (advisoryBtn) {
                if (data.advisory_url) {
                    advisoryBtn.href = data.advisory_url;
                } else if (data.needs_further_diagnosis) {
                    advisoryBtn.href = `/advisory?needs_further_diagnosis=true&crop=${encodeURIComponent(cropName || '')}&prediction_id=${data.prediction_id || ''}&lang=${currentLang}`;
                } else {
                    const diseaseParam = encodeURIComponent(data.prediction || "");
                    const cropParam = encodeURIComponent(cropName || "");
                    const predIdParam = data.prediction_id ? `&prediction_id=${data.prediction_id}` : '';
                    advisoryBtn.href = `/advisory?disease=${diseaseParam}&crop=${cropParam}${predIdParam}&lang=${currentLang}`;
                }

                if (data.needs_further_diagnosis) {
                    advisoryBtn.setAttribute('data-is-followup', 'true');
                    advisoryBtn.className = "btn btn-warning fw-bold text-dark px-4 py-3 shadow";
                    advisoryBtn.innerHTML = `<i class="bi bi-patch-question-fill me-2"></i> ${window.t('res_btn_followup', 'Review Diagnostic Questions & Guidance')}`;
                } else {
                    advisoryBtn.setAttribute('data-is-followup', 'false');
                    advisoryBtn.className = "btn btn-premium-primary px-4 py-3 shadow";
                    advisoryBtn.innerHTML = `<i class="bi bi-book-half me-2"></i> ${window.t('res_btn_advisory', 'View Treatment & Spray Advisory')}`;
                }
            }

            resultsSection.classList.remove('d-none');
            resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    };

    // --------------------------------------------------------------------------
    // 6. History Table Live Filter & Search
    // --------------------------------------------------------------------------
    window.initHistoryFilters = function () {
        const searchInput = document.getElementById('historySearchInput');
        const cropFilter = document.getElementById('historyCropFilter');
        const diseaseFilter = document.getElementById('historyDiseaseFilter');
        const tableBody = document.getElementById('historyTableBody');

        if (!tableBody) return;

        function filterRows() {
            const query = searchInput ? searchInput.value.toLowerCase().trim() : '';
            const selectedCrop = cropFilter ? cropFilter.value.toLowerCase().trim() : '';
            const selectedDisease = diseaseFilter ? diseaseFilter.value.toLowerCase().trim() : '';

            const rows = tableBody.querySelectorAll('tr[data-history-row]');
            let visibleCount = 0;

            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                const rowCrop = (row.getAttribute('data-crop') || '').toLowerCase();
                const rowDisease = (row.getAttribute('data-disease') || '').toLowerCase();

                const matchesQuery = !query || text.includes(query);
                const matchesCrop = !selectedCrop || rowCrop === selectedCrop;
                const matchesDisease = !selectedDisease || rowDisease.includes(selectedDisease);

                if (matchesQuery && matchesCrop && matchesDisease) {
                    row.style.display = '';
                    visibleCount++;
                } else {
                    row.style.display = 'none';
                }
            });

            const noMatchEl = document.getElementById('historyNoMatches');
            if (noMatchEl) {
                if (visibleCount === 0 && rows.length > 0) {
                    noMatchEl.classList.remove('d-none');
                } else {
                    noMatchEl.classList.add('d-none');
                }
            }
        }

        if (searchInput) searchInput.addEventListener('input', filterRows);
        if (cropFilter) cropFilter.addEventListener('change', filterRows);
        if (diseaseFilter) diseaseFilter.addEventListener('change', filterRows);
    };

    // --------------------------------------------------------------------------
    // 7. Password Visibility Toggle
    // --------------------------------------------------------------------------
    window.togglePasswordVisibility = function (inputId, toggleIconId) {
        const input = document.getElementById(inputId);
        const icon = document.getElementById(toggleIconId);
        if (!input || !icon) return;

        if (input.type === 'password') {
            input.type = 'text';
            icon.classList.remove('bi-eye');
            icon.classList.add('bi-eye-slash');
        } else {
            input.type = 'password';
            icon.classList.remove('bi-eye-slash');
            icon.classList.add('bi-eye');
        }
    };

    // --------------------------------------------------------------------------
    // 8. Text-to-Speech (TTS) for Agricultural Advisory
    // --------------------------------------------------------------------------
    window.speakText = function (textElementId, lang) {
        const el = document.getElementById(textElementId);
        if (!el || !('speechSynthesis' in window)) {
            alert("Text-to-Speech is not supported in this browser.");
            return;
        }

        const text = el.innerText || el.textContent;
        if (!text) return;

        window.speechSynthesis.cancel(); // Stop any active speech

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = lang === 'te' ? 'te-IN' : 'en-IN';
        utterance.rate = 0.95; // Slightly slower for better farmer comprehension

        window.speechSynthesis.speak(utterance);
    };

    window.speakDiagnosisAdvisory = function () {
        const disease = document.getElementById('res-predicted-disease')?.innerText || '';
        const prob = document.getElementById('sol-what-is-problem')?.innerText || '';
        const urgency = document.getElementById('sol-action-urgency')?.innerText || '';
        const fullText = `${disease}. ${prob} ${urgency}`;
        if (!fullText.trim() || fullText.includes('--')) return;

        if (!('speechSynthesis' in window)) {
            alert("Text-to-Speech is not supported in this browser.");
            return;
        }
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(fullText);
        utterance.lang = currentLang === 'te' ? 'te-IN' : 'en-IN';
        utterance.rate = 0.95;
        window.speechSynthesis.speak(utterance);
    };

    // --------------------------------------------------------------------------
    // 9. Global DOM Ready Initialization
    // --------------------------------------------------------------------------
    document.addEventListener('DOMContentLoaded', function () {
        // Apply localization on page ready
        applyTranslations(currentLang, false);

        // Bind language toggle buttons safely
        document.querySelectorAll('.lang-toggle-btn').forEach(btn => {
            btn.onclick = function (e) {
                e.preventDefault();
                const lang = this.getAttribute('data-lang');
                if (lang) window.switchLanguage(lang);
            };
        });

        // Initialize prediction form if present
        if (document.getElementById('disease-prediction-form')) {
            window.initPredictionForm();
        }

        // Initialize history filters if present
        if (document.getElementById('historyTableBody')) {
            window.initHistoryFilters();
        }

        console.log(`🌾 Rythu Mithra Premium SaaS UI Initialized [Lang: ${currentLang}]`);
    });

})();
