"""
Model Loaders for Rythu Mithra.
Handles loading, preprocessing, and inference for:
1. TensorFlow/Keras Crop Disease & Pest Classification Model
2. Multilingual XLM-RoBERTa Advisory NLP Model

IMPORTANT:
This loader expects real trained model weights placed in `models/checkpoints/`.
No fake or placeholder weights are generated. If weights are missing,
graceful diagnostics are provided without crashing the application.
"""

import os
import json
import logging
import io

try:
    import numpy as np
except ImportError:
    np = None

try:
    from PIL import Image
except ImportError:
    Image = None

logger = logging.getLogger(__name__)


class ModelNotReadyError(Exception):
    """Raised when an inference request is made before trained weights are provided."""
    pass


class CropDiseaseModelLoader:
    """
    Singleton loader for the TensorFlow/Keras Crop Disease Classification model.
    Loads actual .keras or .h5 models from disk and performs image preprocessing.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(CropDiseaseModelLoader, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, model_path=None, metadata_path=None, target_size=(224, 224)):
        if getattr(self, '_initialized', False):
            return

        self.model_path = model_path
        self.metadata_path = metadata_path
        self.target_size = target_size
        self.model = None
        self.classes = []
        self.metadata = {}
        self.is_loaded = False
        self.load_error = None

        self._load_metadata()
        self._load_model()
        self._initialized = True

    def _load_metadata(self):
        """Loads disease classes and remediation metadata from JSON."""
        if self.metadata_path and os.path.exists(self.metadata_path):
            try:
                with open(self.metadata_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.classes = data.get('classes', [])
                    self.metadata = data.get('metadata', {})
                logger.info(f"Loaded {len(self.classes)} disease classes from metadata.")
            except Exception as e:
                logger.error(f"Failed to load disease metadata: {e}")
                self.classes = []
                self.metadata = {}
        else:
            logger.warning(f"Metadata file not found at: {self.metadata_path}")

    def _load_model(self):
        """
        Loads the trained TensorFlow/Keras model if present on disk.
        Does NOT generate fake models.
        """
        if not self.model_path or not os.path.exists(self.model_path):
            self.is_loaded = False
            self.load_error = (
                f"Trained model file not found at '{self.model_path}'. "
                f"Please place your trained .keras or .h5 file in models/checkpoints/."
            )
            logger.warning(self.load_error)
            return

        try:
            # Lazy import TensorFlow so app startup is fast and non-blocking
            import tensorflow as tf
            logger.info(f"Loading TensorFlow model from: {self.model_path}")
            self.model = tf.keras.models.load_model(self.model_path)
            self.is_loaded = True
            self.load_error = None
            logger.info("TensorFlow crop disease model loaded successfully.")
        except Exception as e:
            self.is_loaded = False
            self.load_error = f"Error loading model from '{self.model_path}': {str(e)}"
            logger.error(self.load_error)

    def preprocess_image(self, image_input):
        """
        Preprocesses an image for TensorFlow model inference.
        Accepts:
            - bytes: Raw image bytes from uploaded file
            - PIL.Image: Image object
            - str: Path to image file
        Returns:
            - numpy.ndarray of shape (1, height, width, 3), scaled to [0, 1]
        """
        try:
            if isinstance(image_input, bytes):
                img = Image.open(io.BytesIO(image_input))
            elif isinstance(image_input, str):
                img = Image.open(image_input)
            elif isinstance(image_input, Image.Image):
                img = image_input
            else:
                raise ValueError("Unsupported image input type.")

            # Ensure 3-channel RGB format (strips alpha channel if PNG)
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Resize to the model's expected input dimension
            img = img.resize(self.target_size, Image.Resampling.BILINEAR)

            # Convert to numpy array and normalize to [0, 1]
            img_array = np.array(img, dtype=np.float32) / 255.0

            # Add batch dimension: (224, 224, 3) -> (1, 224, 224, 3)
            img_tensor = np.expand_dims(img_array, axis=0)
            return img_tensor
        except Exception as e:
            logger.error(f"Image preprocessing failed: {e}")
            raise ValueError(f"Invalid image format or preprocessing failed: {str(e)}")

    def predict(self, preprocessed_image):
        """
        Runs inference on the preprocessed image tensor.
        Returns:
            - predicted_class: str
            - confidence: float (0.0 to 1.0)
            - all_probabilities: dict mapping class name to confidence score
        """
        if not self.is_loaded or self.model is None:
            raise ModelNotReadyError(
                self.load_error or "Crop disease model is not loaded. Add trained weights to models/checkpoints/."
            )

        # Run model inference
        predictions = self.model.predict(preprocessed_image)
        probabilities = predictions[0]

        top_index = int(np.argmax(probabilities))
        confidence = float(probabilities[top_index])

        predicted_class = self.classes[top_index] if top_index < len(self.classes) else f"Class_{top_index}"

        all_probs = {}
        for idx, prob in enumerate(probabilities):
            cls_name = self.classes[idx] if idx < len(self.classes) else f"Class_{idx}"
            all_probs[cls_name] = round(float(prob), 4)

        return predicted_class, confidence, all_probs


class XlmRobertaAdvisoryLoader:
    """
    Singleton loader for the multilingual XLM-RoBERTa agricultural advisory model.
    Loads real tokenizer and weights from Hugging Face model checkpoint directory.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(XlmRobertaAdvisoryLoader, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, model_dir=None):
        if getattr(self, '_initialized', False):
            return

        self.model_dir = model_dir
        self.tokenizer = None
        self.model = None
        self.is_loaded = False
        self.load_error = None

        self._load_model()
        self._initialized = True

    def _load_model(self):
        """Loads XLM-RoBERTa tokenizer and PyTorch model if checkpoint exists on disk."""
        if not self.model_dir or not os.path.exists(self.model_dir):
            self.is_loaded = False
            self.load_error = (
                f"XLM-RoBERTa checkpoint directory not found at '{self.model_dir}'. "
                f"Please place your trained checkpoint folder in models/checkpoints/xlm_roberta/."
            )
            logger.warning(self.load_error)
            return

        try:
            from transformers import AutoTokenizer, AutoModelForSequenceClassification
            import torch

            logger.info(f"Loading XLM-RoBERTa model from: {self.model_dir}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_dir)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_dir)
            self.model.eval()

            self.is_loaded = True
            self.load_error = None
            logger.info("XLM-RoBERTa advisory model loaded successfully.")
        except Exception as e:
            self.is_loaded = False
            self.load_error = f"Error loading XLM-RoBERTa model: {str(e)}"
            logger.error(self.load_error)

    def predict_intent_or_response(self, text):
        """
        Encodes query with XLM-RoBERTa tokenizer and computes model logits.
        """
        if not self.is_loaded or self.model is None:
            raise ModelNotReadyError(
                self.load_error or "XLM-RoBERTa model is not loaded. Add checkpoints to models/checkpoints/xlm_roberta/."
            )

        import torch
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=128,
            padding=True
        )

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probabilities = torch.softmax(logits, dim=1).squeeze().tolist()

        if isinstance(probabilities, float):
            probabilities = [probabilities]

        pred_idx = int(np.argmax(probabilities))
        confidence = float(probabilities[pred_idx])
        return pred_idx, confidence, probabilities
