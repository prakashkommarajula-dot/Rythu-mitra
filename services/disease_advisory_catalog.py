"""
=============================================================================
Rythu Mithra - AI-Based Multilingual Crop Disease & Pest Detection
Service: disease_advisory_catalog.py
Verified Bilingual Agricultural Knowledge Dossiers for 23 Major Crop Pathogens
Derived strictly from ANGRAU, ICAR, PJTSAU, and CIBRC recommended packages.
=============================================================================
"""

from typing import Dict, Any, Optional, List

# Verified Agricultural Dossiers for 23 Target Pathogens / Pests across 14 crops
ADVISORY_CATALOG: Dict[str, Dict[str, Any]] = {
    "Blast": {
        "disease": "Blast",
        "crop": "Rice",
        "scientific_name": "Pyricularia oryzae / Magnaporthe oryzae",
        "problem_type": "Fungal Disease",
        "affected_part": "Leaves, Nodes, Panicle Neck",
        "severity": "High",
        "what_is_problem": {
            "en": "Rice Blast is a destructive fungal disease caused by Pyricularia oryzae. It produces spindle-shaped lesions with ash-grey centers and dark brown margins on leaves. When the fungus attacks the neck node of the panicle (neck blast), the entire panicle turns white and grains remain completely unfilled (chaffy). It can cause 40-70% yield loss in susceptible varieties under favorable weather conditions, with spores spreading rapidly across fields via wind.",
            "te": "వరి అగ్గి తెగులు (బ్లాస్ట్) అనేది పైరిక్యులేరియా ఒరైజే అనే శిలీంధ్రం వల్ల కలిగే తీవ్రమైన వ్యాధి. ఆకులపై కండె ఆకారపు లేదా నూలు కండె వంటి మచ్చలు ఏర్పడి, మధ్యలో బూడిద రంగు మరియు అంచులలో గోధుమ రంగు కనిపిస్తాయి. ఈ తెగులు కంకి మెడ భాగానికి సోకితే (మెడ విరుపు), కంకి తెల్లబడి గింజలు తాలుగా మారి 40-70% వరకు దిగుబడి నష్టం వాటిల్లుతుంది. గాలి ద్వారా దీని బీజాలు పొరుగు పొలాలకు వేగంగా వ్యాపిస్తాయి."
        },
        "why_it_occurs": {
            "en": "High relative humidity (>85%), night temperatures between 18-24°C, persistent dew or raindrops on leaves for more than 10 hours, and excessive application of nitrogenous fertilizers (urea) make leaf tissues tender and highly susceptible to fungal penetration.",
            "te": "గాలిలో అధిక తేమ (85% పైగా), రాత్రి ఉష్ణోగ్రతలు 18-24°C ఉండటం, ఆకులపై మంచు లేదా నీరు ఎక్కువసేపు నిలిచి ఉండటం మరియు పంటకు సిఫారసు కంటే అధికంగా యూరియా (నత్రజని) వాడటం వల్ల ఆకులు లేతగా మారి తెగులు ఉధృతి పెరుగుతుంది."
        },
        "immediate_action_steps": {
            "en": [
                "Inspect the field thoroughly to map the extent of spindle lesions across nursery and main fields.",
                "Drain excess standing water from the field for 2 to 3 days to reduce canopy micro-humidity.",
                "Immediately stop nitrogen (urea) top-dressing until the disease is brought under control.",
                "Remove and safely burn or bury heavily infected leaves and neck-blasted panicles away from water channels.",
                "Consult the local Mandal Agricultural Officer (MAO) if spindle lesions are actively expanding across the field."
            ],
            "te": [
                "పొలాన్ని నిశితంగా పరిశీలించి, నారుమడి మరియు ప్రధాన పొలంలో తెగులు వ్యాపించిన ప్రాంతాలను గుర్తించండి.",
                "మొక్కల మధ్య తేమను తగ్గించడానికి పొలంలోని నిలిచిన నీటిని 2-3 రోజుల పాటు తీసివేసి ఆరబెట్టండి.",
                "తెగులు అదుపులోకి వచ్చే వరకు నత్రజని (యూరియా) ఎరువుల వాడకాన్ని పూర్తిగా నిలిపివేయండి.",
                "తీవ్రంగా తెగులు సోకిన ఆకులు మరియు మెడ విరుపు కంకులను ఏరివేసి పొలానికి దూరంగా తగులబెట్టండి.",
                "మచ్చలు వేగంగా విస్తరిస్తుంటే స్థానిక మండల వ్యవసాయ అధికారి (MAO) లేదా కృషి విజ్ఞాన కేంద్రాన్ని సంప్రదించండి."
            ]
        },
        "action_urgency": {
            "en": "High Urgency: Initiate cultural and corrective actions within 24 to 48 hours to protect panicle necks.",
            "te": "అత్యవసర చర్య అవసరం: కంకి మెడ భాగాన్ని కాపాడుకోవడానికి 24 నుండి 48 గంటల్లోగా నివారణ చర్యలు చేపట్టాలి."
        },
        "prevention_steps": {
            "en": [
                "Grow blast-resistant varieties recommended by ANGRAU such as MTU 1010, NLR 34449, or Simhapuri.",
                "Compulsory seed treatment with Tricyclazole 75% WP @ 2g/kg seed or Carbendazim @ 2g/kg seed prior to sowing.",
                "Avoid dense nursery sowing (do not exceed 25-30 kg seed/acre) to ensure proper sunlight and air circulation.",
                "Apply nitrogen in 3-4 split doses (basal, tillering, panicle initiation) rather than large single applications.",
                "Keep field bunds clean and destroy weed hosts like Echinochloa grass.",
                "Avoid late planting during cold, foggy winter months."
            ],
            "te": [
                "ANGRAU సిఫారసు చేసిన అగ్గి తెగులు నిరోధక రకాలైన MTU 1010, NLR 34449, సింహపురి వంటి రకాలను సాగు చేయండి.",
                "విత్తే ముందు కిలో విత్తనానికి ట్రైసైక్లాజోల్ 75% WP @ 2 గ్రా. లేదా కార్బండిజిమ్ @ 2 గ్రా. కలిపి విత్తన శుద్ధి చేయండి.",
                "నారుమడిలో మొక్కల సాంద్రతను క్రమబద్ధీకరించండి (ఎకరాకు 25-30 కిలోల విత్తనం మించకూడదు).",
                "నత్రజని ఎరువులను ఒకేసారి వేయకుండా 3-4 భాగాలుగా విభజించి వేయండి.",
                "గట్లపై ఉండే తుంగ, గరిక వంటి కలుపు మొక్కలను తొలగించి పొలాన్ని శుభ్రంగా ఉంచండి.",
                "చలి మరియు మంచు ఎక్కువగా ఉండే కాలంలో ఆలస్యంగా నాట్లు వేయడం మానుకోండి."
            ]
        },
        "next_season_prevention": {
            "en": "Conduct deep summer ploughing to expose resting fungal spores to solar heat. Burn or compost all paddy stubbles thoroughly before next season.",
            "te": "వేసవిలో లోతు దుక్కులు చేసి భూమిలోని శిలీంధ్ర బీజాలను ఎండబెట్టండి. పంట కోసిన వెంటనే మోడులను మరియు వ్యర్థాలను నాశనం చేయండి."
        },
        "organic_management": {
            "en": "Spray 5% Neem Seed Kernel Extract (NSKE) @ 50ml/L or Pseudomonas fluorescens @ 10g/L water at early disease initiation.",
            "te": "తెగులు ప్రారంభ దశలో 5% వేప గింజల కషాయం (NSKE) లేదా సూడోమోనాస్ ఫ్లోరోసెన్స్ 10 గ్రాములు లీటరు నీటికి కలిపి పిచికారీ చేయండి."
        },
        "biological_control": {
            "en": "Foliar spray with Bacillus subtilis or Trichoderma harzianum @ 5g/L water suppresses fungal mycelial growth.",
            "te": "ట్రైకోడెర్మా హార్జియానమ్ లేదా బాసిల్లస్ సబ్టిలిస్ 5 గ్రాములు లీటరు నీటికి కలిపి పిచికారీ చేయడం వల్ల శిలీంధ్రం సహజంగా అదుపులోకి వస్తుంది."
        },
        "cultural_control": {
            "en": "Practice Alternate Wetting and Drying (AWD) irrigation and maintain balanced potassium application.",
            "te": "పొలంలో ఆరుతడి పద్ధతిని పాటించండి మరియు తగినంత పొటాష్ ఎరువును సమతుల్యంగా వేయండి."
        },
        "chemical_control": {
            "has_verified_chemical": True,
            "product": {
                "en": "Tricyclazole 75% WP or Isoprothiolane 40% EC",
                "te": "ట్రైసైక్లాజోల్ 75% WP లేదా ఐసోప్రోథియోలేన్ 40% EC"
            },
            "dosage": {
                "en": "Tricyclazole 75% WP @ 0.6g/L water OR Isoprothiolane 40% EC @ 1.5ml/L water",
                "te": "ట్రైసైక్లాజోల్ 75% WP @ 0.6 గ్రా./లీటర్ నీటికి లేదా ఐసోప్రోథియోలేన్ 40% EC @ 1.5 మి.లీ./లీటర్ నీటికి"
            },
            "water_quantity": {
                "en": "200 Litres of spray solution per acre for manual knapsack sprayer",
                "te": "ఎకరాకు 200 లీటర్ల పిచికారీ ద్రావణం (నేప్‌సాక్ స్ప్రేయర్‌తో)"
            },
            "application_method": {
                "en": "High volume foliar spray ensuring thorough coverage of bottom canopy and panicle neck",
                "te": "ఆకులు మరియు కంకి మొదళ్ళు పూర్తిగా తడిసేలా పిచికారీ చేయండి"
            },
            "waiting_period_phi": {
                "en": "30 days before harvest (strictly observe PHI for food safety)",
                "te": "పంట కోతకు ముందు 30 రోజుల వేచిఉండే కాలం (PHI) పాటించాలి"
            },
            "safety_precaution": {
                "en": "Wear protective mask, gloves, and protective eyewear; avoid spraying against the wind.",
                "te": "మాస్క్, చేతి తొడుగులు ధరించండి. గాలికి ఎదురుగా పిచికారీ చేయవద్దు."
            }
        },
        "safety_precautions": {
            "en": "Wear protective mask, gloves, and protective eyewear. Wash hands with soap immediately after spraying. Keep chemical containers locked away from children.",
            "te": "పిచికారీ చేసేటప్పుడు మాస్క్, చేతి తొడుగులు ధరించండి. పిచికారీ చేసిన వెంటనే చేతులను సబ్బుతో శుభ్రం చేసుకోండి. పురుగుమందు డబ్బాలను పిల్లలకు మరియు పశువులకు దూరంగా ఉంచండి."
        }
    },

    "Tikka Leaf Spot": {
        "disease": "Tikka Leaf Spot",
        "crop": "Groundnut",
        "scientific_name": "Cercospora arachidicola / Cercosporidium personatum",
        "problem_type": "Fungal Disease",
        "affected_part": "Leaves, Petioles, Stems",
        "severity": "Moderate to High",
        "what_is_problem": {
            "en": "Tikka Leaf Spot (Early and Late Cercospora leaf spot) is the most destructive foliar disease of groundnut. It causes circular dark brown to black spots with bright yellow halos on leaves, leading to severe premature defoliation. Without timely intervention, pod development is severely stunted, kernel size decreases, and yield losses can reach 30-50%.",
            "te": "వేరుశనగలో తిక్కా ఆకుమచ్చ తెగులు (ముందస్తు మరియు ఆలస్యపు మచ్చలు) ప్రధాన శిలీంధ్ర వ్యాధి. ఆకులపై పసుపు రంగు వలయంతో కూడిన ముదురు గోధుమ లేదా నలుపు రంగు గుండ్రని మచ్చలు ఏర్పడతాయి. తెగులు ఉధృతమైతే ఆకులు రాలిపోయి, కాయల పరిమాణం తగ్గి 30-50% వరకు దిగుబడి నష్టం వాటిల్లుతుంది."
        },
        "why_it_occurs": {
            "en": "Prolonged leaf wetness caused by continuous drizzle, morning dew, temperatures around 25-28°C, and soil-borne fungal spore inoculum from previous groundnut crop residues create ideal conditions for outbreak.",
            "te": "ఎడతెరిపి లేని జల్లులు, ఉదయపు మంచు, 25-28°C ఉష్ణోగ్రతలు మరియు నేలలోని గత పంట అవశేషాల నుండి శిలీంధ్ర బీజాలు గాలి ద్వారా మొక్కలకు సోకడం వల్ల ఈ తెగులు వ్యాపిస్తుంది."
        },
        "immediate_action_steps": {
            "en": [
                "Scout the lower canopy of plants to count spots per leaflet across multiple field spots.",
                "Ensure standing irrigation or rainwater is drained freely to lower ground-level humidity.",
                "Remove and bury heavily blighted fallen leaves to eliminate surface conidia spores.",
                "Avoid touching wet foliage during early morning scouting to avoid mechanical spread of spores.",
                "Consult the local agricultural extension officer if defoliation exceeds 10% of lower canopy."
            ],
            "te": [
                "మొక్కల క్రింది ఆకులపై మచ్చల తీవ్రతను పొలంలోని వివిధ భాగాల్లో నిశితంగా పరిశీలించండి.",
                "నేలపై తేమను తగ్గించడానికి పొలంలో నిలిచిన అదనపు నీటిని బయటకు పంపించండి.",
                "రాలిపడిన తెగులు సోకిన ఆకులను ఏరివేసి భూమిలో పాతిపెట్టండి.",
                "ఉదయం పూట మంచు ఉన్నప్పుడు పొలంలో తిరగవద్దు, దీనివల్ల తెగులు బీజాలు ఇతర మొక్కలకు వ్యాపిస్తాయి.",
                "ఆకులు రాలడం 10% కంటే ఎక్కువైతే వెంటనే స్థానిక వ్యవసాయ అధికారిని సంప్రదించండి."
            ]
        },
        "action_urgency": {
            "en": "Moderate Urgency: Initiate foliar spray within 2 to 4 days of spotting initial concentric lesions.",
            "te": "మధ్యస్థ అత్యవసరం: ఆకులపై గుండ్రని మచ్చలు కనిపించిన 2 నుండి 4 రోజుల్లోగా పిచికారీ చర్యలు చేపట్టాలి."
        },
        "prevention_steps": {
            "en": [
                "Sow tolerant varieties such as Kadiri-6, Kadiri-9, ICGV 91114, or TAG-24.",
                "Treat seed with Mancozeb @ 3g/kg seed or Carbendazim @ 2g/kg seed before sowing.",
                "Adopt intercropping with pigeonpea (redgram) or pearl millet in a 4:1 or 6:1 row ratio.",
                "Maintain optimal plant population without overcrowding (33 plants per square meter).",
                "Ensure balanced potash application (20-30 kg K2O/acre) to build leaf resistance."
            ],
            "te": [
                "కదిరి-6, కదిరి-9, ICGV 91114 లేదా TAG-24 వంటి తెగులు తట్టుకునే రకాలను ఎంపిక చేసుకోండి.",
                "విత్తే ముందు కిలో విత్తనానికి మాంకోజెబ్ @ 3 గ్రా. లేదా కార్బండిజిమ్ @ 2 గ్రా. కలిపి విత్తన శుద్ధి చేయండి.",
                "కందులు లేదా సజ్జలతో 4:1 లేదా 6:1 నిష్పత్తిలో అంతరపంటగా సాగు చేయండి.",
                "చదరపు మీటరుకు 33 మొక్కలు ఉండేలా సరైన సాంద్రతను పాటించండి.",
                "ఆకులలో రోగనిరోధక శక్తిని పెంచడానికి ఎకరాకు 20-30 కిలోల పొటాష్ ఎరువును సమతుల్యంగా వేయండి."
            ]
        },
        "next_season_prevention": {
            "en": "Rotate groundnut with non-leguminous cereals (maize, sorghum, pearl millet) and practice deep summer plowing to bury fungal debris.",
            "te": "పంట మార్పిడిలో వేరుశనగ తర్వాత జొన్న లేదా మొక్కజొన్న సాగు చేయండి. వేసవిలో లోతు దుక్కులు చేసి తెగులు శేషాలను నాశనం చేయండి."
        },
        "organic_management": {
            "en": "Spray 5% Neem Seed Kernel Extract (NSKE) or Panchagavya @ 30ml/L water at initial spot appearance.",
            "te": "మచ్చలు కనిపించిన వెంటనే 5% వేప గింజల కషాయం లేదా పంచగవ్య 30 మి.లీ. లీటరు నీటికి కలిపి పిచికారీ చేయండి."
        },
        "biological_control": {
            "en": "Foliar application of Pseudomonas fluorescens @ 10g/L or Trichoderma viride @ 5g/L water at 15-day intervals.",
            "te": "సూడోమోనాస్ ఫ్లోరోసెన్స్ 10 గ్రా. లేదా ట్రైకోడెర్మా విరిడె 5 గ్రా. లీటరు నీటికి కలిపి 15 రోజుల వ్యవధిలో పిచికారీ చేయండి."
        },
        "cultural_control": {
            "en": "Practice wider row spacing, timely weeding, and balanced fertilizer management.",
            "te": "మొక్కల మధ్య సరైన దూరం పాటించండి, కలుపు లేకుండా చూసుకోండి మరియు సమతుల్య ఎరువులు వేయండి."
        },
        "chemical_control": {
            "has_verified_chemical": True,
            "product": {
                "en": "Mancozeb 75% WP or Tebuconazole 25.9% EC",
                "te": "మాంకోజెబ్ 75% WP లేదా టెబుకొనాజోల్ 25.9% EC"
            },
            "dosage": {
                "en": "Mancozeb 75% WP @ 2.5g/L water OR Tebuconazole 25.9% EC @ 1ml/L water",
                "te": "మాంకోజెబ్ 75% WP @ 2.5 గ్రా./లీటర్ నీటికి లేదా టెబుకొనాజోల్ 25.9% EC @ 1 మి.లీ./లీటర్ నీటికి"
            },
            "water_quantity": {
                "en": "200 Litres of spray solution per acre",
                "te": "ఎకరాకు 200 లీటర్ల పిచికారీ ద్రావణం"
            },
            "application_method": {
                "en": "Thorough foliar spray wetting both upper and lower leaf surfaces",
                "te": "ఆకుల పైభాగం మరియు అడుగు భాగం పూర్తిగా తడిసేలా పిచికారీ చేయండి"
            },
            "waiting_period_phi": {
                "en": "14 to 21 days before harvest",
                "te": "పంట కోతకు ముందు 14 నుండి 21 రోజుల వేచిఉండే కాలం (PHI)"
            },
            "safety_precaution": {
                "en": "Wear protective gear during handling; do not let livestock graze in sprayed fields.",
                "te": "చేతి తొడుగులు ధరించండి; మందు పిచికారీ చేసిన పొలంలో పశువులను మేపవద్దు."
            }
        },
        "safety_precautions": {
            "en": "Do not enter sprayed field for 24 hours. Wash spray equipment away from open drinking wells.",
            "te": "పిచికారీ చేసిన 24 గంటల వరకు పొలంలోకి వెళ్లవద్దు. తాగునీటి బావులకు దూరంగా స్ప్రేయర్లను కడగండి."
        }
    },

    "Pink Bollworm": {
        "disease": "Pink Bollworm",
        "crop": "Cotton",
        "scientific_name": "Pectinophora gossypiella",
        "problem_type": "Insect Pest",
        "affected_part": "Squares, Flowers, Developing Bolls",
        "severity": "High",
        "what_is_problem": {
            "en": "Pink Bollworm is a monophagous invasive pest of cotton. Young larvae bore into developing flower buds (forming 'rosette' flowers) and bolls. Inside bolls, larvae feed on developing seeds and lint, causing premature boll drop, locule damage, fiber staining, and 30-60% yield and quality loss in Bt and non-Bt cotton.",
            "te": "గులాబీ రంగు పురుగు పత్తి పంటను తీవ్రంగా ఆశించే ప్రధాన కీటకం. లార్వాలు మొగ్గలు, పువ్వులలోకి ప్రవేశించి పువ్వులు విచ్చుకోకుండా 'రోసెట్' (గులాబీ మొగ్గ) మాదిరిగా చేస్తాయి. కాయల లోపలికి చొరబడి గింజలను మరియు దూదిని తినివేయడం వల్ల కాయలు రాలిపోతాయి, దూది నాణ్యత దెబ్బతిని 30-60% వరకు దిగుబడి నష్టం కలుగుతుంది."
        },
        "why_it_occurs": {
            "en": "Monoculture of cotton, continuous availability of fruiting bodies due to ratoon/extended cropping, night temperatures between 20-30°C, and failure to install pheromone monitoring traps early in the season allow undetected moth populations to multiply.",
            "te": "పత్తి పంటను పొడిగించడం (రటూన్ సాగు), సంవత్సరం పొడవునా పత్తి సాగు చేయడం, 20-30°C రాత్రి ఉష్ణోగ్రతలు మరియు ప్రారంభంలో లింగాకర్షక బుట్టలు పెట్టకపోవడం వల్ల పురుగు ఉధృతి తీవ్రమవుతుంది."
        },
        "immediate_action_steps": {
            "en": [
                "Install 8 to 10 pheromone traps per acre with Gossyplure septa to monitor male moth catches.",
                "Collect and destroy rosette flowers and dropped bolls containing larvae into deep pits.",
                "Release Trichogramma bactrae egg parasitoid @ 60,000 per acre if trap catches exceed 8 moths/trap/night for 3 consecutive days.",
                "Avoid spraying non-selective broad-spectrum synthetic pyrethroids which flare up whiteflies and bollworms.",
                "Consult the local cotton scientist if green boll sampling reveals >10% infestation."
            ],
            "te": [
                "ఎకరాకు 8 నుండి 10 గోసిప్లూరే లింగాకర్షక బుట్టలను అమర్చి రెక్కల పురుగుల ఉధృతిని గమనించండి.",
                "రోసెట్ పువ్వులు మరియు రాలిన కాయలను ఏరివేసి లోతైన గుంతలలో పాతిపెట్టండి.",
                "వరుసగా 3 రోజులు బుట్టకు 8 పురుగులు పడితే ఎకరాకు 60,000 ట్రైకోగ్రామా బాక్ట్రే గుడ్ల పరాన్నజీవులను విడుదల చేయండి.",
                "తెల్లదోమ ఉధృతి పెంచే సింథటిక్ పైరెథ్రాయిడ్స్ మందులను విచక్షణారహితంగా వాడవద్దు.",
                "పచ్చి కాయలలో 10% కంటే ఎక్కువ పురుగు కనిపిస్తే శాస్త్రవేత్తలను సంప్రదించండి."
            ]
        },
        "action_urgency": {
            "en": "High Urgency: Inspect green bolls immediately and commence mass trapping and biocontrol within 24 to 48 hours.",
            "te": "అత్యవసర చర్య అవసరం: 24 నుండి 48 గంటల్లోగా లింగాకర్షక బుట్టలు అమర్చి నివారణ చర్యలు చేపట్టాలి."
        },
        "prevention_steps": {
            "en": [
                "Sow short-duration (140-160 days) hybrids recommended by agricultural universities.",
                "Strictly avoid extending cotton crop beyond December/January (no ratoon crop).",
                "Plant refuge non-Bt cotton rows (5 rows around boundary or 20% refuge) to delay pest resistance.",
                "Handpick and destroy early rosette flowers during flowering stage.",
                "Use high-quality certified delta seeds with insect-resistant traits."
            ],
            "te": [
                "వ్యవసాయ విశ్వవిద్యాలయాలు సిఫారసు చేసిన స్వల్పకాలిక (140-160 రోజులు) రకాలను సాగు చేయండి.",
                "జనవరి దాటిన తర్వాత పంటను పొడిగించవద్దు (రటూన్ సాగు అస్సలు చేయవద్దు).",
                "పంట చుట్టూ నాన్-బిటి పత్తి మొక్కలను నాటండి.",
                "పూత దశలో కనిపించే రోసెట్ పువ్వులను ఎప్పటికప్పుడు చేతులతో ఏరి నాశనం చేయండి.",
                "ధృవీకరించబడిన నాణ్యమైన విత్తనాలను మాత్రమే వాడండి."
            ]
        },
        "next_season_prevention": {
            "en": "Terminate cotton crop cleanly by January, graze cattle on leftovers, and practice deep summer plowing to kill diapausing pupae in soil crevices.",
            "te": "జనవరి నాటికి పంటను పూర్తి చేసి పశువులను మేపండి. వేసవిలో లోతు దుక్కులు చేసి నేలలోని కోశస్థ దశలను ఎండ్రబెట్టి నాశనం చేయండి."
        },
        "organic_management": {
            "en": "Spray 5% Neem Seed Kernel Extract (NSKE) or Azadirachtin 1500 ppm @ 5ml/L water at squaring stage.",
            "te": "మొగ్గ దశలో 5% వేప గింజల కషాయం లేదా అజాడిరక్టిన్ 1500 ppm @ 5 మి.లీ. లీటరు నీటికి కలిపి పిచికారీ చేయండి."
        },
        "biological_control": {
            "en": "Release egg parasitoids Trichogramma bactrae @ 60,000/acre at weekly intervals 3 times.",
            "te": "ట్రైకోగ్రామా బాక్ట్రే గుడ్ల పరాన్నజీవులను ఎకరాకు 60,000 చొప్పున వారం వ్యవధిలో 3 సార్లు విడుదల చేయండి."
        },
        "cultural_control": {
            "en": "Synchronized sowing across village, manual destruction of rosette flowers, and timely crop termination.",
            "te": "గ్రామంలో రైతులందరూ ఒకేసారి విత్తుకోండి, రోసెట్ పువ్వులను నాశనం చేయండి మరియు సరైన సమయంలో పంటను ముగించండి."
        },
        "chemical_control": {
            "has_verified_chemical": True,
            "product": {
                "en": "Chlorpyrifos 20% EC or Profenofos 50% EC",
                "te": "క్లోరిపైరిఫాస్ 20% EC లేదా ప్రొఫెనోఫాస్ 50% EC"
            },
            "dosage": {
                "en": "Chlorpyrifos 20% EC @ 2.5ml/L water OR Profenofos 50% EC @ 2ml/L water",
                "te": "క్లోరిపైరిఫాస్ 20% EC @ 2.5 మి.లీ./లీటర్ నీటికి లేదా ప్రొఫెనోఫాస్ 50% EC @ 2 మి.లీ./లీటర్ నీటికి"
            },
            "water_quantity": {
                "en": "200 to 250 Litres of spray solution per acre",
                "te": "ఎకరాకు 200 నుండి 250 లీటర్ల పిచికారీ ద్రావణం"
            },
            "application_method": {
                "en": "Targeted foliar spray covering flowering buds and young green bolls during evening hours",
                "te": "సాయంత్రం వేళల్లో మొగ్గలు మరియు పచ్చి కాయలు తడిసేలా పిచికారీ చేయండి"
            },
            "waiting_period_phi": {
                "en": "30 days before harvest",
                "te": "పంట కోతకు ముందు 30 రోజుల వేచిఉండే కాలం (PHI)"
            },
            "safety_precaution": {
                "en": "High toxicity organophosphate: strictly use chemical-resistant respirator and coveralls.",
                "te": "అధిక విషపూరితమైనది: తప్పనిసరిగా రక్షణ మాస్క్ మరియు చేతి తొడుగులు ధరించండి."
            }
        },
        "safety_precautions": {
            "en": "Do not spray near bee hives or fish ponds. Dispose of empty containers safely by puncturing and burying.",
            "te": "తేనెటీగల పెట్టెలు మరియు చేపల చెరువుల దగ్గర పిచికారీ చేయవద్దు. ఖాళీ డబ్బాలను పగలగొట్టి పాతిపెట్టండి."
        }
    },

    "Thrips": {
        "disease": "Thrips",
        "crop": "Chilli",
        "scientific_name": "Scirtothrips dorsalis",
        "problem_type": "Insect Pest",
        "affected_part": "Leaves, Growing Tips, Flowers",
        "severity": "Moderate to High",
        "what_is_problem": {
            "en": "Chilli Thrips are tiny, slender, yellow-brown insects that lacerate leaf tissues and suck sap from the lower surface of tender leaves and growing tips. Affected leaves curl upwards ('boat-shaped' curling), develop bronze-brown patches underneath, and flower buds wither and drop. Severe infestation causes significant stunting and 30-50% pod yield loss, while also transmitting dangerous viral diseases.",
            "te": "మిరపలో తామర పురుగులు (థ్రిప్స్) లేత ఆకుల అడుగు భాగాన రసాన్ని పీల్చే అత్యంత సూక్ష్మమైన పురుగులు. వీటి దాడి వల్ల ఆకుల అంచులు పైకి దోనె మాదిరిగా ముడుచుకుంటాయి (పై ముడత), ఆకుల అడుగున ఇటుక రంగు లేదా గోధుమ రంగు మచ్చలు ఏర్పడతాయి. పూత రాలిపోయి, కాయల పరిమాణం తగ్గి 30-50% వరకు దిగుబడి నష్టం కలుగుతుంది."
        },
        "why_it_occurs": {
            "en": "Dry, hot weather with intermittent sunshine, relative humidity between 50-70%, absence of heavy rainfall, and excessive nitrogenous fertilizer application trigger explosive multiplication of thrips populations.",
            "te": "పొడి వాతావరణం, ఎండ తీవ్రత, గాలిలో తక్కువ తేమ, వర్షాలు లేకపోవడం మరియు సిఫారసు కంటే ఎక్కువ యూరియా వాడటం వల్ల తామర పురుగుల సంఖ్య విపరీతంగా పెరుగుతుంది."
        },
        "immediate_action_steps": {
            "en": [
                "Install 20 to 25 blue sticky traps per acre at crop canopy height to catch flying adults.",
                "Perform light overhead sprinkler irrigation to wash off thrips nymphs from leaf undersides.",
                "Spray 5% Neem Seed Kernel Extract (NSKE) or Neem Oil @ 5ml/L water immediately.",
                "Stop excessive urea application; apply potash to harden succulent leaf tissues.",
                "Scout twice weekly; if upward curling is severe, consult agricultural officer."
            ],
            "te": [
                "ఎకరాకు 20 నుండి 25 నీలి రంగు జిగురు అట్టలను పైరు ఎత్తులో అమర్చి పురుగులను బంధించండి.",
                "స్ప్రింక్లర్ల ద్వారా నీరు చిలకరించడం వల్ల ఆకుల అడుగున ఉన్న పురుగులు రాలిపోతాయి.",
                "వెంటనే 5% వేప గింజల కషాయం లేదా వేప నూనె 5 మి.లీ. లీటరు నీటికి కలిపి పిచికారీ చేయండి.",
                "యూరియా వాడకాన్ని తగ్గించి, పొటాష్ ఎరువును వేయడం ద్వారా ఆకులు గట్టిపడేలా చేయండి.",
                "వారానికి రెండుసార్లు పరిశీలించి పైముడత తీవ్రంగా ఉంటే వ్యవసాయ అధికారిని సంప్రదించండి."
            ]
        },
        "action_urgency": {
            "en": "Moderate to High Urgency: Install blue sticky traps within 24 hours and begin spray within 2 to 3 days.",
            "te": "అత్యవసర చర్య అవసరం: 24 గంటల్లోగా నీలి జిగురు అట్టలను ఏర్పాటు చేసి, 2-3 రోజుల్లో పిచికారీ చేయాలి."
        },
        "prevention_steps": {
            "en": [
                "Grow barrier crops like maize, sorghum, or pearl millet (3-4 dense rows) around the chilli plot.",
                "Treat nursery seed with Imidacloprid 70% WS @ 5g/kg seed before raising seedlings.",
                "Maintain clean bunds free from weed hosts like Parthenium and Amaranthus.",
                "Ensure balanced NPK fertilization avoiding luxury nitrogen consumption.",
                "Use silver-black reflective plastic mulch to disorient incoming flying thrips."
            ],
            "te": [
                "మిరప చేను చుట్టూ 3-4 వరుసలలో జొన్న లేదా మొక్కజొన్నను సరిహద్దు పంటగా సాగు చేయండి.",
                "నారు పోసే ముందు కిలో విత్తనానికి ఇమిడాక్లోప్రిడ్ 70% WS @ 5 గ్రా. కలిపి విత్తన శుద్ధి చేయండి.",
                "గట్లపై ఉండే వయ్యారిభామ, కలుపు మొక్కలను పూర్తిగా తొలగించి శుభ్రంగా ఉంచండి.",
                "సిఫారసు చేసిన మేరకు సమతుల్య ఎరువులను మాత్రమే వాడండి.",
                "సిల్వర్-బ్లాక్ మల్చింగ్ షీట్లను వాడటం వల్ల పురుగులు చేనులోకి రాకుండా నిరోధించవచ్చు."
            ]
        },
        "next_season_prevention": {
            "en": "Rotate chilli with non-solanaceous crops (pulses, cereals), deep plow after harvest, and raise nursery under 40-mesh insect-proof net.",
            "te": "పంట మార్పిడిలో అపరాలు లేదా తృణధాన్యాలను సాగు చేయండి. నారుమడిని 40 మెష్ దోమతెర కింద పెంచండి."
        },
        "organic_management": {
            "en": "Spray 5% Neem Seed Kernel Extract (NSKE) or Fish Oil Rosin Soap (FORS) @ 25g/L water.",
            "te": "5% వేప గింజల కషాయం లేదా ఫిష్ ఆయిల్ రోసిన్ సోప్ (FORS) 25 గ్రా. లీటరు నీటికి కలిపి పిచికారీ చేయండి."
        },
        "biological_control": {
            "en": "Install blue sticky traps (25/acre) and conserve predatory anthocorid bugs and green lacewings.",
            "te": "ఎకరాకు 25 నీలి జిగురు అట్టలను అమర్చండి మరియు సహజ మిత్రపురుగులైన క్రైసోపాను కాపాడుకోండి."
        },
        "cultural_control": {
            "en": "Grow border barrier crops (sorghum/maize) and install reflective silver mulch.",
            "te": "చేను చుట్టూ జొన్న/మొక్కజొన్న రక్షణ పంటలు వేయండి మరియు సిల్వర్ మల్చింగ్ వాడండి."
        },
        "chemical_control": {
            "has_verified_chemical": True,
            "product": {
                "en": "Fipronil 5% SC or Spinetoram 11.7% SC",
                "te": "ఫిప్రోనిల్ 5% SC లేదా స్పినెటోరమ్ 11.7% SC"
            },
            "dosage": {
                "en": "Fipronil 5% SC @ 2ml/L water OR Spinetoram 11.7% SC @ 1ml/L water",
                "te": "ఫిప్రోనిల్ 5% SC @ 2 మి.లీ./లీటర్ నీటికి లేదా స్పినెటోరమ్ 11.7% SC @ 1 మి.లీ./లీటర్ నీటికి"
            },
            "water_quantity": {
                "en": "200 Litres of spray solution per acre",
                "te": "ఎకరాకు 200 లీటర్ల పిచికారీ ద్రావణం"
            },
            "application_method": {
                "en": "Fine mist foliar spray with hollow cone nozzle targeting the undersides of tender foliage",
                "te": "హాలో కోన్ నాజిల్‌తో ఆకుల అడుగు భాగం పూర్తిగా తడిసేలా పిచికారీ చేయండి"
            },
            "waiting_period_phi": {
                "en": "7 days for Fipronil; 3 days for Spinetoram",
                "te": "పంట కోతకు ముందు 7 రోజుల (ఫిప్రోనిల్) లేదా 3 రోజుల (స్పినెటోరమ్) వేచిఉండే కాలం"
            },
            "safety_precaution": {
                "en": "Toxic to bees: avoid spraying during active foraging hours in morning.",
                "te": "తేనెటీగలకు హానికరం: ఉదయం పూట పువ్వులపై తేనెటీగలు ఉన్నప్పుడు పిచికారీ చేయవద్దు."
            }
        },
        "safety_precautions": {
            "en": "Rotate chemical groups across sprays to prevent rapid insecticide resistance.",
            "te": "పురుగులకు మందులపై రోగనిరోధక శక్తి రాకుండా ఉండటానికి మందుల గ్రూపులను మార్చి మార్చి పిచికారీ చేయండి."
        }
    },

    "Early Blight": {
        "disease": "Early Blight",
        "crop": "Tomato",
        "scientific_name": "Alternaria solani",
        "problem_type": "Fungal Disease",
        "affected_part": "Leaves, Stems, Fruit calyx",
        "severity": "Moderate to High",
        "what_is_problem": {
            "en": "Early Blight is a common fungal disease of tomato and potato caused by Alternaria solani. It manifests as dark brown to black spots with characteristic concentric rings ('target-board' appearance) on older lower leaves. Affected leaves turn yellow, chlorotic, and wither dry. Severe leaf drop exposes fruits to sunscald and damages fruit stems, causing 20-40% yield loss.",
            "te": "టమోటాలో ముందస్తు ఆకుమచ్చ తెగులు (ఆల్టర్నేరియా ఎర్లీ బ్లైట్) ప్రధాన శిలీంధ్ర వ్యాధి. మొదట మొక్క క్రింది భాగంలోని ముదిరిన ఆకులపై గుండ్రని ఉంగరాల వంటి (టార్గెట్ బోర్డు లాంటి) గోధుమ రంగు మచ్చలు ఏర్పడతాయి. ఆకులు పసుపు రంగులోకి మారి ఎండి రాలిపోతాయి. ఆకులు రాలిపోవడం వల్ల కాయలపై ఎండ ప్రభావం పడి నాణ్యత తగ్గి 20-40% దిగుబడి నష్టం కలుగుతుంది."
        },
        "why_it_occurs": {
            "en": "Alternating periods of wet and dry weather, temperatures between 24-29°C, dew persistence, heavy canopy shading, and poor soil nutrition (low nitrogen/potassium) favor rapid conidial germination and spread.",
            "te": "తేమ మరియు పొడి వాతావరణం మారి మారి రావడం, 24-29°C ఉష్ణోగ్రతలు, ఆకులపై మంచు ఉండటం, మరియు నేలలో తగినంత బలం లేకపోవడం వల్ల ఈ తెగులు వేగంగా వ్యాపిస్తుంది."
        },
        "immediate_action_steps": {
            "en": [
                "Prune and destroy infected lower leaves touching the soil surface.",
                "Switch from overhead sprinkler to drip irrigation to keep tomato foliage dry.",
                "Stake plants to elevate fruit and lower canopy above moist ground.",
                "Apply balanced potassium fertilizer to strengthen cell walls against fungal enzymes.",
                "Consult KVK or MAO if concentric target spots begin spreading to upper green leaves."
            ],
            "te": [
                "నేలను తాకుతున్న తెగులు సోకిన క్రింది ఆకులను తుంచి నాశనం చేయండి.",
                "ఆకులపై నీరు పడకుండా డ్రిప్ పద్ధతి ద్వారా మాత్రమే నీరు అందించండి.",
                "మొక్కలను కర్రలతో కట్టి పైకి నిలబెట్టండి (స్టేకింగ్).",
                "ఆకులలో రోగనిరోధక శక్తిని పెంచడానికి సమతుల్య పొటాష్ ఎరువును అందించండి.",
                "మచ్చలు పై ఆకులకు విస్తరిస్తుంటే వెంటనే వ్యవసాయ అధికారిని సంప్రదించండి."
            ]
        },
        "action_urgency": {
            "en": "Moderate Urgency: Prune infected foliage and apply protective fungicide within 48 to 72 hours.",
            "te": "మధ్యస్థ అత్యవసరం: తెగులు సోకిన ఆకులను తొలగించి 48 నుండి 72 గంటల్లోగా నివారణ చర్యలు చేపట్టాలి."
        },
        "prevention_steps": {
            "en": [
                "Sow tolerant tomato hybrids such as Arka Rakshak, Arka Samrat, or US-440.",
                "Treat seed with Thiram or Captan @ 3g/kg seed before raising nursery.",
                "Stake indeterminate tomato varieties to maintain good aeration between rows.",
                "Mulch the soil bed with straw or silver plastic to prevent soil splash onto lower foliage.",
                "Maintain 3-year crop rotation avoiding solanaceous crops (brinjal, chilli, potato)."
            ],
            "te": [
                "అర్కా రక్షక్, అర్కా సామ్రాట్ వంటి తెగులు తట్టుకునే రకాలను సాగు చేయండి.",
                "నారు పోసే ముందు కిలో విత్తనానికి థైరమ్ లేదా కాప్టాన్ @ 3 గ్రా. కలిపి విత్తన శుద్ధి చేయండి.",
                "గాలి వెలుతురు బాగా ప్రసరించేలా మొక్కలకు కర్రల సాయంతో స్టేకింగ్ చేయండి.",
                "నేలపై ఎండుగడ్డి లేదా మల్చింగ్ షీట్ వేయడం ద్వారా మట్టి ఆకులకు తగలకుండా చూడండి.",
                "మిరప, వంకాయ, బంగాళాదుంప కాకుండా ఇతర పంటలతో 3 సంవత్సరాల పంట మార్పిడి చేయండి."
            ]
        },
        "next_season_prevention": {
            "en": "Deep summer plowing and strict avoidance of solanaceous volunteers or debris on field margins.",
            "te": "వేసవిలో లోతు దుక్కులు చేసి తెగులు శేషాలను ఎండబెట్టండి. పొలం గట్లపై ఉన్న పాత మొక్కలను నాశనం చేయండి."
        },
        "organic_management": {
            "en": "Foliar spray with Copper Oxychloride 50% WP @ 2.5g/L or 1% Bordeaux mixture.",
            "te": "కాపర్ ఆక్సిక్లోరైడ్ (COC) 2.5 గ్రా. లేదా 1% బోర్డో మిశ్రమాన్ని పిచికారీ చేయండి."
        },
        "biological_control": {
            "en": "Foliar application of Pseudomonas fluorescens @ 10g/L or Trichoderma harzianum @ 5g/L water.",
            "te": "సూడోమోనాస్ ఫ్లోరోసెన్స్ 10 గ్రా. లేదా ట్రైకోడెర్మా హార్జియానమ్ 5 గ్రా. లీటరు నీటికి కలిపి పిచికారీ చేయండి."
        },
        "cultural_control": {
            "en": "Staking of vines, pruning lower foliage touching soil, and drip irrigation.",
            "te": "స్టేకింగ్ పద్ధతి, క్రింది ఆకులను కత్తిరించడం మరియు డ్రిప్ సేద్యం పాటించండి."
        },
        "chemical_control": {
            "has_verified_chemical": True,
            "product": {
                "en": "Mancozeb 75% WP or Chlorothalonil 75% WP",
                "te": "మాంకోజెబ్ 75% WP లేదా క్లోరోథలోనిల్ 75% WP"
            },
            "dosage": {
                "en": "Mancozeb 75% WP @ 2.5g/L water OR Chlorothalonil 75% WP @ 2g/L water",
                "te": "మాంకోజెబ్ 75% WP @ 2.5 గ్రా./లీటర్ నీటికి లేదా క్లోరోథలోనిల్ 75% WP @ 2 గ్రా./లీటర్ నీటికి"
            },
            "water_quantity": {
                "en": "200 Litres of spray solution per acre",
                "te": "ఎకరాకు 200 లీటర్ల పిచికారీ ద్రావణం"
            },
            "application_method": {
                "en": "Uniform canopy spray covering lower stems and leaf undersides",
                "te": "మొక్క మొదళ్ళు మరియు ఆకులు పూర్తిగా తడిసేలా పిచికారీ చేయండి"
            },
            "waiting_period_phi": {
                "en": "7 to 10 days before harvesting fruits",
                "te": "కాయలు కోయడానికి ముందు 7 నుండి 10 రోజుల వేచిఉండే కాలం (PHI)"
            },
            "safety_precaution": {
                "en": "Do not harvest ripe tomatoes on the day of chemical application.",
                "te": "మందు పిచికారీ చేసిన రోజున పండిన టమోటాలను కోయవద్దు."
            }
        },
        "safety_precautions": {
            "en": "Wash picked vegetables thoroughly before consumption. Wear eye goggles during spray preparation.",
            "te": "కోసిన కూరగాయలను శుభ్రంగా కడగండి. మందు కలిపేటప్పుడు కంటి అద్దాలు ధరించండి."
        }
    },

    "Sheath Blight": {
        "disease": "Sheath Blight",
        "crop": "Rice",
        "scientific_name": "Rhizoctonia solani",
        "problem_type": "Fungal Disease",
        "affected_part": "Leaf Sheaths, Upper Leaves",
        "severity": "High",
        "what_is_problem": {
            "en": "Rice Sheath Blight is caused by the soil-borne fungus Rhizoctonia solani. It manifests as oval, greenish-grey water-soaked spots with dark brown margins on leaf sheaths near the water level, which coalesce into large snake-skin patterns. It spreads upward to flag leaves, causing lodging, unfilled grains, and 20-50% yield reduction under humid canopy conditions.",
            "te": "వరిలో పాముపొడ తెగులు (షీత్ బ్లైట్) అనేది రైజోక్టోనియా సొలానీ అనే నేల ద్వారా వ్యాపించే శిలీంధ్రం వల్ల వస్తుంది. నీటి మట్టానికి దగ్గరగా ఉన్న ఆకు తొడుగులపై బూడిద-గోధుమ రంగు పాము చర్మం లాంటి మచ్చలు ఏర్పడతాయి. తెగులు పైకి పాకి జెండా ఆకు వరకు చేరితే మొక్కలు పడిపోయి, గింజలు తాలుగా మారి 20-50% దిగుబడి నష్టం కలుగుతుంది."
        },
        "why_it_occurs": {
            "en": "Warm humid conditions (temperatures 28-32°C, relative humidity 85-100%), heavy plant canopy density, excessive nitrogen use, and sclerotia floating on standing irrigation water favor disease development.",
            "te": "అధిక వేడి మరియు తేమ (28-32°C, 85-100% తేమ), దట్టంగా నాట్లు వేయడం, మితిమీరిన యూరియా వాడకం మరియు నీటిపై తేలే శిలీంధ్ర గుళికల (స్క్లెరోషియా) వల్ల ఈ తెగులు తీవ్రమవుతుంది."
        },
        "immediate_action_steps": {
            "en": [
                "Drain standing field water completely and allow soil surface to dry for 2 to 3 days.",
                "Stop all nitrogenous fertilizer top dressing immediately.",
                "Clear field bunds of weed hosts and improve canopy ventilation.",
                "Remove floating sclerotial bodies and infected dead tillers away from water flow.",
                "Consult local agricultural officer if lesions reach the top third of the plant canopy."
            ],
            "te": [
                "పొలంలోని నిలిచిన నీటిని పూర్తిగా తీసివేసి 2-3 రోజుల పాటు ఆరబెట్టండి.",
                "యూరియా ఎరువును పైపాటుగా వేయడం వెంటనే నిలిపివేయండి.",
                "గట్లపై ఉన్న కలుపు మొక్కలను తొలగించి గాలి వెలుతురు ప్రసరించేలా చూడండి.",
                "నీటిపై తేలే తెగులు గుళికలను మరియు ఎండిన పిలకలను తొలగించండి.",
                "తెగులు మొక్క పైభాగానికి పాకుతుంటే వెంటనే వ్యవసాయ అధికారిని సంప్రదించండి."
            ]
        },
        "action_urgency": {
            "en": "High Urgency: Apply targeted sheath fungicide within 24 to 48 hours of detecting lesions moving above water level.",
            "te": "అత్యవసర చర్య అవసరం: మచ్చలు పైకి పాకుతున్నట్లు గమనించిన 24 నుండి 48 గంటల్లోగా నివారణ చర్యలు చేపట్టాలి."
        },
        "prevention_steps": {
            "en": [
                "Avoid dense planting; maintain 15x15 cm or 20x15 cm hill spacing.",
                "Apply potassium in two split doses to enhance sheath strength.",
                "Apply balanced nitrogen in 3-4 splits rather than large single applications.",
                "Skim and destroy floating sclerotia during final puddled leveling before transplanting.",
                "Avoid using irrigation runoff from infected upstream fields."
            ],
            "te": [
                "దట్టంగా కాకుండా 15x15 సెం.మీ లేదా 20x15 సెం.మీ దూరం పాటించండి.",
                "మొక్కల తొడుగులు బలంగా ఉండటానికి పొటాష్‌ను రెండు భాగాలుగా వేయండి.",
                "యూరియాను ఒకేసారి వేయకుండా 3-4 సార్లుగా విభజించి వేయండి.",
                "దమ్ము చేసే సమయంలో నీటిపై తేలే నల్లని శిలీంధ్ర గుళికలను జల్లెడతో తీసి నాశనం చేయండి.",
                "తెగులు సోకిన పొలాల నుండి వచ్చే మురుగు నీటిని మీ పొలంలోకి రాకుండా చూడండి."
            ]
        },
        "next_season_prevention": {
            "en": "Deep summer plowing to bury sclerotia deeply, and crop rotation with non-host legumes or green manures.",
            "te": "వేసవిలో లోతు దుక్కులు చేసి తెగులు గుళికలను భూమిలో పూడ్చిపెట్టండి. పిల్లిపెసర, జీలుగ వంటి పచ్చిరొట్ట పైర్లతో పంట మార్పిడి చేయండి."
        },
        "organic_management": {
            "en": "Spray Pseudomonas fluorescens @ 10g/L or 5% Neem Seed Kernel Extract (NSKE) at tillering.",
            "te": "పిలక దశలో సూడోమోనాస్ ఫ్లోరోసెన్స్ 10 గ్రా. లేదా 5% వేప గింజల కషాయం పిచికారీ చేయండి."
        },
        "biological_control": {
            "en": "Foliar spray with Trichoderma viride or Bacillus subtilis @ 5g/L water at early sheath infection.",
            "te": "ట్రైకోడెర్మా విరిడె లేదా బాసిల్లస్ సబ్టిలిస్ 5 గ్రాములు లీటరు నీటికి కలిపి పిచికారీ చేయండి."
        },
        "cultural_control": {
            "en": "Alternate wetting and drying (AWD), wider spacing, and balanced potash application.",
            "te": "ఆరుతడి పద్ధతి, మొక్కల మధ్య తగిన దూరం మరియు పొటాష్ సమతుల్య వాడకం."
        },
        "chemical_control": {
            "has_verified_chemical": True,
            "product": {
                "en": "Hexaconazole 5% SC or Validamycin 3% L",
                "te": "హెక్సాకొనాజోల్ 5% SC లేదా వాలిడామైసిన్ 3% L"
            },
            "dosage": {
                "en": "Hexaconazole 5% SC @ 2ml/L water OR Validamycin 3% L @ 2ml/L water",
                "te": "హెక్సాకొనాజోల్ 5% SC @ 2 మి.లీ./లీటర్ నీటికి లేదా వాలిడామైసిన్ 3% L @ 2 మి.లీ./లీటర్ నీటికి"
            },
            "water_quantity": {
                "en": "200 Litres of spray solution per acre",
                "te": "ఎకరాకు 200 లీటర్ల పిచికారీ ద్రావణం"
            },
            "application_method": {
                "en": "Direct the spray nozzle toward the base of the plant hills wetting leaf sheaths",
                "te": "మొక్కల మొదళ్ళు మరియు ఆకు తొడుగులు పూర్తిగా తడిసేలా పిచికారీ నాజిల్‌ను క్రిందికి ఉంచి పిచికారీ చేయండి"
            },
            "waiting_period_phi": {
                "en": "30 days before harvest",
                "te": "పంట కోతకు ముందు 30 రోజుల వేచిఉండే కాలం"
            },
            "safety_precaution": {
                "en": "Wear protective boots and gloves when walking through paddy fields.",
                "te": "వరి పొలంలో తిరిగేటప్పుడు బూట్లు మరియు చేతి తొడుగులు ధరించండి."
            }
        },
        "safety_precautions": {
            "en": "Do not release spray wash water into public canals or fish ponds.",
            "te": "స్ప్రేయర్ కడిగిన నీటిని చేపల చెరువులు లేదా తాగునీటి కాలువల్లోకి వదలవద్దు."
        }
    },

    "Brown Planthopper": {
        "disease": "Brown Planthopper",
        "crop": "Rice",
        "scientific_name": "Nilaparvata lugens",
        "problem_type": "Insect Pest",
        "affected_part": "Stem base, Tillers",
        "severity": "High",
        "what_is_problem": {
            "en": "Brown Planthopper (BPH) is a severe sucking pest of paddy. Both nymphs and adults congregate at the base of the plant and suck plant sap. In severe cases, tillers dry up rapidly in circular patches, turning straw-colored in a condition known as 'hopperburn'. It causes complete crop failure and lodging within days.",
            "te": "వరిలో సుడిదోమ (బ్రౌన్ ప్లాంట్‌హాపర్) అత్యంత నష్టం కలిగించే రసం పీల్చే పురుగు. పిల్ల మరియు పెద్ద పురుగులు మొక్క మొదళ్ళ వద్ద గుంపులుగా చేరి రసాన్ని పీల్చుతాయి. దీనివల్ల పైరు వలయాకారంలో ఎండిపోయి ఎండిన గడ్డి రంగులోకి మారుతుంది. దీనిని 'సుడిదోమ లేదా హాప్పర్‌బర్న్' అంటారు. తెగులు ఉధృతమైతే పంట పూర్తిగా నేలమట్టమవుతుంది."
        },
        "why_it_occurs": {
            "en": "Continuous submergence of fields, high relative humidity inside dense canopies, excessive urea use, close planting, and indiscriminate use of synthetic pyrethroids (which kill natural predators like spiders and mirid bugs) trigger resurgence.",
            "te": "పొలంలో నిరంతరం నీరు నిలకడగా ఉండటం, దట్టంగా నాట్లు వేయడం, అధిక నత్రజని వాడకం మరియు విచక్షణారహితంగా పురుగుమందులు పిచికారీ చేయడం వల్ల సహజ శత్రువులైన సాలెపురుగులు నశించి సుడిదోమ తీవ్రమవుతుంది."
        },
        "immediate_action_steps": {
            "en": [
                "Form 'alleyways' (pathways of 30 cm after every 2 meters) to let sunlight and air penetrate the canopy.",
                "Drain water completely from the field for 3 to 4 days to expose the base of the hills.",
                "Stop applying urea and all synthetic pyrethroid sprays immediately.",
                "Conserve natural predators like wolf spiders, mirid bugs, and rove beetles.",
                "Consult the Mandal Agricultural Officer if hopper count exceeds 10 per hill."
            ],
            "te": [
                "గాలి, వెలుతురు సోకేలా ప్రతి 2 మీటర్లకు 30 సెం.మీ. వెడల్పుతో బాటలు (కాలిబాటలు) తీయండి.",
                "పొలంలోని నీటిని 3-4 రోజుల పాటు పూర్తిగా తీసివేసి ఆరబెట్టండి.",
                "యూరియా మరియు సింథటిక్ పైరెథ్రాయిడ్స్ మందుల వాడకాన్ని వెంటనే ఆపండి.",
                "మిత్రపురుగులైన సాలెపురుగులు, మిరిడ్ బగ్స్‌ను కాపాడుకోండి.",
                "దుబ్బుకు 10 కంటే ఎక్కువ దోమలు కనిపిస్తే వెంటనే వ్యవసాయ అధికారిని సంప్రదించండి."
            ]
        },
        "action_urgency": {
            "en": "High Urgency: Form alleyways and drain field within 24 hours; commence spray if ETL (>10 hoppers/hill) is crossed.",
            "te": "అత్యవసర చర్య అవసరం: 24 గంటల్లోగా బాటలు తీసి నీరు తీసివేయాలి; ఆర్థిక నష్ట పరిమితి దాటితే వెంటనే మందు పిచికారీ చేయాలి."
        },
        "prevention_steps": {
            "en": [
                "Grow resistant varieties such as MTU 1001, NLR 33358, or MTU 1075.",
                "Form alleyways of 30 cm after every 2-3 meters at transplanting.",
                "Adopt Alternate Wetting and Drying (AWD) rather than continuous standing water.",
                "Apply balanced potash and split doses of nitrogen.",
                "Avoid using synthetic pyrethroids like Cypermethrin or Deltamethrin in paddy."
            ],
            "te": [
                "MTU 1001, NLR 33358, MTU 1075 వంటి సుడిదోమను తట్టుకునే రకాలను సాగు చేయండి.",
                "నాట్లు వేసేటప్పుడే ప్రతి 2-3 మీటర్లకు 30 సెం.మీ. బాటలు తీయండి.",
                "నిరంతరం నీరు ఉంచకుండా ఆరుతడి పద్ధతిని పాటించండి.",
                "పొటాష్ సమతుల్యంగా వేసి, నత్రజనిని వాయిదాల పద్ధతిలో వేయండి.",
                "వరిలో సైపర్‌మెథ్రిన్ లేదా డెల్టామెథ్రిన్ వంటి మందులను ఎట్టిపరిస్థితుల్లోనూ వాడవద్దు."
            ]
        },
        "next_season_prevention": {
            "en": "Crop rotation with pulse crops, deep plowing of paddy stubbles, and synchronous planting across the village.",
            "te": "వరి తర్వాత పిల్లిపెసర, మినుము వంటి అపరాలు సాగు చేయండి. పంట కోసిన తర్వాత మోడులను లోతుగా దున్నండి."
        },
        "organic_management": {
            "en": "Spray 5% Neem Seed Kernel Extract (NSKE) or Neem Oil 1500 ppm @ 5ml/L directed at plant bases.",
            "te": "మొక్కల మొదళ్ళు తడిసేలా 5% వేప గింజల కషాయం లేదా వేప నూనె 5 మి.లీ. లీటరు నీటికి కలిపి పిచికారీ చేయండి."
        },
        "biological_control": {
            "en": "Conserve predatory wolf spiders (Lycosa pseudoannulata) and Cyrtorhinus mirid bugs.",
            "te": "పొలంలో ఉండే సాలెపురుగులు మరియు మిరిడ్ బగ్స్ వంటి సహజ శత్రువులను కాపాడుకోండి."
        },
        "cultural_control": {
            "en": "Forming 30 cm alleyways, draining standing water, and avoiding excessive nitrogen.",
            "te": "బాటలు తీయడం, నీరు తీసి ఆరబెట్టడం మరియు యూరియా తగ్గించడం."
        },
        "chemical_control": {
            "has_verified_chemical": True,
            "product": {
                "en": "Trifflumezopyrim 10% SC or Pymetrozine 50% WDG",
                "te": "ట్రైఫ్లూమెజోపైరిమ్ 10% SC లేదా పైమెట్రోజైన్ 50% WDG"
            },
            "dosage": {
                "en": "Trifflumezopyrim 10% SC @ 0.5ml/L water OR Pymetrozine 50% WDG @ 0.6g/L water",
                "te": "ట్రైఫ్లూమెజోపైరిమ్ 10% SC @ 0.5 మి.లీ./లీటర్ నీటికి లేదా పైమెట్రోజైన్ 50% WDG @ 0.6 గ్రా./లీటర్ నీటికి"
            },
            "water_quantity": {
                "en": "200 Litres of spray solution per acre",
                "te": "ఎకరాకు 200 లీటర్ల పిచికారీ ద్రావణం"
            },
            "application_method": {
                "en": "Direct the spray lance to the base of the plants after draining field water",
                "te": "పొలంలోని నీరు తీసివేసిన తర్వాత మొక్కల మొదళ్ళు పూర్తిగా తడిసేలా పిచికారీ చేయండి"
            },
            "waiting_period_phi": {
                "en": "21 to 25 days before harvest",
                "te": "పంట కోతకు ముందు 21 నుండి 25 రోజుల వేచిఉండే కాలం"
            },
            "safety_precaution": {
                "en": "Ensure proper protective clothing and avoid spraying during high wind speeds.",
                "te": "చేతి తొడుగులు ధరించండి. తీవ్రమైన గాలి వీచేటప్పుడు పిచికారీ చేయవద్దు."
            }
        },
        "safety_precautions": {
            "en": "Keep cattle and poultry away from the sprayed field for at least 7 days.",
            "te": "మందు పిచికారీ చేసిన పొలంలో పశువులు, కోళ్లను కనీసం 7 రోజుల పాటు తిరగనివ్వవద్దు."
        }
    },

    "Fall Armyworm": {
        "disease": "Fall Armyworm",
        "crop": "Maize",
        "scientific_name": "Spodoptera frugiperda",
        "problem_type": "Insect Pest",
        "affected_part": "Whorl, Leaves, Cobs",
        "severity": "High",
        "what_is_problem": {
            "en": "Fall Armyworm (FAW) is an invasive voracious caterpillar pest attacking maize. Young larvae scrape leaves creating papery windows. Older larvae feed inside the central whorl, creating large irregular ragged holes and copious sawdust-like fecal frass. Damaged central shoots fail to expand, resulting in 30-60% yield loss and cob damage.",
            "te": "మొక్కజొన్నలో కత్తెర పురుగు (ఫాల్ ఆర్మీవార్మ్) అత్యంత తీవ్రమైన వినాశకర పురుగు. చిన్న లార్వాలు ఆకులపై పచ్చదనాన్ని గీకి తిని తెల్లని పొరలను ఏర్పరుస్తాయి. పెద్ద పురుగులు సుడులలో చేరి ఆకులను కత్తిరించి రంధ్రాలు చేస్తాయి మరియు రంపపు పొట్టు లాంటి విసర్జితాలను వదులుతాయి. దీనివల్ల పైరు ఎదగక కండెలు దెబ్బతిని 30-60% వరకు దిగుబడి నష్టం కలుగుతుంది."
        },
        "why_it_occurs": {
            "en": "Staggered sowing in surrounding areas, monocropping of maize, warm temperatures (25-30°C), absence of intercrops, and failure to apply whorl treatments at seedling stage allow population outbreaks.",
            "te": "రైతులు వేర్వేరు సమయాల్లో మొక్కజొన్న విత్తడం, స్వచ్ఛమైన సాగు, అనుకూల ఉష్ణోగ్రతలు మరియు ప్రారంభ దశలో సుడులలో నివారణ చర్యలు చేపట్టకపోవడం వల్ల ఈ పురుగు ఉధృతమవుతుంది."
        },
        "immediate_action_steps": {
            "en": [
                "Apply dry sand mixed with neem seed powder (9:1 ratio) directly into central leaf whorls.",
                "Handpick and crush egg masses (covered in cream scales) and young caterpillars.",
                "Install 5 pheromone traps per acre to monitor adult moth activity.",
                "Do not spray broad-spectrum insecticides overhead; whorl-directed application is required.",
                "Consult agricultural officer if more than 10-20% of plants show whorl damage."
            ],
            "te": [
                "పొడి ఇసుక మరియు వేప పిండి మిశ్రమాన్ని (9:1 నిష్పత్తిలో) మొక్కల సుడులలో వేయండి.",
                "ఆకుల అడుగున ఉండే గుడ్ల సముదాయాలను మరియు లార్వాలను ఏరి నాశనం చేయండి.",
                "ఎకరాకు 5 లింగాకర్షక బుట్టలను అమర్చి రెక్కల పురుగుల ఉధృతిని గమనించండి.",
                "మందులను పైపైనే పిచికారీ చేయకుండా నేరుగా సుడిలో పడేలా పిచికారీ చేయాలి.",
                "10-20% పైగా మొక్కల సుడులు దెబ్బతింటే వెంటనే వ్యవసాయ అధికారిని సంప్రదించండి."
            ]
        },
        "action_urgency": {
            "en": "High Urgency: Apply whorl treatment within 24 to 48 hours of noticing fresh ragged holes.",
            "te": "అత్యవసర చర్య అవసరం: సుడులలో రంధ్రాలు కనిపించిన 24 నుండి 48 గంటల్లోగా సుడి నివారణ చర్యలు చేపట్టాలి."
        },
        "prevention_steps": {
            "en": [
                "Synchronize planting time across the entire village block within 10-15 days.",
                "Intercrop maize with pulses like cowpea, pigeonpea, or soybean in a 2:1 or 4:2 ratio.",
                "Treat seed with Cyantraniliprole 19.8% + Thiamethoxam 19.8% FS @ 6ml/kg seed.",
                "Erect bird perches @ 10-15 per acre to encourage predatory birds.",
                "Avoid staggered planting and avoid planting sweet corn near grain maize."
            ],
            "te": [
                "గ్రామంలో రైతులందరూ 10-15 రోజుల వ్యవధిలోనే ఒకేసారి విత్తనం వేయాలి.",
                "మొక్కజొన్నలో అలసందలు లేదా కందులను 2:1 లేదా 4:2 నిష్పత్తిలో అంతరపంటగా వేయండి.",
                "విత్తే ముందు విత్తన శుద్ధి తప్పనిసరిగా చేయండి.",
                "పక్షులు వాలడానికి ఎకరాకు 10-15 పక్షి స్థావరాలను (T ఆకారపు కర్రలు) ఏర్పాటు చేయండి.",
                "వేర్వేరు సమయాల్లో విత్తడం మానుకోండి."
            ]
        },
        "next_season_prevention": {
            "en": "Deep summer plowing to expose pupae to predatory birds and hot sun; practice crop rotation with non-graminaceous crops.",
            "te": "వేసవిలో లోతు దుక్కులు చేసి భూమిలోని కోశస్థ దశలను నాశనం చేయండి. పప్పుదినుసుల పంటలతో పంట మార్పిడి చేయండి."
        },
        "organic_management": {
            "en": "Drop dry sand or soil mixed with ash/neem powder into whorls, or spray Azadirachtin 10,000 ppm @ 2ml/L.",
            "te": "మొక్కల సుడిలో బూడిద లేదా ఇసుక-వేపపిండి మిశ్రమాన్ని వేయండి, లేదా వేప నూనె 2 మి.లీ. లీటరు నీటికి పిచికారీ చేయండి."
        },
        "biological_control": {
            "en": "Spray Bacillus thuringiensis (Bt) kurstaki @ 2g/L or Metarhizium rileyi @ 5g/L water directed into whorls.",
            "te": "బాసిల్లస్ తురింజియెన్సిస్ (Bt) 2 గ్రా. లేదా మెటారైజియమ్ 5 గ్రా. లీటరు నీటికి కలిపి సుడులలో పిచికారీ చేయండి."
        },
        "cultural_control": {
            "en": "Intercropping with cowpea, synchronized village planting, and bird perches.",
            "te": "అలసందలతో అంతరపంట, ఒకే సమయంలో విత్తుకోవడం మరియు పక్షి స్థావరాల ఏర్పాటు."
        },
        "chemical_control": {
            "has_verified_chemical": True,
            "product": {
                "en": "Chlorantraniliprole 18.5% SC or Emamectin Benzoate 5% SG",
                "te": "క్లోరాంట్రానిలిప్రోల్ 18.5% SC లేదా ఇమామెక్టిన్ బెంజోయేట్ 5% SG"
            },
            "dosage": {
                "en": "Chlorantraniliprole 18.5% SC @ 0.4ml/L water OR Emamectin Benzoate 5% SG @ 0.5g/L water",
                "te": "క్లోరాంట్రానిలిప్రోల్ 18.5% SC @ 0.4 మి.లీ./లీటర్ నీటికి లేదా ఇమామెక్టిన్ బెంజోయేట్ 5% SG @ 0.5 గ్రా./లీటర్ నీటికి"
            },
            "water_quantity": {
                "en": "200 Litres of spray solution per acre",
                "te": "ఎకరాకు 200 లీటర్ల పిచికారీ ద్రావణం"
            },
            "application_method": {
                "en": "Direct nozzle strictly into the central leaf whorl of each plant using a knapsack sprayer",
                "te": "స్ప్రేయర్ నాజిల్‌ను నేరుగా ప్రతి మొక్క సుడిలోకి గురిపెట్టి పిచికారీ చేయండి"
            },
            "waiting_period_phi": {
                "en": "14 to 21 days before cob harvest",
                "te": "కండెలు కోయడానికి ముందు 14 నుండి 21 రోజుల వేచిఉండే కాలం"
            },
            "safety_precaution": {
                "en": "Wear protective face shield and hand protection during application.",
                "te": "చేతి తొడుగులు మరియు ఫేస్ మాస్క్ తప్పనిసరిగా ధరించండి."
            }
        },
        "safety_precautions": {
            "en": "Do not feed chemically treated green fodder to dairy cattle within the pre-harvest interval.",
            "te": "మందు పిచికారీ చేసిన పచ్చి గడ్డిని వేచిఉండే కాలం ముగిసే వరకు పశువులకు మేపవద్దు."
        }
    },

    "Fruit and Shoot Borer": {
        "disease": "Fruit and Shoot Borer",
        "crop": "Brinjal",
        "scientific_name": "Leucinodes orbonalis",
        "problem_type": "Insect Pest",
        "affected_part": "Tender Shoots, Fruits",
        "severity": "High",
        "what_is_problem": {
            "en": "Brinjal Fruit and Shoot Borer is the most serious pest of eggplant. In early vegetative stage, larvae bore into growing shoots, causing shoot wilting and drooping ('deadhearts'). In reproductive stage, larvae bore inside developing fruits, plugging entrance holes with excreta. Infested fruits rot, become unfit for market, and yield losses range from 40-70%.",
            "te": "వంకాయలో కొమ్మ మరియు కాయ తొలుచు పురుగు అత్యంత ప్రమాదకరమైన పురుగు. పంట ప్రారంభ దశలో లార్వాలు లేత కొమ్మలను తొలిచి లోపలికి ప్రవేశించడం వల్ల కొమ్మల చివర్లు వాడిపోయి వేలాడతాయి. కాయల దశలో కాయలలోకి చొరబడి గుజ్జును తినివేయడం వల్ల కాయలు కుళ్ళి మార్కెట్‌కు పనికిరాకుండా పోతాయి. దీనివల్ల 40-70% వరకు దిగుబడి నష్టం కలుగుతుంది."
        },
        "why_it_occurs": {
            "en": "Continuous overlapping brinjal cultivation throughout the year, warm humid climates, and failure to clip damaged shoots early allow continuous pest generations.",
            "te": "సంవత్సరం పొడవునా వంకాయను నిరంతరం సాగు చేయడం, అనుకూల ఉష్ణోగ్రతలు మరియు దెబ్బతిన్న కొమ్మలను ఎప్పటికప్పుడు తుంచకపోవడం వల్ల ఈ పురుగు ఉధృతి పెరుగుతుంది."
        },
        "immediate_action_steps": {
            "en": [
                "Clip and destroy all wilted and drooping shoot tips below the point of bore holes.",
                "Collect all bored, damaged fruits and bury them deeply with lime.",
                "Install 8 to 10 pheromone traps (Lucin-lure) per acre for mass trapping.",
                "Avoid repeating same chemical class continuously to prevent pesticide resistance.",
                "Consult local horticultural officer if fruit damage exceeds 10%."
            ],
            "te": [
                "వాడిపోయిన కొమ్మల చివర్లను పురుగు ఉన్న భాగం కంటే కొద్దిగా క్రిందికి తుంచి నాశనం చేయండి.",
                "పురుగు ఆశించిన కాయలను ఎప్పటికప్పుడు ఏరివేసి సున్నం చల్లి లోతైన గుంతల్లో పాతిపెట్టండి.",
                "ఎకరాకు 8 నుండి 10 లూసిన్-ల్యూర్ లింగాకర్షక బుట్టలను అమర్చండి.",
                "ఒకే రకమైన పురుగుమందులను పదే పదే వాడవద్దు.",
                "కాయల నష్టం 10% కంటే ఎక్కువైతే ఉద్యానవన అధికారిని సంప్రదించండి."
            ]
        },
        "action_urgency": {
            "en": "Moderate to High Urgency: Clip wilted shoots weekly and install pheromone traps within 48 hours.",
            "te": "అత్యవసర చర్య అవసరం: వాడిన కొమ్మలను వారానికోసారి తుంచివేయాలి మరియు 48 గంటల్లో లింగాకర్షక బుట్టలు అమర్చాలి."
        },
        "prevention_steps": {
            "en": [
                "Grow tolerant brinjal varieties or hybrids with spiny calyx recommended by university.",
                "Clipping of infested terminal shoots at weekly intervals right from 30 days after transplanting.",
                "Install pheromone traps @ 10-12/acre immediately at flowering stage.",
                "Intercrop with coriander or fennel to attract parasitic wasps and natural predators.",
                "Practice clean field sanitation and destroy old ratoon crops."
            ],
            "te": [
                "ముళ్ళు కలిగిన తొడిమలు ఉండే తెగులు తట్టుకునే రకాలను ఎంపిక చేసుకోండి.",
                "నాటిన 30 రోజుల నుండి ప్రతి వారం దెబ్బతిన్న కొమ్మలను క్రమం తప్పకుండా తుంచివేయండి.",
                "పూత దశ నుండే ఎకరాకు 10-12 లింగాకర్షక బుట్టలను అమర్చండి.",
                "చేను చుట్టూ ధనియాలు లేదా సోంపు పంటలను వేయడం ద్వారా మిత్రపురుగులను ఆకర్షించండి.",
                "పాత వంకాయ పంటలను పొలంలో ఉంచకుండా వెంటనే దున్నివేయండి."
            ]
        },
        "next_season_prevention": {
            "en": "Strict crop rotation with non-solanaceous crops (cereals, legumes); deep summer plowing to destroy pupae.",
            "te": "పంట మార్పిడిలో వంకాయ తర్వాత పప్పుదినుసులు లేదా తృణధాన్యాలు సాగు చేయండి. వేసవిలో లోతు దుక్కులు చేయండి."
        },
        "organic_management": {
            "en": "Spray 5% Neem Seed Kernel Extract (NSKE) or Neem Oil 10,000 ppm @ 2ml/L water at weekly intervals.",
            "te": "5% వేప గింజల కషాయం లేదా వేప నూనె 2 మి.లీ. లీటరు నీటికి కలిపి వారం వ్యవధిలో పిచికారీ చేయండి."
        },
        "biological_control": {
            "en": "Release egg parasitoids Trichogramma chilonis @ 50,000/acre at weekly intervals 4-5 times.",
            "te": "ట్రైకోగ్రామా చిలోనిస్ గుడ్ల పరాన్నజీవులను ఎకరాకు 50,000 చొప్పున వారం వ్యవధిలో 4-5 సార్లు విడుదల చేయండి."
        },
        "cultural_control": {
            "en": "Regular manual clipping of wilted shoots and installation of Lucin-lure pheromone traps.",
            "te": "వాడిన కొమ్మలను క్రమం తప్పకుండా కత్తిరించడం మరియు లింగాకర్షక బుట్టలను ఏర్పాటు చేయడం."
        },
        "chemical_control": {
            "has_verified_chemical": True,
            "product": {
                "en": "Emamectin Benzoate 5% SG or Chlorantraniliprole 18.5% SC",
                "te": "ఇమామెక్టిన్ బెంజోయేట్ 5% SG లేదా క్లోరాంట్రానిలిప్రోల్ 18.5% SC"
            },
            "dosage": {
                "en": "Emamectin Benzoate 5% SG @ 0.4g/L water OR Chlorantraniliprole 18.5% SC @ 0.3ml/L water",
                "te": "ఇమామెక్టిన్ బెంజోయేట్ 5% SG @ 0.4 గ్రా./లీటర్ నీటికి లేదా క్లోరాంట్రానిలిప్రోల్ 18.5% SC @ 0.3 మి.లీ./లీటర్ నీటికి"
            },
            "water_quantity": {
                "en": "200 Litres of spray solution per acre",
                "te": "ఎకరాకు 200 లీటర్ల పిచికారీ ద్రావణం"
            },
            "application_method": {
                "en": "Thorough foliar spray covering flowering clusters and developing brinjal fruits",
                "te": "పూత మరియు పిందెలు పూర్తిగా తడిసేలా పిచికారీ చేయండి"
            },
            "waiting_period_phi": {
                "en": "3 days for Emamectin Benzoate; 3 days for Chlorantraniliprole",
                "te": "కాయలు కోయడానికి ముందు 3 రోజుల వేచిఉండే కాలం (PHI)"
            },
            "safety_precaution": {
                "en": "Pick all marketable ripe fruits prior to spraying chemicals.",
                "te": "మందు పిచికారీ చేయడానికి ముందే కోతకు వచ్చిన కాయలను పూర్తిగా కోసివేయండి."
            }
        },
        "safety_precautions": {
            "en": "Wash picked brinjal fruits thoroughly in clean running water before market transport.",
            "te": "మార్కెట్‌కు తరలించే ముందు కోసిన కాయలను మంచినీటితో శుభ్రంగా కడగండి."
        }
    },

    "Fusarium Wilt": {
        "disease": "Fusarium Wilt",
        "crop": "Bengal Gram",
        "scientific_name": "Fusarium oxysporum f. sp. ciceris",
        "problem_type": "Fungal Disease",
        "affected_part": "Vascular System, Roots, Foliage",
        "severity": "High",
        "what_is_problem": {
            "en": "Fusarium Wilt is a devastating vascular disease of chickpea (Bengal Gram) and pigeonpea. The soil-borne fungus penetrates roots and clogs xylem water-conducting vessels. Affected plants exhibit sudden drooping of petioles, leaf chlorosis, and progressive drying from bottom up without leaf shedding. Splitting the collar region reveals distinctive dark brown vascular browning. Yield losses reach up to 100% in disease patches.",
            "te": "శనగలో ఎండు తెగులు (ఫ్యుసేరియం విల్ట్) నేల ద్వారా వ్యాపించే తీవ్రమైన శిలీంధ్ర వ్యాధి. శిలీంధ్రం వేర్ల ద్వారా ప్రవేశించి మొక్కల నీటి నాళాలను మూసివేస్తుంది. దీనివల్ల మొక్కలు ఆకస్మికంగా వడలిపోయి, ఆకులు పసుపు రంగులోకి మారి రాలిపోకుండానే ఎండిపోతాయి. మొదలును నిలువుగా చీల్చి చూస్తే లోపలి నాళాలు ముదురు గోధుమ రంగులోకి మారడం స్పష్టంగా కనిపిస్తుంది. తెగులు సోకిన పొలాల్లో 100% వరకు నష్టం కలుగుతుంది."
        },
        "why_it_occurs": {
            "en": "High soil temperatures (25-30°C) during seedling or flowering stages, dry soil moisture stress, and persistence of fungal chlamydospores in soil for several years favor disease outbreak.",
            "te": "మొలక లేదా పూత దశలో నేలలో అధిక ఉష్ణోగ్రతలు (25-30°C), నేలలో తేమ లోపించడం మరియు నేలలో గత పంటలకు సంబంధించిన శిలీంధ్ర బీజాలు ఉండటం వల్ల ఈ తెగులు తీవ్రమవుతుంది."
        },
        "immediate_action_steps": {
            "en": [
                "Uproot and burn wilted plants immediately along with root systems to prevent chlamydospore build-up.",
                "Do not flood the field as irrigation water rapidly disperses fungal inoculum.",
                "Spot drench surrounding healthy plants with biological agents (Trichoderma).",
                "Avoid deep intercultivation that injures crop roots and creates entry points.",
                "Consult agricultural officer to confirm vascular browning diagnosis."
            ],
            "te": [
                "ఎండు తెగులు సోకిన మొక్కలను వేర్లతో సహా పీకి పొలానికి దూరంగా తగులబెట్టండి.",
                "పొలానికి ఎక్కువగా నీరు పెట్టవద్దు, నీటి ప్రవాహం ద్వారా తెగులు ఇతర మొక్కలకు వ్యాపిస్తుంది.",
                "మొక్కల మొదళ్ల వద్ద ట్రైకోడెర్మా ద్రావణాన్ని పోసి తడపండి.",
                "వేర్లు దెబ్బతినకుండా అంతరకృషిని జాగ్రత్తగా చేయండి.",
                "నాళాల రంగు మారడాన్ని నిర్ధారించుకోవడానికి వ్యవసాయ అధికారిని సంప్రదించండి."
            ]
        },
        "action_urgency": {
            "en": "Moderate to High Urgency: Uproot wilted plants immediately and spot-drench biologicals within 24 to 48 hours.",
            "te": "అత్యవసర చర్య అవసరం: ఎండిన మొక్కలను వెంటనే పీకివేసి, 24 నుండి 48 గంటల్లోగా జీవ శిలీంధ్ర నాశినితో మొదళ్లను తడపాలి."
        },
        "prevention_steps": {
            "en": [
                "Sow wilt-resistant varieties such as JG 11, JAKI 9218, KAK 2, or NBeG 3.",
                "Compulsory seed treatment with Trichoderma viride @ 10g/kg seed or Carbendazim @ 2g/kg seed.",
                "Soil application of Trichoderma viride enriched in well-decomposed FYM (2 kg in 50 kg manure/acre).",
                "Avoid early sowing during warm October temperatures; delay slightly to cooler November.",
                "Practice 3 to 4-year crop rotation with non-host cereals like sorghum or wheat."
            ],
            "te": [
                "JG 11, JAKI 9218, KAK 2, NBeG 3 వంటి ఎండు తెగులును తట్టుకునే రకాలను సాగు చేయండి.",
                "విత్తే ముందు కిలో విత్తనానికి ట్రైకోడెర్మా విరిడె @ 10 గ్రా. లేదా కార్బండిజిమ్ @ 2 గ్రా. కలిపి విత్తన శుద్ధి తప్పక చేయండి.",
                "ఎకరాకు 2 కిలోల ట్రైకోడెర్మాను 50 కిలోల పశువుల ఎరువులో కలిపి ఆఖరి దుక్కిలో వేయండి.",
                "అక్టోబర్‌లో వేడి ఎక్కువగా ఉన్నప్పుడు కాకుండా నవంబర్ మొదటి వారంలో విత్తుకోండి.",
                "జొన్న లేదా గోధుమ వంటి తృణధాన్యాలతో 3-4 సంవత్సరాల పంట మార్పిడి చేయండి."
            ]
        },
        "next_season_prevention": {
            "en": "Deep summer plowing to desiccate fungal structures, long crop rotation, and green manuring with sunnhemp.",
            "te": "వేసవిలో లోతు దుక్కులు చేసి నేలను ఎండబెట్టండి. జనుము లేదా జీలుగతో పచ్చిరొట్ట ఎరువుల సాగు చేయండి."
        },
        "organic_management": {
            "en": "Soil application of Trichoderma viride @ 2.5 kg/acre mixed in 250 kg organic compost at sowing.",
            "te": "విత్తే సమయంలో ఎకరాకు 2.5 కిలోల ట్రైకోడెర్మా విరిడెను 250 కిలోల సేంద్రీయ ఎరువుతో కలిపి నేలలో వేయండి."
        },
        "biological_control": {
            "en": "Seed bio-priming with Trichoderma harzianum or Pseudomonas fluorescens @ 10g/kg seed.",
            "te": "ట్రైకోడెర్మా హార్జియానమ్ లేదా సూడోమోనాస్ ఫ్లోరోసెన్స్ 10 గ్రా./కిలో విత్తనానికి కలిపి విత్తన శుద్ధి చేయండి."
        },
        "cultural_control": {
            "en": "Resistant varieties (JG 11), delayed cooler planting, and long crop rotation.",
            "te": "తెగులు తట్టుకునే రకాల సాగు (JG 11), ఆలస్యంగా చలికాలంలో విత్తడం మరియు పంట మార్పిడి."
        },
        "chemical_control": {
            "has_verified_chemical": False,
            "unverified_reason": {
                "en": "Fusarium is a vascular soil-borne pathogen. Foliar chemical sprays are ineffective once infection has occurred. Prevention via seed treatment and resistant varieties is the only verified scientific management.",
                "te": "ఎండు తెగులు నేల ద్వారా వ్యాపించే అంతర్గత శిలీంధ్ర వ్యాధి. మొక్కకు సోకిన తర్వాత ఆకులపై రసాయనాలు పిచికారీ చేయడం వల్ల ఎలాంటి ఉపయోగం ఉండదు. విత్తన శుద్ధి మరియు నిరోధక రకాల సాగు మాత్రమే శాస్త్రీయమైన పరిష్కారం."
            }
        },
        "safety_precautions": {
            "en": "Always wear disposable gloves and face mask when handling dry chemical seed treatment fungicides.",
            "te": "విత్తన శుద్ధి చేసేటప్పుడు రసాయన పొడి ముక్కులోకి వెళ్లకుండా మాస్క్ మరియు చేతి తొడుగులు ధరించండి."
        }
    },

    "Grain Mold": {
        "disease": "Grain Mold",
        "crop": "Sorghum",
        "scientific_name": "Curvularia lunata / Fusarium spp.",
        "problem_type": "Fungal Disease",
        "affected_part": "Panicles, Grains",
        "severity": "Moderate to High",
        "what_is_problem": {
            "en": "Sorghum Grain Mold is a complex fungal infection attacking maturing grain panicles. It causes white, pink, grey, or black discoloration and velvety fungal growth on developing grains. Severely infected grains become soft, chalky, break easily during threshing, germinate poorly, and accumulate dangerous mycotoxins, causing 30-50% economic loss.",
            "te": "జొన్నలో గింజ బూజు తెగులు (గ్రెయిన్ మోల్డ్) అనేది కంకి గింజలపై దాడి చేసే సంక్లిష్ట శిలీంధ్ర వ్యాధి. గింజలపై నలుపు, గులాబీ లేదా బూడిద రంగు బూజు ఏర్పడుతుంది. తెగులు సోకిన గింజలు మెత్తబడి నూర్పిడి సమయంలో పిండిగా మారిపోతాయి. విత్తన మొలక శాతం తగ్గి, విషపూరితమైన మైకోటాక్సిన్లు చేరడం వల్ల 30-50% వరకు ఆర్థిక నష్టం వాటిల్లుతుంది."
        },
        "why_it_occurs": {
            "en": "Frequent rain and persistent high relative humidity (>80%) coinciding with the grain filling and physiological maturity stages of sorghum favor mold colonization.",
            "te": "గింజ పాలుపోసుకునే దశలో మరియు కంకి ముదిరే సమయంలో ఎడతెరిపి లేని వర్షాలు, మంచు మరియు గాలిలో అధిక తేమ ఉండటం వల్ల బూజు వేగంగా వ్యాపిస్తుంది."
        },
        "immediate_action_steps": {
            "en": [
                "Harvest mature panicles promptly as soon as physiological maturity (black layer formation) is attained.",
                "Do not leave harvested panicles on wet ground; elevate them on tarpaulins for sun-drying.",
                "Dry threshed grains rapidly below 10-12% moisture before bagging.",
                "Separate heavily molded discolored grain lots from food and animal feed streams.",
                "Consult local KVK scientist if mold occurs during early milky grain stage."
            ],
            "te": [
                "గింజ ముదిరిన వెంటనే (బ్లాక్ లేయర్ ఏర్పడగానే) ఆలస్యం చేయకుండా కంకులను వెంటనే కోయండి.",
                "కోసిన కంకులను తడి నేలపై ఉంచకుండా టార్పాలిన్లపై ఎండబెట్టండి.",
                "నూర్పిడి చేసిన గింజలను 10-12% కంటే తక్కువ తేమ వచ్చే వరకు బాగా ఎండబెట్టండి.",
                "బూజు పట్టిన నల్లని గింజలను ఆహార అవసరాలకు లేదా పశువుల దాణాకు వాడవద్దు.",
                "పాలుపోసుకునే దశలోనే బూజు కనిపిస్తే వ్యవసాయ అధికారిని సంప్రదించండి."
            ]
        },
        "action_urgency": {
            "en": "Moderate Urgency: Harvest and dry grains immediately upon reaching physiological maturity.",
            "te": "మధ్యస్థ అత్యవసరం: పంట ముదిరిన వెంటనే కోత కోసి ఎండబెట్టాలి."
        },
        "prevention_steps": {
            "en": [
                "Sow grain-mold tolerant sorghum hybrids such as CSH 16, CSH 25, or CSV 20.",
                "Adjust sowing dates so that grain maturation does not coincide with peak monsoon rains.",
                "Choose varieties with loose or semi-compact panicles rather than tight dense heads.",
                "Ensure balanced fertilization and harvest at physiological maturity.",
                "Store grains only in moisture-proof clean bags in ventilated godowns."
            ],
            "te": [
                "CSH 16, CSH 25 వంటి బూజు తెగులును తట్టుకునే రకాలను సాగు చేయండి.",
                "కంకి పాలుపోసుకునే సమయానికి భారీ వర్షాలు ముగిసేలా విత్తే కాలాన్ని సరిచూసుకోండి.",
                "కంకి వదులుగా ఉండే రకాలను ఎంపిక చేసుకోండి.",
                "సమతుల్య ఎరువులు వాడి సరైన సమయంలో కోత కోయండి.",
                "తేమ లేని శుభ్రమైన సంచులలో గింజలను భద్రపరచండి."
            ]
        },
        "next_season_prevention": {
            "en": "Deep summer plowing and crop rotation with non-cereal crops like pulses or oilseeds.",
            "te": "వేసవిలో లోతు దుక్కులు చేసి తెగులు శేషాలను నాశనం చేయండి. పప్పుదినుసులతో పంట మార్పిడి చేయండి."
        },
        "organic_management": {
            "en": "Foliar spray with 5% Neem Seed Kernel Extract (NSKE) at early flowering.",
            "te": "పూత దశలో 5% వేప గింజల కషాయాన్ని పిచికారీ చేయండి."
        },
        "biological_control": {
            "en": "Spray Pseudomonas fluorescens @ 10g/L water at 50% flowering stage.",
            "te": "50% పూత దశలో సూడోమోనాస్ ఫ్లోరోసెన్స్ 10 గ్రాములు లీటరు నీటికి కలిపి పిచికారీ చేయండి."
        },
        "cultural_control": {
            "en": "Adjusting sowing dates to avoid rains at maturity, loose panicle varieties, and prompt post-harvest drying.",
            "te": "విత్తే కాలాన్ని సర్దుబాటు చేయడం, వదులు కంకి రకాలు మరియు కోసిన వెంటనే ఎండబెట్టడం."
        },
        "chemical_control": {
            "has_verified_chemical": True,
            "product": {
                "en": "Propiconazole 25% EC or Mancozeb 75% WP",
                "te": "ప్రొపికొనాజోల్ 25% EC లేదా మాంకోజెబ్ 75% WP"
            },
            "dosage": {
                "en": "Propiconazole 25% EC @ 1ml/L water OR Mancozeb 75% WP @ 2.5g/L water",
                "te": "ప్రొపికొనాజోల్ 25% EC @ 1 మి.లీ./లీటర్ నీటికి లేదా మాంకోజెబ్ 75% WP @ 2.5 గ్రా./లీటర్ నీటికి"
            },
            "water_quantity": {
                "en": "200 Litres of spray solution per acre",
                "te": "ఎకరాకు 200 లీటర్ల పిచికారీ ద్రావణం"
            },
            "application_method": {
                "en": "Directed panicle spray at 50% flowering followed by a second spray 10 days later",
                "te": "50% పూత దశలో కంకులపై మాత్రమే పడేలా పిచికారీ చేయండి"
            },
            "waiting_period_phi": {
                "en": "30 days before harvest",
                "te": "పంట కోతకు ముందు 30 రోజుల వేచిఉండే కాలం"
            },
            "safety_precaution": {
                "en": "Do not spray immediately before rainfall; use personal protective equipment.",
                "te": "వర్షం వచ్చే సూచన ఉన్నప్పుడు పిచికారీ చేయవద్దు. రక్షణ దుస్తులు ధరించండి."
            }
        },
        "safety_precautions": {
            "en": "Never consume or sell moldy grains with visible fungal sclerotia or mycotoxin smell.",
            "te": "తీవ్రంగా బూజు పట్టిన గింజలను మానవ ఆహారానికి లేదా జంతువులకు ఎట్టిపరిస్థితుల్లోనూ వాడవద్దు."
        }
    },

    "Leaf Blotch": {
        "disease": "Leaf Blotch",
        "crop": "Turmeric",
        "scientific_name": "Taphrina maculans",
        "problem_type": "Fungal Disease",
        "affected_part": "Leaves",
        "severity": "Moderate",
        "what_is_problem": {
            "en": "Turmeric Leaf Blotch caused by Taphrina maculans appears as small, reddish-brown to dark brown spots on both surfaces of leaves. Spots coalesce into large dirty-yellow or dark blotches, causing rapid drying and blighting of foliage. Photosynthesis is severely impaired, resulting in reduced rhizome weight and 20-35% yield reduction.",
            "te": "పసుపులో ఆకుమచ్చ తెగులు (టాఫ్రినా లీఫ్ బ్లాచ్) ఆకుల రెండు వైపులా ఎరుపు-గోధుమ రంగు చిన్న మచ్చల రూపంలో ప్రారంభమవుతుంది. ఈ మచ్చలు కలిసిపోయి పెద్ద ముదురు గోధుమ లేదా పసుపు రంగు మచ్చలుగా మారి ఆకులు ఎండిపోతాయి. కిరణజన్య సంయోగక్రియ తగ్గి దుంప పరిమాణం తగ్గి 20-35% వరకు దిగుబడి నష్టం కలుగుతుంది."
        },
        "why_it_occurs": {
            "en": "Heavy monsoon rains, excessive field moisture or waterlogging, relative humidity above 80%, and continuous shade favor pathogen sporulation.",
            "te": "ఎడతెరిపి లేని వర్షాలు, పొలంలో నీరు నిలవడం, అధిక తేమ మరియు తీవ్రమైన నీడ ఉన్న ప్రదేశాలలో ఈ తెగులు వేగంగా వ్యాపిస్తుంది."
        },
        "immediate_action_steps": {
            "en": [
                "Improve field drainage trenches to remove excess water from between ridges and furrows.",
                "Remove and burn severely blotched lower leaves to reduce fungal inoculum.",
                "Stop overhead sprinkling and avoid working in wet turmeric plots.",
                "Apply balanced potash to enhance rhizome and leaf resilience.",
                "Consult local horticultural officer if blotch spots expand to top foliage."
            ],
            "te": [
                "పసుపు బోదెల మధ్య నిలిచిన అదనపు నీటిని వెంటనే బయటకు పంపేలా కాలువలను శుభ్రం చేయండి.",
                "తెగులు తీవ్రంగా సోకిన క్రింది ఆకులను తుంచి పొలానికి దూరంగా తగులబెట్టండి.",
                "పైనుండి నీరు చిలకరించవద్దు మరియు తడిగా ఉన్నప్పుడు పొలంలో తిరగవద్దు.",
                "దుంప ఎదుగుదలకు సమతుల్య పొటాష్ ఎరువును అందించండి.",
                "మచ్చలు పై ఆకులకు పాకుతుంటే ఉద్యానవన అధికారిని సంప్రదించండి."
            ]
        },
        "action_urgency": {
            "en": "Moderate Urgency: Improve drainage immediately and initiate protective fungicide spray within 2 to 3 days.",
            "te": "మధ్యస్థ అత్యవసరం: నీరు తీసివేసి 2-3 రోజుల్లోగా నివారణ మందు పిచికారీ చేయాలి."
        },
        "prevention_steps": {
            "en": [
                "Plant certified disease-free seed rhizomes of improved varieties like IISR Pratibha or Duggirala.",
                "Treat seed rhizomes before planting with Mancozeb @ 3g/L water for 30 minutes.",
                "Provide raised bed or ridge-and-furrow planting to guarantee good drainage.",
                "Apply neem cake @ 200 kg/acre along with FYM at final bed preparation.",
                "Maintain clean weeding and avoid heavy shading trees inside plot."
            ],
            "te": [
                "ప్రతిభ, దుగ్గిరాల వంటి ఆరోగ్యకరమైన విత్తన దుంపలను మాత్రమే నాటండి.",
                "విత్తే ముందు దుంపలను లీటరు నీటికి మాంకోజెబ్ @ 3 గ్రా. కలిపిన ద్రావణంలో 30 నిమిషాలు నానబెట్టి శుద్ధి చేయండి.",
                "బోదెలు మరియు సాళ్ళ పద్ధతిలో నాటి నీరు నిలవకుండా చూడండి.",
                "ఆఖరి దుక్కిలో ఎకరాకు 200 కిలోల వేపపిండిని పశువుల ఎరువుతో కలిపి వేయండి.",
                "కలుపు లేకుండా చూసుకోండి మరియు తీవ్రమైన నీడను నివారించండి."
            ]
        },
        "next_season_prevention": {
            "en": "Deep summer plowing and strict 3-year crop rotation with non-rhizome crops like maize or pulses.",
            "te": "వేసవిలో లోతు దుక్కులు చేయండి. పసుపు తర్వాత మొక్కజొన్న లేదా పప్పుదినుసులతో 3 సంవత్సరాల పంట మార్పిడి చేయండి."
        },
        "organic_management": {
            "en": "Foliar spray with 1% Bordeaux mixture or Copper Oxychloride @ 2.5g/L water.",
            "te": "1% బోర్డో మిశ్రమం లేదా కాపర్ ఆక్సిక్లోరైడ్ 2.5 గ్రా. లీటరు నీటికి కలిపి పిచికారీ చేయండి."
        },
        "biological_control": {
            "en": "Rhizome treatment and foliar spray with Pseudomonas fluorescens @ 10g/L water.",
            "te": "విత్తన దుంపల శుద్ధి మరియు ఆకులపై సూడోమోనాస్ ఫ్లోరోసెన్స్ 10 గ్రా./లీ. పిచికారీ చేయండి."
        },
        "cultural_control": {
            "en": "Raised bed planting, free drainage channels, and removal of blighted leaves.",
            "te": "ఎత్తైన బోదెల సాగు, మురుగు నీటి కాలువలు మరియు ఎండిన ఆకులను తొలగించడం."
        },
        "chemical_control": {
            "has_verified_chemical": True,
            "product": {
                "en": "Mancozeb 75% WP or Propiconazole 25% EC",
                "te": "మాంకోజెబ్ 75% WP లేదా ప్రొపికొనాజోల్ 25% EC"
            },
            "dosage": {
                "en": "Mancozeb 75% WP @ 2.5g/L water OR Propiconazole 25% EC @ 1ml/L water",
                "te": "మాంకోజెబ్ 75% WP @ 2.5 గ్రా./లీటర్ నీటికి లేదా ప్రొపికొనాజోల్ 25% EC @ 1 మి.లీ./లీటర్ నీటికి"
            },
            "water_quantity": {
                "en": "200 to 250 Litres of spray solution per acre",
                "te": "ఎకరాకు 200 నుండి 250 లీటర్ల పిచికారీ ద్రావణం"
            },
            "application_method": {
                "en": "Foliar spray thoroughly wetting upper and lower leaf surfaces",
                "te": "ఆకుల రెండు వైపులా పూర్తిగా తడిసేలా పిచికారీ చేయండి"
            },
            "waiting_period_phi": {
                "en": "40 days before rhizome harvest",
                "te": "దుంపలు తవ్వడానికి ముందు 40 రోజుల వేచిఉండే కాలం"
            },
            "safety_precaution": {
                "en": "Wear protective mask and gloves; avoid spraying during windy conditions.",
                "te": "మాస్క్ మరియు చేతి తొడుగులు ధరించండి. గాలి ఎక్కువగా ఉన్నప్పుడు పిచికారీ చేయవద్దు."
            }
        },
        "safety_precautions": {
            "en": "Keep chemical containers away from domestic wells and animal enclosures.",
            "te": "రసాయన డబ్బాలను తాగునీటి బావులు మరియు పశువుల కొట్టాలకు దూరంగా ఉంచండి."
        }
    },

    "Leaf Curl Virus": {
        "disease": "Leaf Curl Virus",
        "crop": "Chilli",
        "scientific_name": "Begomovirus / Chilli leaf curl virus",
        "problem_type": "Viral Disease",
        "affected_part": "Leaves, Growing Shoots",
        "severity": "High",
        "what_is_problem": {
            "en": "Chilli Leaf Curl Virus is a destructive viral disease transmitted by the whitefly (Bemisia tabaci). Symptoms include severe upward and downward curling of leaves, puckering, thickening of veins, shortened internodes, and stunted bushy growth. Flower buds drop prematurely and infected plants produce deformed, tiny, unmarketable fruits, resulting in up to 80% yield loss.",
            "te": "మిరపలో ఆకు ముడత వైరస్ (జెమిని వైరస్) తెల్లదోమ ద్వారా వ్యాపించే అత్యంత ప్రమాదకరమైన వైరస్ తెగులు. దీనివల్ల ఆకులు పైకి మరియు క్రిందికి ముడుచుకుపోయి, ఈనెలు లావుగా మారి మొక్క గిడసబారి గుబురుగా తయారవుతుంది. పూత రాలిపోయి, కాయలు వంకరగా మారి చిన్నవిగా తయారవుతాయి. తీవ్రమైన దశలో 80% వరకు దిగుబడి నష్టం కలుగుతుంది."
        },
        "why_it_occurs": {
            "en": "Heavy populations of vector whiteflies, dry and warm conditions, presence of infected solanaceous weeds, and lack of border trap crops allow rapid viral spread.",
            "te": "వైరస్‌ను వ్యాప్తి చేసే తెల్లదోమల సంఖ్య విపరీతంగా పెరగడం, పొడి వేడి వాతావరణం, పొలం గట్లపై కలుపు మొక్కలు ఉండటం వల్ల ఈ వైరస్ వేగంగా వ్యాపిస్తుంది."
        },
        "immediate_action_steps": {
            "en": [
                "Rogue out and destroy severely virus-stunted plants in plastic bags to avoid dispersing whiteflies.",
                "Install 25 yellow sticky traps per acre immediately to capture adult whiteflies.",
                "Spray 5% Neem Seed Kernel Extract (NSKE) or Neem Oil @ 5ml/L to deter whitefly feeding.",
                "Control broadleaf weed hosts on bunds that serve as virus reservoirs.",
                "Consult agricultural officer if more than 5% of young plants show systemic curling."
            ],
            "te": [
                "వైరస్ సోకి ముడుచుకుపోయిన మొక్కలను వెంటనే పీకి ప్లాస్టిక్ సంచులలో పెట్టి పొలానికి దూరంగా నాశనం చేయండి.",
                "ఎకరాకు 25 పసుపు రంగు జిగురు అట్టలను అమర్చి తెల్లదోమలను నివారించండి.",
                "5% వేప గింజల కషాయం లేదా వేప నూనె 5 మి.లీ. లీటరు నీటికి కలిపి పిచికారీ చేయండి.",
                "గట్లపై ఉన్న కలుపు మొక్కలను పూర్తిగా తొలగించండి.",
                "5% కంటే ఎక్కువ మొక్కలకు వైరస్ సోకితే వ్యవసాయ అధికారిని సంప్రదించండి."
            ]
        },
        "action_urgency": {
            "en": "High Urgency: Rogue out infected plants and install yellow sticky traps within 24 hours to halt vector spread.",
            "te": "అత్యవసర చర్య అవసరం: 24 గంటల్లోగా వైరస్ మొక్కలను పీకివేయాలి మరియు పసుపు జిగురు అట్టలు అమర్చాలి."
        },
        "prevention_steps": {
            "en": [
                "Grow barrier crops (3-4 dense rows of maize or sorghum) around chilli plots.",
                "Raise nursery seedlings under 40-mesh insect-proof nylon net.",
                "Seed treatment with Imidacloprid 70% WS @ 5g/kg seed before sowing.",
                "Use reflective silver-black plastic mulch to repel flying whiteflies.",
                "Maintain clean cultivation free from Parthenium and alternate host weeds."
            ],
            "te": [
                "చేను చుట్టూ 3-4 వరుసలలో జొన్న లేదా మొక్కజొన్నను సరిహద్దు రక్షణ పంటగా సాగు చేయండి.",
                "నారును 40 మెష్ దోమతెర కింద రక్షిత వాతావరణంలో పెంచండి.",
                "విత్తే ముందు కిలో విత్తనానికి ఇమిడాక్లోప్రిడ్ @ 5 గ్రా. కలిపి విత్తన శుద్ధి చేయండి.",
                "సిల్వర్-బ్లాక్ మల్చింగ్ షీట్లు వాడటం ద్వారా తెల్లదోమ రాకుండా చూడండి.",
                "గట్లపై కలుపు మొక్కలు లేకుండా నిరంతరం శుభ్రంగా ఉంచండి."
            ]
        },
        "next_season_prevention": {
            "en": "Strict crop rotation with non-host crops (legumes, cereals) and deep summer plowing.",
            "te": "పప్పుదినుసులు లేదా తృణధాన్యాలతో పంట మార్పిడి చేయండి. వేసవిలో లోతు దుక్కులు చేయండి."
        },
        "organic_management": {
            "en": "Spray 5% Neem Seed Kernel Extract (NSKE) or Fish Oil Rosin Soap (FORS) @ 25g/L water.",
            "te": "5% వేప గింజల కషాయం లేదా ఫిష్ ఆయిల్ రోసిన్ సోప్ (FORS) 25 గ్రా. లీటరు నీటికి పిచికారీ చేయండి."
        },
        "biological_control": {
            "en": "Install yellow sticky traps (25/acre) and conserve predatory mirid bugs and ladybird beetles.",
            "te": "ఎకరాకు 25 పసుపు జిగురు అట్టలు అమర్చండి మరియు అక్షింతల పురుగులను కాపాడుకోండి."
        },
        "cultural_control": {
            "en": "Border barrier crops (maize/sorghum), reflective silver mulch, and nursery net covering.",
            "te": "సరిహద్దు రక్షణ పంటలు, సిల్వర్ మల్చింగ్ మరియు దోమతెర కింద నారు పెంపకం."
        },
        "chemical_control": {
            "has_verified_chemical": True,
            "product": {
                "en": "Diafenthiuron 50% WP or Spiromesifen 22.9% SC (Targeting whitefly vector)",
                "te": "డయాఫెంథియురాన్ 50% WP లేదా స్పైరోమెసిఫెన్ 22.9% SC (తెల్లదోమ నివారణకు)"
            },
            "dosage": {
                "en": "Diafenthiuron 50% WP @ 1.25g/L water OR Spiromesifen 22.9% SC @ 1ml/L water",
                "te": "డయాఫెంథియురాన్ 50% WP @ 1.25 గ్రా./లీటర్ నీటికి లేదా స్పైరోమెసిఫెన్ 22.9% SC @ 1 మి.లీ./లీటర్ నీటికి"
            },
            "water_quantity": {
                "en": "200 Litres of spray solution per acre",
                "te": "ఎకరాకు 200 లీటర్ల పిచికారీ ద్రావణం"
            },
            "application_method": {
                "en": "Foliar spray directed thoroughly to the undersides of leaves where whiteflies colonize",
                "te": "తెల్లదోమలు ఉండే ఆకుల అడుగు భాగం పూర్తిగా తడిసేలా పిచికారీ చేయండి"
            },
            "waiting_period_phi": {
                "en": "7 days before harvesting green chillies",
                "te": "పచ్చిమిర్చి కోయడానికి ముందు 7 రోజుల వేచిఉండే కాలం"
            },
            "safety_precaution": {
                "en": "Viruses cannot be cured directly with chemicals; target only the vector whitefly.",
                "te": "వైరస్‌లను మందులతో నేరుగా చంపలేము; కేవలం వ్యాప్తి చేసే తెల్లదోమను మాత్రమే అదుపు చేయాలి."
            }
        },
        "safety_precautions": {
            "en": "Wash picked chillies thoroughly. Avoid spraying during midday heat.",
            "te": "కోసిన మిరపకాయలను శుభ్రంగా కడగండి. మధ్యాహ్నం ఎండలో పిచికారీ చేయవద్దు."
        }
    },

    "Rhizome Rot": {
        "disease": "Rhizome Rot",
        "crop": "Turmeric",
        "scientific_name": "Pythium aphanidermatum",
        "problem_type": "Fungal Disease",
        "affected_part": "Rhizomes, Roots, Pseudostems",
        "severity": "High",
        "what_is_problem": {
            "en": "Turmeric Rhizome Rot is a destructive disease caused by Pythium and Fusarium species. Initial symptoms include yellowing of lower leaf margins that progresses upward along pseudostems. The collar region becomes soft, water-soaked, and easily pulls away with a foul odor. Underground rhizomes turn brown, soft, and decay completely, causing up to 50-80% crop loss in poorly drained fields.",
            "te": "పసుపులో దుంప కుళ్ళు తెగులు (రైజోమ్ రాట్) పైథియమ్ మరియు ఫ్యుసేరియం వల్ల కలిగే అత్యంత ప్రమాదకరమైన వ్యాధి. మొదట క్రింది ఆకుల అంచులు పసుపు రంగులోకి మారి పై ఆకులకు వ్యాపిస్తాయి. మొక్క మొదలు మెత్తబడి, నీరుగారి సులభంగా ఊడివస్తుంది మరియు దుర్వాసన వస్తుంది. భూమిలోని దుంపలు కుళ్ళిపోయి ముద్దగా తయారవుతాయి. నీరు నిలిచే పొలాల్లో 50-80% వరకు పంట నష్టం కలుగుతుంది."
        },
        "why_it_occurs": {
            "en": "Excessive soil moisture, water stagnation during heavy rains, ill-drained clay soils, using uncertified infected seed rhizomes, and continuous turmeric cropping promote disease spread.",
            "te": "పొలంలో నీరు నిలకడగా ఉండటం, సరైన మురుగు కాలువలు లేకపోవడం, బంకమట్టి నేలలు, తెగులు సోకిన విత్తన దుంపలను నాటడం వల్ల ఈ తెగులు తీవ్రమవుతుంది."
        },
        "immediate_action_steps": {
            "en": [
                "Open deep drainage channels immediately to drain all stagnant water from between beds.",
                "Uproot and destroy rotting diseased clumps along with surrounding infested soil.",
                "Drench the affected spots and surrounding healthy plants with Metalaxyl + Mancozeb.",
                "Stop all surface irrigation until the soil surface dries out adequately.",
                "Consult the local horticultural officer if yellowing patches spread across ridges."
            ],
            "te": [
                "బోదెల మధ్య నిలిచిన నీటిని వెంటనే బయటకు పంపేలా లోతైన మురుగు కాలువలు తీయండి.",
                "కుళ్ళిన మొక్కలను దుంపలతో సహా తవ్వి తీసి పొలానికి దూరంగా పాతిపెట్టండి.",
                "తెగులు సోకిన ప్రదేశాలలో మెటలాక్సిల్ + మాంకోజెబ్ ద్రావణాన్ని మొదళ్ల వద్ద పోసి తడపండి.",
                "నేల ఆరే వరకు నీరు పెట్టడం పూర్తిగా నిలిపివేయండి.",
                "పసుపు పచ్చని మచ్చలు విస్తరిస్తుంటే ఉద్యానవన అధికారిని సంప్రదించండి."
            ]
        },
        "action_urgency": {
            "en": "High Urgency: Drain water immediately and spot-drench fungicide within 24 to 48 hours to stop spreading.",
            "te": "అత్యవసర చర్య అవసరం: వెంటనే నీరు తీసివేసి, 24 నుండి 48 గంటల్లోగా మొదళ్లను మందు ద్రావణంతో తడపాలి."
        },
        "prevention_steps": {
            "en": [
                "Always select healthy, plump seed rhizomes from certified disease-free fields.",
                "Treat seed rhizomes before planting with Metalaxyl-Mancozeb @ 2.5g/L water for 30 minutes.",
                "Plant strictly on raised beds (15-20 cm high) with deep furrows for rapid drainage.",
                "Apply Trichoderma viride enriched in farmyard manure (2.5 kg/acre) at planting.",
                "Practice solarization of nursery beds and rotate with non-rhizome crops."
            ],
            "te": [
                "తెగులు లేని ఆరోగ్యకరమైన విత్తన దుంపలను మాత్రమే ఎంపిక చేసుకోండి.",
                "నాటే ముందు దుంపలను మెటలాక్సిల్-మాంకోజెబ్ 2.5 గ్రా./లీటర్ నీటిలో 30 నిమిషాలు నానబెట్టి శుద్ధి చేయండి.",
                "నీరు త్వరగా బయటకు పోయేలా ఎత్తైన బోదెలపై (15-20 సెం.మీ. ఎత్తు) మాత్రమే నాటండి.",
                "ఎకరాకు 2.5 కిలోల ట్రైకోడెర్మాను పశువుల ఎరువులో కలిపి నాటే సమయంలో వేయండి.",
                "పసుపు తర్వాత మొక్కజొన్న, వరి లేదా పప్పుధాన్యాలతో పంట మార్పిడి చేయండి."
            ]
        },
        "next_season_prevention": {
            "en": "Strict 3-year crop rotation avoiding ginger and turmeric; deep summer plowing to solarize soil.",
            "te": "అల్లం, పసుపు కాకుండా ఇతర పంటలతో 3 సంవత్సరాల పంట మార్పిడి చేయండి. వేసవిలో లోతు దుక్కులు చేయండి."
        },
        "organic_management": {
            "en": "Soil drenching with 1% Bordeaux mixture or Copper Oxychloride @ 3g/L water.",
            "te": "1% బోర్డో మిశ్రమం లేదా కాపర్ ఆక్సిక్లోరైడ్ 3 గ్రా. లీటరు నీటికి కలిపి మొదళ్ల వద్ద తడపండి."
        },
        "biological_control": {
            "en": "Rhizome treatment and soil application of Trichoderma viride @ 2.5 kg/acre enriched in 250 kg FYM.",
            "te": "ట్రైకోడెర్మా విరిడె 2.5 కిలోలు ఎకరాకు పశువుల ఎరువుతో కలిపి నేలలో వేయండి."
        },
        "cultural_control": {
            "en": "Raised bed planting, free-draining channels, and removal of rotting clumps.",
            "te": "ఎత్తైన బోదెల సాగు, మురుగు కాలువలు మరియు కుళ్ళిన దుంపలను ఏరివేయడం."
        },
        "chemical_control": {
            "has_verified_chemical": True,
            "product": {
                "en": "Metalaxyl 8% + Mancozeb 64% WP",
                "te": "మెటలాక్సిల్ 8% + మాంకోజెబ్ 64% WP (రిడోమిల్)"
            },
            "dosage": {
                "en": "Metalaxyl 8% + Mancozeb 64% WP @ 2.5g/L water for soil drenching",
                "te": "మెటలాక్సిల్ 8% + మాంకోజెబ్ 64% WP @ 2.5 గ్రా./లీటర్ నీటికి కలిపి మొదళ్ల వద్ద తడపాలి"
            },
            "water_quantity": {
                "en": "300 to 400 Litres of drenching solution per acre",
                "te": "ఎకరాకు 300 నుండి 400 లీటర్ల ద్రావణం మొదళ్లు తడిసేలా పోయాలి"
            },
            "application_method": {
                "en": "Remove sprayer nozzle cap and pour drench solution directly around the base of affected beds",
                "te": "నాజిల్ క్యాప్ తీసివేసి మొక్క మొదళ్ళు మరియు దుంపలు పూర్తిగా తడిసేలా ద్రావణాన్ని పోయండి"
            },
            "waiting_period_phi": {
                "en": "60 days before rhizome harvesting",
                "te": "దుంపలు తవ్వడానికి ముందు 60 రోజుల వేచిఉండే కాలం"
            },
            "safety_precaution": {
                "en": "Wear rubber boots and gloves during soil drenching.",
                "te": "మందు పోసే సమయంలో రబ్బరు బూట్లు మరియు చేతి తొడుగులు ధరించండి."
            }
        },
        "safety_precautions": {
            "en": "Do not let chemical runoff enter ponds or cattle watering troughs.",
            "te": "మందు కలిసిన మురుగు నీటిని పశువుల తొట్లు లేదా చెరువుల్లోకి పోనివ్వవద్దు."
        }
    },

    "Whitefly": {
        "disease": "Whitefly",
        "crop": "Cotton",
        "scientific_name": "Bemisia tabaci",
        "problem_type": "Insect Pest",
        "affected_part": "Foliage, Lower leaf surface",
        "severity": "Moderate to High",
        "what_is_problem": {
            "en": "Whitefly is a destructive sucking pest of cotton. Tiny white-winged insects and scale-like nymphs congregate on leaf undersides, sucking phloem sap. They excrete sticky honeydew that fosters black sooty mold fungus on leaves and open bolls, hindering photosynthesis and staining lint. It also transmits deadly Cotton Leaf Curl Virus, causing 25-50% yield reduction.",
            "te": "పత్తిలో తెల్లదోమ రసం పీల్చే అత్యంత ప్రమాదకరమైన పురుగు. తెల్లని రెక్కలు కలిగిన సూక్ష్మ పురుగులు ఆకుల అడుగున చేరి రసాన్ని పీల్చుతాయి. ఇవి తేనె వంటి జిగురు పదార్థాన్ని విసర్జించడం వల్ల ఆకులపై నల్లని మసి తెగులు (సూటీ మోల్డ్) ఏర్పడి కిరణజన్య సంయోగక్రియ దెబ్బతింటుంది. దూది నల్లబడి నాణ్యత కోల్పోతుంది మరియు లీఫ్ కర్ల్ వైరస్‌ను వ్యాపింపజేసి 25-50% దిగుబడి నష్టం కలిగిస్తుంది."
        },
        "why_it_occurs": {
            "en": "Dry spells with high temperatures (32-38°C), low rainfall, excess use of urea, and indiscriminate early spraying of synthetic pyrethroids (destroying natural predators like ladybird beetles and lace wings) cause whitefly outbreaks.",
            "te": "వర్షాభావం, అధిక ఎండ తీవ్రత (32-38°C), అధిక నత్రజని వాడకం మరియు ప్రారంభంలో సింథటిక్ పైరెథ్రాయిడ్స్ మందులు వాడటం వల్ల మిత్రపురుగులు చనిపోయి తెల్లదోమ ఉధృతమవుతుంది."
        },
        "immediate_action_steps": {
            "en": [
                "Install 20 to 25 yellow sticky traps per acre slightly above canopy height.",
                "Spray 5% Neem Seed Kernel Extract (NSKE) or Neem Oil 1500 ppm @ 5ml/L immediately.",
                "Stop applying excessive nitrogenous fertilizers (urea).",
                "Direct spray nozzles upward to thoroughly coat leaf undersides.",
                "Consult the local cotton scientist if nymphs exceed 6-8 per leaf."
            ],
            "te": [
                "ఎకరాకు 20 నుండి 25 పసుపు జిగురు అట్టలను పైరు ఎత్తులో అమర్చి పురుగులను బంధించండి.",
                "వెంటనే 5% వేప గింజల కషాయం లేదా వేప నూనె 5 మి.లీ. లీటరు నీటికి కలిపి పిచికారీ చేయండి.",
                "యూరియా ఎరువును ఎక్కువగా వేయడం ఆపండి.",
                "ఆకుల అడుగు భాగం పూర్తిగా తడిసేలా నాజిల్‌ను పైకి గురిపెట్టి పిచికారీ చేయండి.",
                "ఆకుకు 6-8 కంటే ఎక్కువ పిల్ల పురుగులు కనిపిస్తే శాస్త్రవేత్తలను సంప్రదించండి."
            ]
        },
        "action_urgency": {
            "en": "Moderate Urgency: Install yellow sticky traps within 24 hours; commence spray when nymph counts exceed 6-8/leaf.",
            "te": "మధ్యస్థ అత్యవసరం: 24 గంటల్లోగా పసుపు జిగురు అట్టలు అమర్చాలి; ఆకుకు 6-8 పురుగులు ఉంటే పిచికారీ చేయాలి."
        },
        "prevention_steps": {
            "en": [
                "Sow tolerant varieties or hybrids recommended by agricultural universities.",
                "Avoid monoculture; plant barrier crops like maize or sorghum around cotton fields.",
                "Maintain optimal plant density and practice timely weed control.",
                "Apply balanced potash to toughen leaf tissues against piercing mouthparts.",
                "Avoid repetitive use of synthetic pyrethroids."
            ],
            "te": [
                "విశ్వవిద్యాలయం సిఫారసు చేసిన తెల్లదోమను తట్టుకునే రకాలను సాగు చేయండి.",
                "చేను చుట్టూ జొన్న లేదా మొక్కజొన్నను సరిహద్దు పంటగా వేయండి.",
                "మొక్కల మధ్య సరైన దూరం పాటించి కలుపు లేకుండా చూసుకోండి.",
                "ఆకులు గట్టిపడేలా పొటాష్ ఎరువును సమతుల్యంగా వేయండి.",
                "పైరెథ్రాయిడ్స్ మందులను పదే పదే వాడవద్దు."
            ]
        },
        "next_season_prevention": {
            "en": "Crop rotation with non-host crops, deep summer plowing, and timely destruction of cotton stalks by January.",
            "te": "పంట మార్పిడి పాటించండి. వేసవిలో లోతు దుక్కులు చేసి జనవరి నాటికే పత్తి కట్టెను తొలగించండి."
        },
        "organic_management": {
            "en": "Spray 5% Neem Seed Kernel Extract (NSKE) or Fish Oil Rosin Soap (FORS) @ 25g/L water.",
            "te": "5% వేప గింజల కషాయం లేదా ఫిష్ ఆయిల్ రోసిన్ సోప్ (FORS) 25 గ్రా. లీటరు నీటికి పిచికారీ చేయండి."
        },
        "biological_control": {
            "en": "Install yellow sticky traps (25/acre) and conserve parasitoid Encarsia and Chrysoperla predators.",
            "te": "ఎకరాకు 25 పసుపు జిగురు అట్టలు అమర్చండి మరియు క్రైసోపా మిత్రపురుగులను రక్షించుకోండి."
        },
        "cultural_control": {
            "en": "Grow border barrier crops (sorghum/maize) and install yellow sticky traps.",
            "te": "సరిహద్దు పంటల సాగు మరియు పసుపు జిగురు అట్టల ఏర్పాటు."
        },
        "chemical_control": {
            "has_verified_chemical": True,
            "product": {
                "en": "Diafenthiuron 50% WP or Pyriproxyfen 10% EC",
                "te": "డయాఫెంథియురాన్ 50% WP లేదా పైరిప్రాక్సిఫెన్ 10% EC"
            },
            "dosage": {
                "en": "Diafenthiuron 50% WP @ 1.25g/L water OR Pyriproxyfen 10% EC @ 2ml/L water",
                "te": "డయాఫెంథియురాన్ 50% WP @ 1.25 గ్రా./లీటర్ నీటికి లేదా పైరిప్రాక్సిఫెన్ 10% EC @ 2 మి.లీ./లీటర్ నీటికి"
            },
            "water_quantity": {
                "en": "200 Litres of spray solution per acre",
                "te": "ఎకరాకు 200 లీటర్ల పిచికారీ ద్రావణం"
            },
            "application_method": {
                "en": "Fine spray directed strictly upward to wet leaf undersides using hollow cone nozzle",
                "te": "ఆకుల అడుగు భాగం పూర్తిగా తడిసేలా నాజిల్‌ను పైకి పెట్టి పిచికారీ చేయండి"
            },
            "waiting_period_phi": {
                "en": "30 days before harvest",
                "te": "పంట కోతకు ముందు 30 రోజుల వేచిఉండే కాలం"
            },
            "safety_precaution": {
                "en": "Do not spray during extreme midday heat; wear protective eyewear and face mask.",
                "te": "మధ్యాహ్నం తీవ్రమైన ఎండలో పిచికారీ చేయవద్దు. కంటి అద్దాలు మరియు మాస్క్ ధరించండి."
            }
        },
        "safety_precautions": {
            "en": "Rotate chemical groups between sprays to prevent rapid insecticide resistance.",
            "te": "పురుగులకు మందులపై రోగనిరోధక శక్తి రాకుండా ఉండటానికి మందుల గ్రూపులను మార్చి పిచికారీ చేయండి."
        }
    },

    "Yellow Vein Mosaic Virus": {
        "disease": "Yellow Vein Mosaic Virus",
        "crop": "Okra",
        "scientific_name": "Bhendi yellow vein mosaic virus (BYVMV)",
        "problem_type": "Viral Disease",
        "affected_part": "Leaves, Veins, Fruits",
        "severity": "High",
        "what_is_problem": {
            "en": "Bhendi Yellow Vein Mosaic Virus is the most serious disease of okra, transmitted by whiteflies. Leaves develop a striking network of bright yellow veins interlaced with green tissue. As the disease advances, leaves become completely yellow, plants remain stunted, and fruits turn yellow-white, hard, fibrous, and unmarketable, causing up to 80-90% crop loss if infection occurs early.",
            "te": "బెండలో పల్లాకు తెగులు లేదా పసుపు ఈనెల వైరస్ (YVMV) తెల్లదోమ ద్వారా వ్యాపించే అత్యంత తీవ్రమైన వ్యాధి. ఆకుల ఈనెలు పసుపు రంగులోకి మారి వలలాగా కనిపిస్తాయి. తెగులు ముదిరితే ఆకులు పూర్తిగా పసుపుపచ్చగా మారి మొక్క ఎదుగుదల ఆగిపోతుంది. కాయలు కూడా పసుపు-తెలుపు రంగులోకి మారి గట్టిపడి మార్కెట్‌కు పనికిరాకుండా పోతాయి. దీనివల్ల 80-90% వరకు పంట నష్టం కలుగుతుంది."
        },
        "why_it_occurs": {
            "en": "High population density of whiteflies (Bemisia tabaci), warm and humid weather, sowing susceptible varieties, and wild malvaceous weed hosts along field bunds facilitate disease explosion.",
            "te": "తెల్లదోమల ఉధృతి ఎక్కువగా ఉండటం, వేడి తేమతో కూడిన వాతావరణం, తెగులును తట్టుకోలేని రకాలను నాటడం మరియు గట్లపై కలుపు మొక్కలు ఉండటం వల్ల ఈ వైరస్ వేగంగా వ్యాపిస్తుంది."
        },
        "immediate_action_steps": {
            "en": [
                "Rogue out and destroy infected yellow plants immediately in early crop stage.",
                "Install 20 yellow sticky traps per acre to capture flying whiteflies.",
                "Spray 5% Neem Seed Kernel Extract (NSKE) or Neem Oil 1500 ppm @ 5ml/L water.",
                "Destroy wild malvaceous weeds (like Abutilon and Sida) on field borders.",
                "Consult local agricultural officer if more than 5% of plants show yellow veins."
            ],
            "te": [
                "ప్రారంభ దశలో తెగులు సోకిన పసుపు మొక్కలను పీకి పొలానికి దూరంగా తగులబెట్టండి.",
                "ఎకరాకు 20 పసుపు రంగు జిగురు అట్టలను అమర్చి తెల్లదోమలను అదుపు చేయండి.",
                "5% వేప గింజల కషాయం లేదా వేప నూనె 5 మి.లీ. లీటరు నీటికి కలిపి పిచికారీ చేయండి.",
                "చేను గట్లపై ఉండే కలుపు మొక్కలను పూర్తిగా నాశనం చేయండి.",
                "5% కంటే ఎక్కువ మొక్కలలో పసుపు ఈనెలు కనిపిస్తే వ్యవసాయ అధికారిని సంప్రదించండి."
            ]
        },
        "action_urgency": {
            "en": "High Urgency: Remove infected plants and install yellow sticky traps within 24 hours.",
            "te": "అత్యవసర చర్య అవసరం: 24 గంటల్లోగా వైరస్ మొక్కలను పీకివేయాలి మరియు పసుపు జిగురు అట్టలు అమర్చాలి."
        },
        "prevention_steps": {
            "en": [
                "Sow YVMV-resistant varieties like Parbhani Kranti, Arka Anamika, or Kashi Kranti.",
                "Treat seed with Imidacloprid 70% WS @ 5g/kg seed before sowing.",
                "Plant 2-3 border rows of maize or sorghum to obstruct incoming whitefly vectors.",
                "Avoid growing okra in close proximity to cotton or other solanaceous crops.",
                "Maintain clean weeding throughout the vegetative phase."
            ],
            "te": [
                "పర్భని క్రాంతి, అర్కా అనామిక, కాశీ క్రాంతి వంటి వైరస్ నిరోధక రకాలను మాత్రమే సాగు చేయండి.",
                "విత్తే ముందు కిలో విత్తనానికి ఇమిడాక్లోప్రిడ్ @ 5 గ్రా. కలిపి విత్తన శుద్ధి చేయండి.",
                "చేను చుట్టూ 2-3 వరుసలలో జొన్న లేదా మొక్కజొన్నను సరిహద్దు పంటగా వేయండి.",
                "పత్తి పంటకు దగ్గరగా బెండను సాగు చేయవద్దు.",
                "మొక్కల ఎదుగుదల దశలో కలుపు లేకుండా నిరంతరం శుభ్రంగా ఉంచండి."
            ]
        },
        "next_season_prevention": {
            "en": "Crop rotation with non-malvaceous crops (cereals, legumes) and deep summer plowing.",
            "te": "పప్పుదినుసులు లేదా తృణధాన్యాలతో పంట మార్పిడి చేయండి. వేసవిలో లోతు దుక్కులు చేయండి."
        },
        "organic_management": {
            "en": "Foliar spray with 5% Neem Seed Kernel Extract (NSKE) or Fish Oil Rosin Soap @ 25g/L.",
            "te": "5% వేప గింజల కషాయం లేదా ఫిష్ ఆయిల్ రోసిన్ సోప్ 25 గ్రా. లీటరు నీటికి పిచికారీ చేయండి."
        },
        "biological_control": {
            "en": "Install yellow sticky traps (20/acre) and conserve predatory ladybird beetles.",
            "te": "ఎకరాకు 20 పసుపు జిగురు అట్టలు అమర్చండి మరియు అక్షింతల పురుగులను కాపాడుకోండి."
        },
        "cultural_control": {
            "en": "Resistant varieties (Arka Anamika), border barrier crops, and roguing infected plants.",
            "te": "నిరోధక రకాల సాగు (అర్కా అనామిక), సరిహద్దు పంటలు మరియు రోగగ్రస్థ మొక్కలను పీకివేయడం."
        },
        "chemical_control": {
            "has_verified_chemical": True,
            "product": {
                "en": "Diafenthiuron 50% WP or Acetamiprid 20% SP (For whitefly vector control)",
                "te": "డయాఫెంథియురాన్ 50% WP లేదా ఎసిటామ్రిప్రిడ్ 20% SP (తెల్లదోమ నివారణకు)"
            },
            "dosage": {
                "en": "Diafenthiuron 50% WP @ 1.25g/L water OR Acetamiprid 20% SP @ 0.2g/L water",
                "te": "డయాఫెంథియురాన్ 50% WP @ 1.25 గ్రా./లీటర్ నీటికి లేదా ఎసిటామ్రిప్రిడ్ 20% SP @ 0.2 గ్రా./లీటర్ నీటికి"
            },
            "water_quantity": {
                "en": "200 Litres of spray solution per acre",
                "te": "ఎకరాకు 200 లీటర్ల పిచికారీ ద్రావణం"
            },
            "application_method": {
                "en": "Foliar spray directed to the undersides of leaves where whiteflies feed",
                "te": "తెల్లదోమలు ఉండే ఆకుల అడుగు భాగం తడిసేలా పిచికారీ చేయండి"
            },
            "waiting_period_phi": {
                "en": "3 to 5 days before picking tender okra fruits",
                "te": "కాయలు కోయడానికి ముందు 3 నుండి 5 రోజుల వేచిఉండే కాలం (PHI)"
            },
            "safety_precaution": {
                "en": "Pick all harvestable bhendi fruits before spraying chemicals.",
                "te": "మందు పిచికారీ చేయడానికి ముందే కోతకు వచ్చిన కాయలను పూర్తిగా కోసివేయండి."
            }
        },
        "safety_precautions": {
            "en": "Wash picked okra thoroughly before cooking or selling.",
            "te": "కోసిన బెండకాయలను మంచి నీటితో శుభ్రంగా కడగండి."
        }
    }
}

