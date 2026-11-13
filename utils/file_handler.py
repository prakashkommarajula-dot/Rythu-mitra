"""
File Handling and Validation Utilities for Rythu Mithra.
Handles safe saving, extension checking, and image dimension validation.
"""

import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from PIL import Image


def allowed_file(filename, allowed_extensions):
    """Check if file has an allowed image extension."""
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in allowed_extensions


def save_uploaded_image(file_storage, upload_folder, allowed_extensions=None):
    """
    Validates, renames, and safely saves an uploaded image file.
    Returns:
        tuple: (unique_filename, absolute_file_path)
    Raises:
        ValueError: If file is invalid or not an image.
    """
    if allowed_extensions is None:
        allowed_extensions = {'png', 'jpg', 'jpeg', 'webp'}

    if not file_storage or file_storage.filename == '':
        raise ValueError("No file provided for upload.")

    original_filename = secure_filename(file_storage.filename)
    if not allowed_file(original_filename, allowed_extensions):
        raise ValueError(
            f"Invalid file type. Allowed formats: {', '.join(allowed_extensions)}"
        )

    # Validate image data integrity using PIL
    try:
        image = Image.open(file_storage.stream)
        image.verify()  # Verify file is not corrupted
        # Reset stream pointer after verify
        file_storage.stream.seek(0)
    except Exception as e:
        raise ValueError(f"Uploaded file is not a valid or readable image: {str(e)}")

    # Generate unique timestamped filename to prevent collisions
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    random_token = uuid.uuid4().hex[:8]
    ext = original_filename.rsplit('.', 1)[1].lower()
    unique_filename = f"crop_{timestamp}_{random_token}.{ext}"

    os.makedirs(upload_folder, exist_ok=True)
    destination_path = os.path.join(upload_folder, unique_filename)

    file_storage.save(destination_path)
    return unique_filename, destination_path
