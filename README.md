# Rythu Mithra (రైతు మిత్ర)
### AI-Based Multilingual Crop Disease & Pest Detection and Agricultural Advisory System

A professional, modular, and scalable multi-modal agricultural decision support system designed as a final-year engineering capstone project.

---

## 🌾 1. Project Overview

**Rythu Mithra** empowers farmers with accessible, localized, and instant agronomic intelligence:
- **Visual Crop Disease & Pest Diagnosis**: Farmers capture or upload photos of diseased plant foliage (e.g. Rice, Cotton, Tomato, Potato, Maize). A deep learning convolutional neural network identifies the pathogen, estimates severity, and yields immediate organic and chemical remedies.
- **Multilingual Voice & Text Advisory**: Farmers can ask agricultural questions in their native language (**Telugu `te-IN`**, **Hindi `hi-IN`**, and **Indian English `en-IN`**). Voice input is transcribed in real-time via the browser's Web Speech API and processed using a multilingual cross-lingual language model (XLM-RoBERTa) backed by an extensive agricultural knowledge base.
- **Voice Response (Text-to-Speech)**: Advisory answers can be read aloud to farmers directly in the web browser.
- **Persistent Diagnostics History**: All detection records, uploaded crop images, and advisory interactions are cataloged in an SQLite database.

---

## 🛠️ 2. Technology Stack

| Layer | Technologies Used | Purpose |
|---|---|---|
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5, Bootstrap Icons | Responsive UI, mobile accessibility, drag-and-drop file upload |
| **Voice Input & TTS** | Web Speech API (`SpeechRecognition` & `SpeechSynthesis`) | Native in-browser speech-to-text in Telugu, Hindi, English |
| **Backend** | Python Flask, Werkzeug | Reusable application factory, Blueprints, REST APIs |
| **Database** | SQLite, Flask-SQLAlchemy | Lightweight, self-contained persistence of queries and diagnoses |
| **Computer Vision** | TensorFlow / Keras | Image preprocessing and leaf disease classification |
| **Multilingual NLP** | Hugging Face Transformers (`XLM-RoBERTa`), PyTorch | Multilingual query representation and advisory mapping |
| **Testing** | Pytest, Flask Test Client | Unit tests for routes, validation, and services |

---

## 📁 3. Project Folder Structure

```text
Rythu_Mithra/
├── app.py                      # Flask Application Factory and main entry point
├── config.py                   # Environment-specific configuration classes
├── requirements.txt            # Project dependencies and version pins
├── README.md                   # Installation, model setup, and user manual
│
├── database/                   # SQLite database models and setup
│   ├── __init__.py             # SQLAlchemy instance and init_db hook
│   ├── models.py               # DiseaseDetectionRecord & AdvisoryQueryRecord models
│   └── init_db.py              # Standalone DB schema creation script
│
├── models/                     # Deep learning & NLP model loader layer
│   ├── __init__.py             # Models package initialization
│   ├── model_loader.py         # TensorFlow & XLM-RoBERTa singleton loaders & preprocessors
│   ├── disease_metadata.json   # Multilingual symptoms & remedies catalog for 9 crop classes
│   └── checkpoints/            # Directory reserved for real trained model files
│       ├── .gitkeep
│       └── README.md           # Instructions on how to export and place model weights
│
├── data/                       # Datasets, corpora, and sample queries
│   ├── sample_queries.json     # Multilingual benchmark prompts (Telugu, Hindi, English)
│   └── README.md               # Guidelines for placing notebooks and datasets safely
│
├── services/                   # Business logic layer (decoupled from routes)
│   ├── __init__.py
│   ├── disease_service.py      # Image validation, preprocessing, inference & DB storage
│   ├── advisory_service.py     # Multilingual query handling, NLP inference & fallback rules
│   └── history_service.py      # History queries and dashboard analytics summary
│
├── routes/                     # Reusable Flask Blueprints (HTTP & JSON API)
│   ├── __init__.py             # Blueprint exports
│   ├── main_routes.py          # Dashboard (/), History (/history), and About (/about)
│   ├── disease_routes.py       # Disease detection UI & /api/disease/predict endpoint
│   └── advisory_routes.py      # Advisory UI & /api/advisory/query endpoint
│
├── utils/                      # Helper utilities
│   ├── __init__.py
│   ├── file_handler.py         # Secure file saving, extension checking & PIL validation
│   ├── logger.py               # Centralized logging configuration
│   └── constants.py            # Supported languages, speech tags, and severity levels
│
├── templates/                  # Jinja2 HTML templates styled with Bootstrap 5
│   ├── base.html               # Shared layout (navbar, footer, responsive grid)
│   ├── index.html              # Main dashboard with statistics and quick actions
│   ├── disease_detect.html     # Drag-and-drop image upload and diagnostic report UI
│   ├── advisory.html           # Voice microphone interface and multilingual advisory chat
│   ├── history.html            # Tabular view of past diagnoses and voice queries
│   ├── about.html              # Technical specifications and architecture
│   └── error.html              # Friendly error display (400, 404, 500)
│
├── static/                     # Client-side static assets
│   ├── css/
│   │   └── style.css           # Custom styling, animations, and agricultural theme
│   ├── js/
│   │   ├── main.js             # General UI initialization and tooltips
│   │   ├── speech.js           # Web Speech API voice capture, TTS & advisory AJAX handler
│   │   └── disease_detect.js   # Drag-and-drop preview, AJAX image submission & renderer
│   ├── images/
│   │   └── .gitkeep            # Static logos and reference imagery
│   └── uploads/
│       └── .gitkeep            # Uploaded crop leaves for diagnosis (auto-created)
│
└── tests/                      # Automated test suite
    ├── __init__.py
    ├── test_routes.py          # Flask test client route & API integration tests
    └── test_services.py        # Unit tests for loaders, speech mappings, and file handlers
```

