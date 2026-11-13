"""
Centralized Multilingual Translation Loader for Python / Jinja2 Templates.
Provides backend translation parity with static/js/translations.js.
Supports English ('en') and Telugu ('te').
"""

import os
import json
import logging

logger = logging.getLogger(__name__)

# Direct in-memory dictionary for maximum speed and zero file-I/O overhead
try:
    from utils.translations_data import TRANSLATIONS
except ImportError:
    try:
        from translations_data import TRANSLATIONS
    except ImportError:
        TRANSLATIONS = {'en': {}, 'te': {}}


def get_translation(key, lang='te', fallback=None):
    """
    Retrieves translation for key in target language ('te' or 'en').
    Falls back to English if not found, then to fallback or key itself.
    """
    lang = str(lang or 'te').lower().strip()
    if lang not in ['te', 'en']:
        lang = 'te'

    lang_dict = TRANSLATIONS.get(lang, {})
    if key in lang_dict and lang_dict[key]:
        return lang_dict[key]

    # Fallback to English
    en_dict = TRANSLATIONS.get('en', {})
    if key in en_dict and en_dict[key]:
        return en_dict[key]

    return fallback if fallback is not None else key


def get_all_translations():
    """Returns the full translations dictionary."""
    return TRANSLATIONS
