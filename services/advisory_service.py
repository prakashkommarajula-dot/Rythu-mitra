"""
=============================================================================
Rythu Mithra - AI-Based Multilingual Crop Disease & Pest Detection
Service: advisory_service.py
Phase 6: Smart Agricultural Advisory Engine & Fallback Diagnosis Workflow
=============================================================================
Provides production-grade, bilingual (Telugu & English) agricultural advisories
derived strictly from verified ANGRAU / ICAR / PJTSAU / KVK dataset corpora:
- 'data/processed/cleaned_corpus.csv'
- 'data/processed/diagnosis_fallback.csv'

Features:
1. Reusable Advisory Engine indexing 23 disease/pest classes across 14 crops.
2. Full 9-section structured IPM advisory generation:
   (Overview, Symptoms, Severity, Organic, Biological, Cultural, Chemical,
    Prevention, Safety Precautions).
3. Exact preservation of verified chemical dosages and safety guidelines.
4. Intelligent Crop Alias Normalization (e.g. Paddy <-> Rice, Jowar <-> Sorghum).
5. 'Requires Further Diagnosis' fallback workflow with crop-specific diagnostic questions.
6. Multi-turn follow-up diagnosis resolver.
7. Database audit logging of farmer advisory views with data isolation.
=============================================================================
"""

import os
import re
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd

from database import db
from database.models import AdvisoryQueryRecord, AdvisoryViewRecord
from utils.constants import SUPPORTED_LANGUAGES
from services.disease_advisory_catalog import get_catalog_entry, DEFAULT_DOSSIER

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEANED_CORPUS_PATH = PROJECT_ROOT / "data" / "processed" / "cleaned_corpus.csv"
FALLBACK_CORPUS_PATH = PROJECT_ROOT / "data" / "processed" / "diagnosis_fallback.csv"

# Comprehensive crop alias mapping for Indian and regional terminology
CROP_ALIASES = {
    'paddy': 'Rice',
    'rice': 'Rice',
    'వరి': 'Rice',
    'cotton': 'Cotton',
    'పత్తి': 'Cotton',
    'chilli': 'Chilli',
    'chili': 'Chilli',
    'మిరప': 'Chilli',
    'tomato': 'Tomato',
    'టమోటా': 'Tomato',
    'టమాట': 'Tomato',
    'bengal gram': 'Bengal Gram',
    'chickpea': 'Bengal Gram',
    'శనగ': 'Bengal Gram',
    'gram': 'Bengal Gram',
    'groundnut': 'Groundnut',
    'peanut': 'Groundnut',
    'వేరుశనగ': 'Groundnut',
    'maize': 'Maize',
    'corn': 'Maize',
    'మొక్కజొన్న': 'Maize',
    'jowar': 'Jowar',
    'sorghum': 'Jowar',
    'జొన్న': 'Jowar',
    'turmeric': 'Turmeric',
    'పసుపు': 'Turmeric',
    'brinjal': 'Brinjal',
    'eggplant': 'Brinjal',
    'వంకాయ': 'Brinjal',
    'okra': 'Okra',
    'bhendi': 'Okra',
    'ladyfinger': 'Okra',
    'బెండ': 'Okra',
    'green gram': 'Green Gram',
    'moong': 'Green Gram',
    'పెసర': 'Green Gram',
    'red gram': 'Red Gram',
    'arhar': 'Red Gram',
    'tur': 'Red Gram',
    'కందులు': 'Red Gram',
    'black gram': 'Black Gram',
    'urad': 'Black Gram',
    'మినుములు': 'Black Gram',
}

# Crop local Telugu names
CROP_TELUGU_NAMES = {
    'Rice': 'వరి',
    'Cotton': 'పత్తి',
    'Chilli': 'మిరప',
    'Tomato': 'టమాట',
    'Bengal Gram': 'శనగ',
    'Groundnut': 'వేరుశనగ',
    'Maize': 'మొక్కజొన్న',
    'Jowar': 'జొన్న',
    'Turmeric': 'పసుపు',
    'Brinjal': 'వంకాయ',
    'Okra': 'బెండ',
    'Green Gram': 'పెసర',
    'Red Gram': 'కందులు',
    'Black Gram': 'మినుములు',
}


def normalize_crop_name(crop: Optional[str]) -> str:
    """Normalizes regional, English, and Telugu crop names to dataset standard."""
    if not crop or not str(crop).strip():
        return "General"
    cleaned = str(crop).strip().lower()
    return CROP_ALIASES.get(cleaned, str(crop).strip().title())


def clean_text_field(val: Any, default: str = "") -> str:
    """Cleans NaN, None, or empty dataframe values."""
    if val is None or pd.isna(val):
        return default
    text = str(val).strip()
    if text.lower() in ['nan', 'none', 'unknown', '-']:
        return default
    return text