---

## 📄 4. Detailed Explanation of Every File

1. **`app.py`**:
   The core entry point utilizing the Application Factory pattern (`create_app()`). Configures error handlers, injects global template variables (e.g. supported languages), auto-initializes the SQLite database tables on startup, and registers the three blueprints.
2. **`config.py`**:
   Centralizes environment configurations into `DevelopmentConfig`, `ProductionConfig`, and `TestingConfig`. Specifies upload path (`static/uploads`), database URI (`sqlite:///database/rythu_mithra.db`), maximum file upload size (16MB), and model checkpoint paths.
3. **`requirements.txt`**:
   Pins all necessary Python dependencies (Flask, Flask-SQLAlchemy, TensorFlow, Transformers, Torch, SentencePiece, Pillow, Pytest).
4. **`database/__init__.py` & `database/models.py`**:
   Manages the SQLAlchemy instance. Contains `DiseaseDetectionRecord` (stores uploaded filename, detected crop, disease, confidence, symptoms, and remedies) and `AdvisoryQueryRecord` (stores user question, language, voice/text mode, and response).
5. **`database/init_db.py`**:
   CLI script to initialize or reset database tables (`python database/init_db.py`).
6. **`models/model_loader.py`**:
   Provides decoupled loaders without generating fake weights:
   - `CropDiseaseModelLoader`: Singleton that loads the TensorFlow/Keras model from disk, performs authentic image preprocessing (RGB conversion, resizing to 224x224, normalization to `[0, 1]`, batch dimension expansion), and runs prediction. If the model file is not yet placed, it returns structured status without crashing.
   - `XlmRobertaAdvisoryLoader`: Singleton that loads the Hugging Face XLM-RoBERTa tokenizer and PyTorch model weights from `models/checkpoints/xlm_roberta/`.
7. **`models/disease_metadata.json`**:
   Accurate agronomic knowledge base covering 9 classes (Rice Blast, Rice Brown Spot, Cotton Leaf Curl, Cotton Bacterial Blight, Tomato Early Blight, Tomato Late Blight, Potato Late Blight, Maize Common Rust, Healthy Crop) with trilingual symptoms, organic controls, and chemical treatments with exact dosages.
8. **`models/checkpoints/README.md`**:
   Step-by-step instructions for exporting model weights from your training notebook into this directory.
9. **`services/disease_service.py`**:
   Decoupled service that saves the uploaded leaf photo, invokes `CropDiseaseModelLoader`, retrieves disease metadata, commits the diagnosis to SQLite, and returns a JSON-serializable dictionary.
10. **`services/advisory_service.py`**:
    Handles queries across Telugu, Hindi, and English. Evaluates queries with XLM-RoBERTa when checkpoints are mounted and leverages an extensive agricultural domain knowledge base so farmers receive verified advice even before NLP weights are placed.
11. **`services/history_service.py`**:
    Retrieves recent detections and queries, computing summary counts for the dashboard.
12. **`routes/main_routes.py`**:
    Renders the Dashboard (`/`), History (`/history`), and About (`/about`) templates.
13. **`routes/disease_routes.py`**:
    Renders the Disease Detection interface (`/disease-detect`) and provides the multipart form upload API endpoint (`/api/disease/predict`).
14. **`routes/advisory_routes.py`**:
    Renders the Advisory interface (`/advisory`), provides the advisory query API (`/api/advisory/query`), and serves sample queries (`/api/advisory/samples`).
