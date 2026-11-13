# Model Checkpoints Directory

This directory is designated for your trained machine learning model weights.

## 1. TensorFlow / Keras Crop Disease Model
Place your trained deep learning model file here:
- **Expected File Path**: `models/checkpoints/crop_disease_model.keras` (or update `CROP_DISEASE_MODEL_PATH` in `config.py` if using `.h5`)
- **Input Dimensions**: `(224, 224, 3)` RGB, normalized to `[0, 1]`.
- **Output Classes**: Maps to the classes defined in `models/disease_metadata.json`:
  1. `Rice_Blast`
  2. `Rice_Brown_Spot`
  3. `Cotton_Leaf_Curl`
  4. `Cotton_Bacterial_Blight`
  5. `Tomato_Early_Blight`
  6. `Tomato_Late_Blight`
  7. `Potato_Late_Blight`
  8. `Maize_Common_Rust`
  9. `Healthy_Crop`

### Exporting from your Training Notebook:
```python
# In your training Jupyter notebook:
model.save("models/checkpoints/crop_disease_model.keras")
```

---

## 2. Multilingual XLM-RoBERTa Advisory Model
Place your fine-tuned Hugging Face XLM-RoBERTa model checkpoint folder here:
- **Expected Directory Path**: `models/checkpoints/xlm_roberta/`
- **Required Files in this folder**:
  - `config.json`
  - `tokenizer_config.json`
  - `sentencepiece.bpe.model` (or `tokenizer.json`)
  - `model.safetensors` (or `pytorch_model.bin`)
  - `special_tokens_map.json`

### Exporting from your Training Notebook:
```python
# In your NLP training notebook:
model.save_pretrained("models/checkpoints/xlm_roberta/")
tokenizer.save_pretrained("models/checkpoints/xlm_roberta/")
```

---
*Note: The application will start cleanly even if models are not yet placed. When models are missing, clear diagnostics will be shown in the UI without crashing the server.*