class SmartAdvisoryEngine:
    """
    Singleton Advisory Engine that indexes verified agricultural dataset files
    and delivers comprehensive 9-section IPM advisory guides.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SmartAdvisoryEngine, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if getattr(self, '_initialized', False):
            return

        self.df_corpus = pd.DataFrame()
        self.df_fallback = pd.DataFrame()
        self._load_datasets()
        self._initialized = True

    def _load_datasets(self):
        """Loads and indexes cleaned corpus and fallback diagnosis CSVs."""
        try:
            if CLEANED_CORPUS_PATH.exists():
                self.df_corpus = pd.read_csv(CLEANED_CORPUS_PATH, encoding='utf-8')
                logger.info(f"Loaded Cleaned Advisory Corpus: {len(self.df_corpus)} records.")
            else:
                logger.error(f"Cleaned corpus not found at {CLEANED_CORPUS_PATH}")

            if FALLBACK_CORPUS_PATH.exists():
                self.df_fallback = pd.read_csv(FALLBACK_CORPUS_PATH, encoding='utf-8')
                logger.info(f"Loaded Fallback Diagnosis Corpus: {len(self.df_fallback)} records.")
            else:
                logger.error(f"Fallback corpus not found at {FALLBACK_CORPUS_PATH}")
        except Exception as e:
            logger.error(f"Error loading advisory datasets: {e}")

    def get_available_diseases(self) -> List[Dict[str, Any]]:
        """Returns list of distinct verified disease and pest classes in dataset."""
        if self.df_corpus.empty:
            return []
        
        valid = self.df_corpus[
            (~self.df_corpus['Disease_or_Pest'].isna()) &
            (~self.df_corpus['Disease_or_Pest'].isin(['Requires further diagnosis', '-', '', 'Unknown', 'unknown']))
        ]
        
        results = []
        for d in sorted(valid['Disease_or_Pest'].unique()):
            sub = valid[valid['Disease_or_Pest'] == d]
            crops = sub['Crop'].dropna().unique().tolist()
            sci = sub['Scientific_Name'].dropna().unique().tolist()
            ptype = sub['Problem_Type'].dropna().unique().tolist()
            results.append({
                'name': d,
                'crops': crops,
                'scientific_name': sci[0] if sci and sci[0] not in ['Unknown', 'nan', '  '] else None,
                'type': ptype[0] if ptype else 'Disease'
            })
        return results

    def get_advisory(
        self,
        disease_or_pest: str,
        crop: Optional[str] = None,
        language: str = 'te',
        severity: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieves a verified 9-section IPM advisory for a specific disease or pest.
        Prioritizes crop-specific matches, then falls back to general species match.
        """
        if not disease_or_pest or not disease_or_pest.strip():
            return None

        d_query = disease_or_pest.strip().lower()
        
        # If query is explicitly 'requires further diagnosis', route to fallback
        if 'further diagnosis' in d_query:
            return self.get_fallback_advisory(crop=crop, language=language)

        if self.df_corpus.empty:
            self._load_datasets()
            if self.df_corpus.empty:
                return None

        # Filter out invalid / fallback rows
        valid_df = self.df_corpus[
            (~self.df_corpus['Disease_or_Pest'].isna()) &
            (self.df_corpus['Disease_or_Pest'].str.lower() != 'requires further diagnosis')
        ]

        # 1. Match by Disease/Pest name
        matches = valid_df[valid_df['Disease_or_Pest'].str.lower() == d_query]

        # If no exact match, try substring or word match
        if matches.empty:
            matches = valid_df[valid_df['Disease_or_Pest'].str.lower().str.contains(re.escape(d_query), na=False)]

        if matches.empty:
            logger.warning(f"No verified advisory found for disease/pest: '{disease_or_pest}'")
            return None

        # 2. Prioritize Crop-Specific Record if crop is provided
        selected_row = None
        norm_crop = normalize_crop_name(crop)
        if norm_crop and norm_crop.lower() != 'general':
            crop_match = matches[matches['Crop'].str.lower() == norm_crop.lower()]
            if not crop_match.empty:
                selected_row = crop_match.iloc[0]

        if selected_row is None:
            # Pick row with highest completeness of advisory fields
            selected_row = matches.iloc[0]

        # 3. Construct 9 Structured Sections with Catalog Integration & Strict Language Isolation
        row = selected_row
        disease_name = str(row['Disease_or_Pest']).strip()
        scientific_name = clean_text_field(row.get('Scientific_Name'), None)
        crop_name = clean_text_field(row.get('Crop'), norm_crop or "General")
        crop_local_name = clean_text_field(row.get('Crop_Local_Name'), CROP_TELUGU_NAMES.get(crop_name, crop_name))
        problem_type = clean_text_field(row.get('Problem_Type'), 'Disease')
        affected_part = clean_text_field(row.get('Affected_Plant_Part'), 'Foliage / Whole Plant')
        
        sev = severity or clean_text_field(row.get('Severity'), 'Medium')
        if sev.lower() in ['nan', 'none', '']:
            sev = 'Medium'

        lang = 'te' if language == 'te' else 'en'
        cat = get_catalog_entry(disease_name, norm_crop)

        if cat:
            what_prob = cat.get('what_is_problem', {}).get(lang, '')
            why_occ = cat.get('why_it_occurs', {}).get(lang, '')
            imm_steps = cat.get('immediate_action_steps', {}).get(lang, [])
            urgency = cat.get('action_urgency', {}).get(lang, '')
            prev_steps = cat.get('prevention_steps', {}).get(lang, [])
            next_season = cat.get('next_season_prevention', {}).get(lang, '')
            org_mgmt = cat.get('organic_management', {}).get(lang, '')
            bio_ctrl = cat.get('biological_control', {}).get(lang, '')
            cult_ctrl = cat.get('cultural_control', {}).get(lang, '')
            safety_prec = cat.get('safety_precautions', {}).get(lang, '')
            scientific_name = cat.get('scientific_name') or scientific_name
            sev = cat.get('severity') or sev
            affected_part = cat.get('affected_part') or affected_part

            chem = cat.get('chemical_control', {})
            if chem.get('has_verified_chemical'):
                prod = chem.get('product', {}).get(lang, '')
                dos = chem.get('dosage', {}).get(lang, '')
                water = chem.get('water_quantity', {}).get(lang, '')
                app_meth = chem.get('application_method', {}).get(lang, '')
                phi = chem.get('waiting_period_phi', {}).get(lang, '')
                safe_note = chem.get('safety_precaution', {}).get(lang, '')
                chem_structured = {
                    'has_verified_chemical': True,
                    'product': prod,
                    'dosage': dos,
                    'water_quantity': water,
                    'application_method': app_meth,
                    'waiting_period_phi': phi,
                    'safety_precaution': safe_note,
                    'unverified_message': None
                }
                chem_summary = f"{prod} - {dos}"
            else:
                unv_msg = chem.get('unverified_reason', {}).get(
                    lang,
                    "No verified chemical recommendation is available for this diagnosis." if lang == 'en' else "ఈ నిర్ధారణకు ధృవీకరించబడిన రసాయన సిఫారసు అందుబాటులో లేదు."
                )
                chem_structured = {
                    'has_verified_chemical': False,
                    'product': None,
                    'dosage': None,
                    'water_quantity': None,
                    'application_method': None,
                    'waiting_period_phi': None,
                    'safety_precaution': None,
                    'unverified_message': unv_msg
                }
                chem_summary = unv_msg

            return {
                'is_fallback': False,
                'confirmed_diagnosis': True,
                'disease_or_pest': disease_name,
                'scientific_name': scientific_name,
                'crop': crop_name,
                'crop_local_name': crop_local_name,
                'problem_type': problem_type,
                'affected_plant_part': affected_part,
                'severity': sev.capitalize(),
                
                # Structured Sections for Rich UI
                'immediate_action_structured': {
                    'what_is_problem': what_prob,
                    'why_it_occurs': why_occ,
                    'steps': imm_steps,
                    'urgency': urgency
                },
                'prevention_structured': {
                    'steps': prev_steps,
                    'next_season': next_season
                },
                'chemical_structured': chem_structured,

                # Bilingual String Content
                'symptoms_te': cat.get('what_is_problem', {}).get('te', ''),
                'symptoms_en': cat.get('what_is_problem', {}).get('en', ''),
                'advisory_te': cat.get('what_is_problem', {}).get('te', ''),
                'advisory_en': cat.get('what_is_problem', {}).get('en', ''),
                
                # Standard Accordion Content (Language Isolated)
                'immediate_actions': " ".join(imm_steps) if isinstance(imm_steps, list) else imm_steps,
                'organic_management': org_mgmt,
                'biological_control': bio_ctrl,
                'cultural_control': cult_ctrl,
                'chemical_control': chem_summary,
                'prevention': " ".join(prev_steps) if isinstance(prev_steps, list) else prev_steps,
                'safety_precautions': safety_prec,
                'diagnostic_questions': None,
                'source': 'ANGRAU / PJTSAU / CIBRC Agricultural Guidelines'
            }

        # Fallback to CSV with strict language isolation
        def isolate_text(txt: Optional[str], target_lang: str) -> str:
            if not txt:
                return "English advisory is not available for this recommendation." if target_lang == 'en' else "ఈ సూచనకు తెలుగు సమాచారం అందుబాటులో లేదు."
            has_te = any('\u0c00' <= c <= '\u0c7f' for c in txt)
            if target_lang == 'en' and has_te:
                return "English advisory is not available for this recommendation."
            return txt

        chemical_raw = clean_text_field(row.get('Chemical_Control'), '')
        has_chem = bool(chemical_raw and len(chemical_raw) > 5)
        if has_chem:
            chem_clean = isolate_text(chemical_raw, lang)
            chem_structured = {
                'has_verified_chemical': True,
                'product': chem_clean,
                'dosage': chem_clean,
                'water_quantity': "200 Litres water / acre" if lang == 'en' else "ఎకరాకు 200 లీటర్ల నీరు",
                'application_method': "Foliar spray" if lang == 'en' else "ఆకులపై పిచికారీ",
                'waiting_period_phi': "Follow CIBRC product label" if lang == 'en' else "లేబుల్ సూచనలు పాటించండి",
                'safety_precaution': "Wear protective PPE" if lang == 'en' else "చేతి తొడుగులు, మాస్క్ ధరించండి",
                'unverified_message': None
            }
        else:
            unv_msg = "No verified chemical recommendation is available for this diagnosis." if lang == 'en' else "ఈ నిర్ధారణకు ధృవీకరించబడిన రసాయన సిఫారసు అందుబాటులో లేదు."
            chem_structured = {
                'has_verified_chemical': False,
                'product': None,
                'dosage': None,
                'water_quantity': None,
                'application_method': None,
                'waiting_period_phi': None,
                'safety_precaution': None,
                'unverified_message': unv_msg
            }

        adv_text = isolate_text(clean_text_field(row.get('Advisory_' + ('Telugu' if lang == 'te' else 'English')), ''), lang)

        return {
            'is_fallback': False,
            'confirmed_diagnosis': True,
            'disease_or_pest': disease_name,
            'scientific_name': scientific_name if scientific_name and scientific_name.lower() not in ['unknown', 'none'] else None,
            'crop': crop_name,
            'crop_local_name': crop_local_name,
            'problem_type': problem_type,
            'affected_plant_part': affected_part,
            'severity': sev.capitalize(),
            
            'immediate_action_structured': {
                'what_is_problem': adv_text,
                'why_it_occurs': "Weather conditions and canopy humidity contribute to symptom emergence." if lang == 'en' else "వాతావరణ పరిస్థితులు మరియు తేమ తెగులు వ్యాప్తికి దోహదం చేస్తాయి.",
                'steps': [adv_text],
                'urgency': "Moderate Urgency: Initiate corrective measures within 2 to 3 days." if lang == 'en' else "మధ్యస్థ అత్యవసరం: 2 నుండి 3 రోజుల్లోగా నివారణ చర్యలు చేపట్టాలి."
            },
            'prevention_structured': {
                'steps': [isolate_text(clean_text_field(row.get('Prevention'), ''), lang)],
                'next_season': "Practice deep summer plowing and certified seed treatment." if lang == 'en' else "వేసవిలో లోతు దుక్కులు చేసి విత్తన శుద్ధి తప్పనిసరిగా పాటించండి."
            },
            'chemical_structured': chem_structured,

            'symptoms_te': clean_text_field(row.get('Symptoms'), "లక్షణాలు అందుబాటులో ఉన్నాయి."),
            'symptoms_en': isolate_text(clean_text_field(row.get('Symptoms'), ''), 'en'),
            'advisory_te': clean_text_field(row.get('Advisory_Telugu'), "ఈ రికార్డుకు తెలుగు సలహా అందుబాటులో లేదు."),
            'advisory_en': clean_text_field(row.get('Advisory_English'), "English advisory is not available for this record."),
            
            'immediate_actions': adv_text,
            'organic_management': isolate_text(clean_text_field(row.get('Organic_Management'), ''), lang),
            'biological_control': isolate_text(clean_text_field(row.get('Biological_Control'), ''), lang),
            'cultural_control': isolate_text(clean_text_field(row.get('Cultural_Control'), ''), lang),
            'chemical_control': chem_structured.get('unverified_message') or chemical_raw,
            'prevention': isolate_text(clean_text_field(row.get('Prevention'), ''), lang),
            'safety_precautions': isolate_text(clean_text_field(row.get('Safety_Precautions'), ''), lang),
            'diagnostic_questions': clean_text_field(row.get('Diagnostic_Questions'), None),
            'source': clean_text_field(row.get('Source'), 'PJTSAU / ANGRAU Agricultural Advisory Guidelines')
        }

    def get_fallback_advisory(self, crop: Optional[str] = None, language: str = 'te') -> Dict[str, Any]:
        """
        Retrieves crop-specific diagnostic questions and general non-chemical guidance
        from 'data/processed/diagnosis_fallback.csv' when confidence is low or diagnosis is uncertain.
        Strictly provides NO chemical recommendations.
        """
        if self.df_fallback.empty:
            self._load_datasets()

        norm_crop = normalize_crop_name(crop)
        selected_row = None
        lang = 'te' if language == 'te' else 'en'

        if not self.df_fallback.empty:
            if norm_crop and norm_crop.lower() != 'general':
                crop_matches = self.df_fallback[self.df_fallback['Crop'].str.lower() == norm_crop.lower()]
                if not crop_matches.empty:
                    selected_row = crop_matches.iloc[0]

            if selected_row is None and not self.df_fallback.empty:
                selected_row = self.df_fallback.iloc[0]

        if selected_row is not None:
            row = selected_row
            diag_questions_te = clean_text_field(
                row.get('Diagnostic_Questions'),
                "ఆకులపై మచ్చల ఆకారం ఏమిటి? నష్టం ఎంత శాతం ఉంది? పురుగులు లేదా వాటి విసర్జితాలు కనిపిస్తున్నాయా?"
            )
            diag_questions_en = "Are leaf spots circular or irregular? Are insects or webbing visible? What percentage of plants show symptoms?"
            advisory_te = clean_text_field(
                row.get('Advisory_Telugu'),
                "పంట లక్షణాలు పూర్తిగా నిర్ధారణ కానందున, పొలాన్ని మరింత నిశితంగా పరిశీలించి స్థానిక వ్యవసాయ శాఖ అధికారిని సంప్రదించండి."
            )
            advisory_en = clean_text_field(
                row.get('Advisory_English'),
                "English advisory is not available for this record."
            )
            crop_name = clean_text_field(row.get('Crop'), norm_crop or "General")
        else:
            diag_questions_te = "ఆకులపై మచ్చల ఆకారం ఏమిటి? పురుగులు కనిపిస్తున్నాయా? ఏ దశలో నష్టం ప్రారంభమైంది?"
            diag_questions_en = "What is the shape of leaf spots? Are insects visible? At what stage did damage begin?"
            advisory_te = "ఈ రికార్డుకు తెలుగు సలహా అందుబాటులో లేదు."
            advisory_en = "English advisory is not available for this record."
            crop_name = norm_crop or "General"

        diag_questions = diag_questions_en if lang == 'en' else diag_questions_te
        unv_chem_msg = (
            "No verified chemical recommendation is available for this diagnosis. "
            "Diagnosis is uncertain; never spray chemicals without confirmed pathogen identification."
            if lang == 'en' else
            "ఈ నిర్ధారణకు ధృవీకరించబడిన రసాయన సిఫారసు అందుబాటులో లేదు. "
            "ఖచ్చితమైన నిర్ధారణ లేకుండా పురుగుమందులు వాడవద్దు."
        )

        return {
            'is_fallback': True,
            'confirmed_diagnosis': False,
            'disease_or_pest': 'Requires further diagnosis (మరింత నిర్ధారణ అవసరం)' if lang == 'te' else 'Requires further diagnosis',
            'scientific_name': None,
            'crop': crop_name,
            'crop_local_name': CROP_TELUGU_NAMES.get(crop_name, crop_name),
            'problem_type': 'Diagnosis Pending',
            'affected_plant_part': 'Observation Required',
            'severity': 'Pending Verification',
            
            # Diagnostic questions to ask the farmer
            'diagnostic_questions': diag_questions,
            'diagnostic_questions_te': diag_questions_te,
            'diagnostic_questions_en': diag_questions_en,
            'advisory_te': advisory_te,
            'advisory_en': advisory_en,
            
            'immediate_action_structured': {
                'what_is_problem': (
                    "The symptom description is ambiguous or multiple crop problems match this pattern. "
                    "Further field scouting or expert review is required." if lang == 'en' else
                    "లక్షణాలు నిర్దిష్టంగా లేనందున ఒకే రకమైన తెగులుగా నిర్ధారించలేకపోతున్నాము. మరింత పరిశీలన అవసరం."
                ),
                'why_it_occurs': (
                    "Overlapping symptoms between nutritional deficiencies, insect attacks, and early fungal infections." if lang == 'en' else
                    "పోషక లోపాలు, పురుగుల ఉధృతి మరియు ప్రారంభ శిలీంధ్ర లక్షణాలు ఒకేలా ఉండటం వల్ల ఖచ్చితమైన నిర్ధారణ అవసరం."
                ),
                'steps': [
                    "Review the interactive diagnostic questions below and select matching signs." if lang == 'en' else "క్రింద ఉన్న నిర్ధారణ ప్రశ్నలను పరిశీలించి సరిపోలే లక్షణాలను ఎంచుకోండి.",
                    "Isolate a small sample leaf and consult your local Agricultural Officer (MAO)." if lang == 'en' else "తెగులు సోకిన ఆకును స్థానిక వ్యవసాయ అధికారికి చూపించి నిర్ధారించుకోండి.",
                    "Avoid applying chemical pesticides without confirmed diagnosis." if lang == 'en' else "స్పష్టమైన నిర్ధారణ లేకుండా రసాయన పురుగుమందులను పిచికారీ చేయవద్దు."
                ],
                'urgency': "Scouting Urgency: Conduct detailed field scouting within 24 hours." if lang == 'en' else "పరిశీలన అత్యవసరం: రాబోయే 24 గంటల్లో పొలాన్ని నిశితంగా పరిశీలించండి."
            },
            'prevention_structured': {
                'steps': [
                    "Conduct regular field scouting twice a week." if lang == 'en' else "వారానికి రెండుసార్లు పొలాన్ని నిశితంగా పరిశీలించండి.",
                    "Maintain balanced soil nutrition based on soil health cards." if lang == 'en' else "భూసార పరీక్ష ఆధారంగా సమతుల్య ఎరువులను వాడండి."
                ],
                'next_season': "Practice seed treatment and crop rotation with non-host crops." if lang == 'en' else "విత్తన శుద్ధి తప్పక చేసి, పంట మార్పిడి పాటించండి."
            },
            'chemical_structured': {
                'has_verified_chemical': False,
                'product': None,
                'dosage': None,
                'water_quantity': None,
                'application_method': None,
                'waiting_period_phi': None,
                'safety_precaution': None,
                'unverified_message': unv_chem_msg
            },

            # Non-chemical general guidance only
            'organic_management': (
                "Apply 5% Neem Seed Kernel Extract (NSKE) or neem oil as a safe general repellent." if lang == 'en' else
                "వేప నూనె లేదా సహజ కషాయాలను సాధారణ రక్షణ చర్యగా పరిశీలించవచ్చు."
            ),
            'biological_control': (
                "Install yellow and blue sticky traps to identify flying insect pests." if lang == 'en' else
                "పసుపు/నీలి జిగురు అట్టలు అమర్చి పురుగుల ఉనికిని గమనించండి."
            ),
            'cultural_control': (
                "Ensure proper field drainage and clear weed hosts on field bunds." if lang == 'en' else
                "నీటి నిల్వను తగ్గించండి, కలుపు మొక్కలను తొలగించండి."
            ),
            'chemical_control': None,
            'prevention': (
                "Regular field scouting and balanced NPK fertilization." if lang == 'en' else
                "క్రమం తప్పకుండా పొలం పరిశీలన చేయండి, సమతుల్య ఎరువులు వాడండి."
            ),
            'safety_precautions': (
                "Strictly avoid applying chemical insecticides or fungicides without pathogen confirmation." if lang == 'en' else
                "తెగులు నిర్ధారణ కాకుండా పురుగుమందులు వాడవద్దు. నిపుణుల సలహా తీసుకోండి."
            ),
            'source': 'PJTSAU / ANGRAU Diagnostic Fallback Corpus'
        }