# Add default fallback dossier for general queries
DEFAULT_DOSSIER: Dict[str, Any] = {
    "disease": "Agricultural Advisory",
    "crop": "General Crop",
    "problem_type": "Crop Condition",
    "severity": "Moderate",
    "what_is_problem": {
        "en": "The observed crop symptoms require structured diagnosis and management based on integrated pest management principles.",
        "te": "గుర్తించిన పంట లక్షణాలకు సమగ్ర సస్యరక్షణ పద్ధతుల ఆధారంగా సరైన యాజమాన్య చర్యలు చేపట్టాలి."
    },
    "why_it_occurs": {
        "en": "Weather fluctuations, relative humidity extremes, unbalanced nutrient application, and pest vectors contribute to crop stress.",
        "te": "వాతావరణ మార్పులు, గాలిలో అధిక తేమ, అసమతుల్య ఎరువుల వాడకం మరియు పురుగుల వ్యాప్తి పంట ఒత్తిడికి కారణమవుతాయి."
    },
    "immediate_action_steps": {
        "en": [
            "Inspect the field thoroughly to determine symptom spread across ridges.",
            "Regulate irrigation to avoid waterlogging or drought stress.",
            "Avoid excessive nitrogenous fertilizer application until diagnosis is clear.",
            "Remove and destroy severely affected leaves away from the field.",
            "Consult the local Mandal Agricultural Officer (MAO) or KVK scientists."
        ],
        "te": [
            "పొలాన్ని నిశితంగా పరిశీలించి లక్షణాలు ఎంతవరకు వ్యాపించాయో గుర్తించండి.",
            "నీరు నిలవకుండా లేదా బెట్ట రాకుండా తగినంత నీటిని సమతుల్యంగా అందించండి.",
            "ఖచ్చితమైన నిర్ధారణ అయ్యే వరకు అధిక నత్రజని ఎరువులు వేయవద్దు.",
            "తీవ్రంగా దెబ్బతిన్న ఆకులను ఏరివేసి పొలానికి దూరంగా నాశనం చేయండి.",
            "స్థానిక మండల వ్యవసాయ అధికారి (MAO) లేదా KVK శాస్త్రవేత్తలను సంప్రదించండి."
        ]
    },
    "action_urgency": {
        "en": "Moderate Urgency: Monitor field symptoms closely over the next 48 hours.",
        "te": "మధ్యస్థ అత్యవసరం: రాబోయే 48 గంటల్లో లక్షణాలను గమనిస్తూ నివారణ చర్యలు చేపట్టండి."
    },
    "prevention_steps": {
        "en": [
            "Practice regular field sanitation and remove crop residues.",
            "Ensure balanced fertilization based on soil health card recommendations.",
            "Maintain optimal plant spacing to allow good air circulation.",
            "Adopt crop rotation with non-host crops."
        ],
        "te": [
            "పొలాన్ని ఎల్లప్పుడూ శుభ్రంగా ఉంచుకోండి మరియు పంట అవశేషాలను తొలగించండి.",
            "భూసార పరీక్ష ఆధారంగా సమతుల్య ఎరువులను వాడండి.",
            "మొక్కల మధ్య తగిన దూరం ఉండేలా చూసుకోండి.",
            "పంట మార్పిడిని క్రమం తప్పకుండా పాటించండి."
        ]
    },
    "next_season_prevention": {
        "en": "Deep summer ploughing and seed treatment with recommended bio-agents prior to sowing.",
        "te": "వేసవిలో లోతు దుక్కులు చేయండి మరియు విత్తే ముందు విత్తన శుద్ధి తప్పనిసరిగా చేయండి."
    },
    "organic_management": {
        "en": "Spray 5% Neem Seed Kernel Extract (NSKE) or Neem Oil 1500 ppm @ 5ml/L water as a general protective measure.",
        "te": "సాధారణ రక్షణ చర్యగా 5% వేప గింజల కషాయం లేదా వేప నూనె 5 మి.లీ. లీటరు నీటికి కలిపి పిచికారీ చేయండి."
    },
    "biological_control": {
        "en": "Apply Trichoderma viride or Pseudomonas fluorescens @ 5g/L water for biological suppression.",
        "te": "ట్రైకోడెర్మా విరిడె లేదా సూడోమోనాస్ ఫ్లోరోసెన్స్ 5 గ్రాములు లీటరు నీటికి కలిపి పిచికారీ చేయండి."
    },
    "cultural_control": {
        "en": "Maintain field sanitation, proper weed management, and balanced irrigation schedules.",
        "te": "పొలం పరిశుభ్రత పాటించండి, కలుపు లేకుండా చూసుకోండి మరియు సరైన సమయాల్లో నీరు పెట్టండి."
    },
    "chemical_control": {
        "has_verified_chemical": False,
        "unverified_reason": {
            "en": "No verified chemical recommendation is available for this diagnosis. Do not spray chemicals without confirmed diagnosis.",
            "te": "ఈ నిర్ధారణకు ధృవీకరించబడిన రసాయన సిఫారసు అందుబాటులో లేదు. ఖచ్చితమైన నిర్ధారణ లేకుండా పురుగుమందులు వాడవద్దు."
        }
    },
    "safety_precautions": {
        "en": "Always wear protective gloves and face mask when handling agricultural formulations.",
        "te": "పురుగుమందులు వాడేటప్పుడు చేతి తొడుగులు మరియు మాస్క్ తప్పనిసరిగా ధరించండి."
    }
}


def get_catalog_entry(disease_name: str, crop_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Retrieves the verified catalog profile for a disease.
    Supports case-insensitive matching and alias resolution.
    """
    if not disease_name:
        return None
    d_clean = disease_name.strip().lower()

    # Exact match
    for k, v in ADVISORY_CATALOG.items():
        if k.lower() == d_clean:
            return v

    # Substring match
    for k, v in ADVISORY_CATALOG.items():
        if k.lower() in d_clean or d_clean in k.lower():
            return v

    return None