15. **`utils/file_handler.py`**:
    Protects the system against malicious uploads by validating file extensions, verifying file integrity with Pillow, and generating unique collision-free filenames (`crop_YYYYMMDD_HHMMSS_<uuid>.<ext>`).
16. **`utils/constants.py` & `utils/logger.py`**:
    Stores language codes, Web Speech tags (`te-IN`, `hi-IN`, `en-IN`), severity scales, and standardized logging.
17. **`templates/`**:
    Bootstrap 5 Jinja2 templates providing responsive layouts, drag-and-drop zones, voice animation feedback, and diagnostic cards.
18. **`static/js/speech.js`**:
    Integrates the browser's native Web Speech API for voice recognition in Telugu, Hindi, and English, provides visual microphone pulsing animations, and powers Text-to-Speech (TTS) response playback.
19. **`static/js/disease_detect.js`**:
    Handles drag-and-drop image uploads, live file preview, client-side validation, AJAX POST submission, and UI result rendering.
20. **`tests/test_routes.py` & `tests/test_services.py`**:
    Automated integration tests validating HTTP routes, API contracts, image validator edge cases, and graceful handling of missing model checkpoints.

---

## 🚀 5. Installation & Execution Guide

### Step 1: Create and Activate a Python Virtual Environment

```bash
# Navigate to the project root directory
cd Rythu_Mithra

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# (Or Windows Command Prompt)
.\venv\Scripts\activate.bat

# (Or Linux / macOS)
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> **Note on TensorFlow & PyTorch**: Ensure your Python version is 3.10 or 3.11 for optimal compatibility with TensorFlow 2.15+ and PyTorch.

---

### Step 3: Initialize the SQLite Database

Run the database setup script to create all required tables:

```bash
python database/init_db.py
```

Output:
```text
[*] Initializing database at: ...\database\rythu_mithra.db
[+] Database tables initialized successfully:
    - disease_detections
    - advisory_queries
```

---

### Step 4: Placing Your Trained Machine Learning Models

> **Important**: The application starts cleanly and runs even before model weights are added. Once your models are trained, place them into `models/checkpoints/` as follows:

#### 1. TensorFlow / Keras Crop Disease Model:
Copy your trained model file into:
```text
models/checkpoints/crop_disease_model.keras
```
*(If your file is named `model.h5`, update `CROP_DISEASE_MODEL_PATH` in `config.py` or set the environment variable).*

#### 2. Fine-Tuned XLM-RoBERTa Advisory Model:
Save your fine-tuned Hugging Face checkpoint directory into:
```text
models/checkpoints/xlm_roberta/
```
Ensure it contains `config.json`, `tokenizer.json` / `sentencepiece.bpe.model`, and `model.safetensors`.

---

### Step 5: Run the Flask Application

```bash
python app.py
```

The terminal will display:
```text
============================================================
  🌾 Rythu Mithra (రైతు మిత్ర) Server Starting...
  🌾 Listening on http://localhost:5000
============================================================
```

Open your browser and navigate to:
```text
http://127.0.0.1:5000
```

---

## 🎙️ 6. Using Voice Input (Web Speech API)

1. Open **Google Chrome** or **Microsoft Edge** (browsers that natively support the Web Speech API).
2. Navigate to the **Multilingual Advisory** page (`/advisory`).
3. Select your preferred language:
   - **Telugu (`తెలుగు`)** -> Speech Recognition Code: `te-IN`
   - **Hindi (`हिन्दी`)** -> Speech Recognition Code: `hi-IN`
   - **English** -> Speech Recognition Code: `en-IN`
4. Click the **Red Microphone Icon** and allow microphone access when prompted by the browser.
5. Speak your farming query clearly (e.g., *"వరి పంటలో అగ్గి తెగులు నివారణ ఏమిటి?"*).
6. The speech is transcribed into the query field in real time.
7. Click **"Get Advisory"** (or speech recognition will auto-submit when you finish speaking).
8. Click **"Read Aloud"** to listen to the advice using Text-to-Speech!

---

## 🧪 7. Running Automated Tests

Run the full automated test suite using `pytest`:

```bash
pytest
```

To run with verbose output:
```bash
pytest -v
```

All route responses, API payload validations, multilingual fallbacks, and missing-model handlers will be verified.

---

## 🛡️ Project Principles Followed
- **No data loss**: Existing datasets and notebooks are protected.
- **No fake models**: Clean abstraction layers handle real weights and missing weights gracefully without synthetic predictions.
- **Separation of concerns**: Presentation (HTML/CSS/JS), Business Services (`services/`), and ML Logic (`models/`) are strictly separated.
- **Reusable architecture**: Flask Blueprints and services allow plug-and-play extension to mobile apps (Flutter/React Native) or cloud deployments (GCP / AWS).