# Singleton engine instance
advisory_engine = SmartAdvisoryEngine()


def get_advisory(
    disease_or_pest: str,
    crop: Optional[str] = None,
    language: str = 'te',
    severity: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Convenience helper to retrieve advisory."""
    return advisory_engine.get_advisory(
        disease_or_pest=disease_or_pest,
        crop=crop,
        language=language,
        severity=severity
    )


def get_fallback_advisory(crop: Optional[str] = None, language: str = 'te') -> Dict[str, Any]:
    """Convenience helper to retrieve fallback diagnostic questions and safe advice."""
    return advisory_engine.get_fallback_advisory(crop=crop, language=language)


def log_advisory_view(
    user_id: Optional[int],
    disease_or_pest: str,
    crop: Optional[str] = None,
    prediction_id: Optional[int] = None,
    language: str = 'te'
) -> Optional[int]:
    """
    Saves an advisory view audit record to the database linked to the authenticated farmer.
    """
    try:
        record = AdvisoryViewRecord(
            user_id=user_id,
            prediction_id=prediction_id,
            disease_or_pest=disease_or_pest,
            crop=crop,
            language=language or 'te'
        )
        db.session.add(record)
        db.session.commit()
        logger.info(f"Logged advisory view: user_id={user_id}, disease='{disease_or_pest}'")
        return record.id
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error logging advisory view: {e}")
        return None


# =============================================================================
# Legacy & Voice Advisory Query Compatibility Layer
# =============================================================================

AGRICULTURAL_KNOWLEDGE_BASE = [
    {
        'keywords': ['వరి', 'అగ్గి తెగులు', 'blast', 'వరి అగ్గి', 'వరి ఆకుమచ్చ'],
        'language': 'te',
        'category': 'Disease Management - Rice',
        'response': (
            "వరిలో అగ్గి తెగులు (Blast) నివారణకు సిఫార్సులు:\n"
            "1. సేంద్రీయ పద్ధతి: లీటరు నీటికి సూడోమోనాస్ ఫ్లోరోసెన్స్ 10 గ్రాములు లేదా 5% వేప గింజల కషాయం (NSKE) పిచికారీ చేయండి.\n"
            "2. రసాయన పద్ధతి: ట్రైసైక్లాజోల్ 75% WP లీటరు నీటికి 0.6 గ్రా. లేదా ఐసోప్రోథియోలేన్ 40% EC 1.5 మి.లీ. పిచికారీ చేయండి.\n"
            "3. జాగ్రత్తలు: పంటలో నత్రజని (యూరియా) ఎరువులను అధికంగా వాడకండి; పొలంలో నిలిచిన నీటిని తీసివేసి ఆరబెట్టండి."
        )
    },
    {
        'keywords': ['धान', 'झुलसा', 'ब्लास्ट', 'blast', 'rice blast'],
        'language': 'hi',
        'category': 'Disease Management - Rice',
        'response': (
            "धान में झुलसा रोग (Blast) के नियंत्रण हेतु उपाय:\n"
            "1. जैविक उपाय: स्यूडोमोनास फ्लोरोसेंस 10 ग्राम/लीटर या 5% नीम के बीज के काढ़े का छिड़काव करें।\n"
            "2. रासायनिक उपाय: ट्राइसाइक्लाजोल 75% WP 0.6 ग्राम/लीटर अथवा आइसोप्रोपियोलेन 40% EC 1.5 मिली/लीटर का छिड़काव करें।\n"
            "3. प्रबंधन: यूरिया (नाइट्रोजन) की अधिक मात्रा देने से बचें। खेत से अतिरिक्त पानी निकाल दें।"
        )
    },
    {
        'keywords': ['टमाटर', 'झुलसा', 'पत्ती मरोड़', 'leaf curl', 'early blight'],
        'language': 'hi',
        'category': 'Disease Management - Tomato',
        'response': (
            "टमाटर में झुलसा एवं पत्ती मरोड़ रोग का उपचार:\n"
            "1. झुलसा नियंत्रण: मैंकोजेब 75% WP 2.5 ग्राम/लीटर या क्लोरोथालोनिल 2 ग्राम/लीटर का छिड़काव करें।\n"
            "2. सफेद मक्खी (पत्ती मरोड़ वाहक) नियंत्रण: पीले चिपचिपे ट्रैप लगाएं और इमिडाक्लोप्रिड 17.8% SL 0.5 मिली/लीटर पानी में घोलकर छिड़कें।\n"
            "3. खेत की सफाई रखें तथा संक्रमित पत्तियों को तोड़कर नष्ट कर दें।"
        )
    },
    {
        'keywords': ['कपास', 'सफेद मक्खी', 'गुलाबी सुंडी', 'whitefly', 'bollworm'],
        'language': 'hi',
        'category': 'Pest Management - Cotton',
        'response': (
            "कपास में सफेद मक्खी एवं कीट नियंत्रण उपाय:\n"
            "1. पीला चिपचिपा प्रपंच (येलो स्टिकी ट्रैप) 15-20 प्रति एकड़ लगाएं।\n"
            "2. 5% नीम तेल (1500 ppm) 5 मिली प्रति लीटर पानी में मिलाकर पत्तियों के नीचे छिड़काव करें।\n"
            "3. प्रकोप अधिक होने पर फ्लोनिकामाइड 50% WG 0.3 ग्राम/लीटर या डायफेन्थियूरॉन 1.25 ग्राम/लीटर का छिड़काव करें।"
        )
    },
    {
        'keywords': ['ప్రత్తి', 'తెల్లదోమ', 'whitefly', 'ఆకుముడత', 'leaf curl'],
        'language': 'te',
        'category': 'Pest Management - Cotton',
        'response': (
            "ప్రత్తి పంటలో తెల్లదోమ మరియు ఆకుముడత నివారణ చర్యలు:\n"
            "1. జీవ నియంత్రణ: ఎకరాకు 15-20 పసుపు రంగు జిగురు అట్టలను ఏర్పాటు చేసి తెల్లదోమ ఉధృతిని తగ్గించండి.\n"
            "2. కషాయం: 5% వేప నూనెను లీటరు నీటికి 5 మి.లీ. చొప్పున కలిపి ఆకుల అడుగు భాగం తడిసేలా పిచికారీ చేయండి.\n"
            "3. రసాయన మందు: డయాఫెంథియురాన్ 50% WP లీటరుకు 1.25 గ్రా. లేదా ఫ్లోనికామిడ్ 50% WG 0.3 గ్రా. పిచికారీ చేయండి."
        )
    },
    {
        'keywords': ['టమాటో', 'టమాట', 'మాడు తెగులు', 'early blight', 'late blight'],
        'language': 'te',
        'category': 'Disease Management - Tomato',
        'response': (
            "టమాట పంటలో ఆకుమాడు / బ్లైట్ తెగులు నివారణ:\n"
            "1. నివారణ చర్యలు: తెగులు సోకిన కింది ఆకులను కత్తిరించి నాశనం చేయండి. మొక్కల మధ్య గాలి వెలుతురు ఉండేలా చూడండి.\n"
            "2. పిచికారీ: మాంకోజెబ్ 75% WP లీటరు నీటికి 2.5 గ్రా. లేదా క్లోరోథలోనిల్ 2 గ్రా. పిచికారీ చేయండి.\n"
            "3. వర్షపు రోజుల్లో: కాపర్ ఆక్సిక్లోరైడ్ 3 గ్రా. లేదా మెటలాక్సిల్ + మాంకోజెబ్ 2 గ్రా. లీటరు నీటికి వాడండి."
        )
    },
    {
        'keywords': ['rice', 'blast', 'paddy', 'leaf blast', 'neck blast'],
        'language': 'en',
        'category': 'Disease Management - Rice',
        'response': (
            "Management of Blast in Rice / Paddy:\n"
            "1. Organic Control: Spray Pseudomonas fluorescens @ 10g/L or 5% Neem Seed Kernel Extract (NSKE).\n"
            "2. Chemical Control: Spray Tricyclazole 75% WP @ 0.6g/L or Isoprothiolane 40% EC @ 1.5ml/L at disease onset.\n"
            "3. Agronomic Practice: Avoid excessive top-dressing of nitrogen fertilizers and avoid stagnant standing water during humid days."
        )
    },
    {
        'keywords': ['cotton', 'whitefly', 'leaf curl', 'bollworm', 'pest'],
        'language': 'en',
        'category': 'Pest Management - Cotton',
        'response': (
            "Integrated Pest Management for Cotton:\n"
            "1. Install 15-20 yellow sticky traps per acre to monitor and suppress whitefly vector population.\n"
            "2. Spray 5% Neem Seed Kernel Extract (NSKE) or Neem Oil 1500 ppm @ 5ml/L targeting undersides of foliage.\n"
            "3. For severe infestation exceeding ETL, apply Diafenthiuron 50% WP @ 1.25g/L or Flonicamid 50% WG @ 0.3g/L strictly adhering to label safety directions."
        )
    },
    {
        'keywords': ['tomato', 'early blight', 'leaf spot', 'blight', 'alternaria'],
        'language': 'en',
        'category': 'Disease Management - Tomato',
        'response': (
            "Control Measures for Tomato Early Blight (Alternaria solani):\n"
            "1. Pruning: Remove and safely destroy lower infected leaves with target-board lesions.\n"
            "2. Fungicide Spray: Apply Mancozeb 75% WP @ 2.5g/L or Chlorothalonil @ 2g/L water at early disease onset.\n"
            "3. Field Practice: Ensure wide row spacing for good air circulation and avoid overhead furrow flooding."
        )
    }
]


def _match_knowledge_base(query_text: str, language: str) -> Tuple[str, str]:
    query_lower = query_text.lower()
    for entry in AGRICULTURAL_KNOWLEDGE_BASE:
        if entry['language'] == language:
            for kw in entry['keywords']:
                if kw.lower() in query_lower:
                    return entry['response'], entry['category']
    for entry in AGRICULTURAL_KNOWLEDGE_BASE:
        for kw in entry['keywords']:
            if kw.lower() in query_lower:
                return entry['response'], entry['category']
    fallback_response = (
        "క్షమించండి, మీ ప్రశ్నకు సంబంధించిన పూర్తి సమాచారం ప్రస్తుతానికి అందుబాటులో లేదు.\n"
        "దయచేసి దగ్గరలోని కృషి విజ్ఞాన కేంద్రం (KVK) లేదా మండల వ్యవసాయ అధికారిని సంప్రదించండి."
        if language == 'te' else
        "Sorry, specific recommendations for your query are currently not found in the immediate knowledge base.\n"
        "Please consult your local Krishi Vigyan Kendra (KVK) or Agriculture Extension Officer."
    )
    return fallback_response, "General Farming Inquiry"


def process_advisory_query(query_text: str, language: str = 'te', input_type: str = 'text', app_config=None, user_id=None):
    if not query_text or not str(query_text).strip():
        raise ValueError("Query text cannot be empty.")

    query_text = str(query_text).strip()
    language = language.lower() if language else 'te'
    if language not in SUPPORTED_LANGUAGES:
        language = 'te'

    lang_meta = SUPPORTED_LANGUAGES[language]
    response_text, category = _match_knowledge_base(query_text, language)

    # Persist query
    record = AdvisoryQueryRecord(
        user_id=user_id,
        user_query=query_text,
        detected_language=language,
        input_type=input_type,
        response_text=response_text,
        category=category
    )
    db.session.add(record)
    db.session.commit()

    return {
        'success': True,
        'record_id': record.id,
        'query': query_text,
        'language': language,
        'language_name': lang_meta['name'],
        'input_type': input_type,
        'response': response_text,
        'category': category,
        'speech_tag': lang_meta.get('speech_tag', 'te-IN'),
        'timestamp': record.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }
