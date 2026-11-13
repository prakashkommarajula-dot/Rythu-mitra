"""
=============================================================================
Rythu Mithra - AI-Based Multilingual Crop Disease & Pest Detection
Service: crop_symptoms_service.py
Crop-Specific Quick Add Symptom Catalog & Diagnostic Questions Generator
Derived directly from ANGRAU / ICAR / PJTSAU dataset corpora:
- data/processed/cleaned_corpus.csv
- data/processed/diagnosis_fallback.csv
=============================================================================
"""

from typing import Dict, Any, List, Optional
from services.advisory_service import normalize_crop_name

# Dataset-derived Crop Symptom & Pest Problem Catalog
# Each chip contains verified Telugu & English labels and symptom snippets.
CROP_SYMPTOM_CATALOG: Dict[str, Dict[str, Any]] = {
    "Groundnut": {
        "crop": "Groundnut",
        "crop_te": "వేరుశనగ",
        "major_diseases": ["Tikka Leaf Spot", "Leaf Miner", "Collar Rot"],
        "symptoms": [
            {
                "id": "gn_tikka_spots",
                "label_en": "Yellow & brown leaf spots",
                "label_te": "ఆకులపై పసుపు, గోధుమ మచ్చలు",
                "symptom_en": "Dark brown circular spots with a yellow ring are forming on groundnut leaves.",
                "symptom_te": "వేరుశనగ ఆకుల మీద నల్లటి, గోధుమ రంగు మచ్చలు ఏర్పడి చుట్టూ పసుపు వలయం కనిపిస్తోంది.",
                "disease": "Tikka Leaf Spot"
            },
            {
                "id": "gn_leaf_shedding",
                "label_en": "Premature leaf shedding",
                "label_te": "ఆకులు ముందుగానే రాలిపోవడం",
                "symptom_en": "Groundnut leaves are drying up and shedding prematurely.",
                "symptom_te": "వేరుశనగ తోటలో ఆకులు ముందుగానే రాలిపోయి మొక్కలు మోడువారుతున్నాయి.",
                "disease": "Tikka Leaf Spot"
            },
            {
                "id": "gn_leaf_miner_tunnels",
                "label_en": "Leaf miner white tunnels",
                "label_te": "ఆకులపై తెల్లటి సొరంగాలు (గీతలు)",
                "symptom_en": "White streaks like tunnels and mines are visible on groundnut leaves.",
                "symptom_te": "వేరుశనగ ఆకులపై తెల్లటి గీతలు, సొరంగాల వంటి మచ్చలు కనిపిస్తున్నాయి.",
                "disease": "Leaf Miner"
            },
            {
                "id": "gn_folded_leaves",
                "label_en": "Folded & webbed leaves",
                "label_te": "ముడుచుకున్న ఆకులు (లోపల పురుగు)",
                "symptom_en": "Groundnut leaves are folded together with small larvae webbed inside.",
                "symptom_te": "ఆకులు ఒకదానికొకటి ముడుచుకుని లోపల చిన్న గొంగళి పురుగు ఆకు పచ్చదనాన్ని తింటోంది.",
                "disease": "Leaf Miner"
            },
            {
                "id": "gn_collar_rot",
                "label_en": "Seedling wilting / collar rot",
                "label_te": "మొలకలు వాడిపోవడం / మొదలు కుళ్లు",
                "symptom_en": "Groundnut seedlings are wilting and base of stem is rotting near soil line.",
                "symptom_te": "మొలక దశలోనే మొక్కలు వాడిపోయి, మొదలు భాగం కుళ్ళిపోతోంది.",
                "disease": "Collar Rot"
            },
            {
                "id": "gn_caterpillar",
                "label_en": "Caterpillar defoliation",
                "label_te": "గొంగళి పురుగు ఆకులను తినడం",
                "symptom_en": "Caterpillars are aggressively chewing groundnut leaves leaving only veins.",
                "symptom_te": "పురుగులు వేరుశనగ ఆకులను కొరికి తిని ఈనెలను మాత్రమే మిగులుస్తున్నాయి.",
                "disease": "Spodoptera / Leaf Miner"
            }
        ],
        "diagnostic_questions": {
            "te": [
                "విత్తనశుద్ధి చేశారా?",
                "నేలలో తేమ ఎక్కువగా ఉండి నీరు నిలిచిందా?",
                "మొక్క మొదలు భాగంలో తెల్లటి బూజు లేదా కుళ్ళు కనిపిస్తోందా?",
                "ఆకుల అడుగు భాగంలో నల్లటి మచ్చలు స్పష్టంగా ఉన్నాయా?"
            ],
            "en": [
                "Was seed treatment carried out before sowing?",
                "Is there excessive moisture or water stagnation in the soil?",
                "Is white mycelium or rot visible at the collar region near soil line?",
                "Are dark circular spots prominent on the lower leaf surface?"
            ]
        }
    },
    "Rice": {
        "crop": "Rice",
        "crop_te": "వరి",
        "major_diseases": ["Blast", "Brown Planthopper", "Stem Borer"],
        "symptoms": [
            {
                "id": "rice_blast_spindle",
                "label_en": "Spindle-shaped brown lesions",
                "label_te": "కండె ఆకారపు గోధుమ మచ్చలు",
                "symptom_en": "Spindle-shaped spots with grey centers and brown margins on paddy leaves.",
                "symptom_te": "వరి ఆకులపై కండె ఆకారపు బూడిద రంగు కేంద్రం గల గోధుమ మచ్చలు కనిపిస్తున్నాయి.",
                "disease": "Blast"
            },
            {
                "id": "rice_neck_rot",
                "label_en": "Neck blast / panicle rot",
                "label_te": "మెడ విరుపు / వెన్ను నల్లబడటం",
                "symptom_en": "Panicle base is turning black and breaking, resulting in chaffy white ears.",
                "symptom_te": "వరి వెన్ను మొదలు నల్లబడి విరిగిపోతోంది, గింజలు తాలుగా మారుతున్నాయి.",
                "disease": "Blast"
            },
            {
                "id": "rice_hopper_burn",
                "label_en": "Hopper burn circular drying",
                "label_te": "సుడిదోమ వల్ల వలయాకార ఎండటం",
                "symptom_en": "Circular patches in the paddy field are drying up rapidly due to hopper burn.",
                "symptom_te": "పొలంలో అక్కడక్కడా గుండ్రంగా పైరు ఎండిపోయి సుడిదోమ నష్టం కనిపిస్తోంది.",
                "disease": "Brown Planthopper"
            },
            {
                "id": "rice_stem_insects",
                "label_en": "Brown hoppers at stem base",
                "label_te": "మొక్కల మొదళ్ల వద్ద గోధుమ రంగు దోమలు",
                "symptom_en": "Small brown insects are clustered at the base of rice tillers near water surface.",
                "symptom_te": "నీటి పైభాగంలో వరి దుబ్బుల మొదళ్ల వద్ద గోధుమ రంగు పురుగులు గుంపులుగా ఉన్నాయి.",
                "disease": "Brown Planthopper"
            },
            {
                "id": "rice_yellowing_tips",
                "label_en": "Yellow leaf tips & wilting",
                "label_te": "ఆకు చివర్లు పసుపు రంగులోకి మారడం",
                "symptom_en": "The tips of rice leaves are turning yellow and drying downwards.",
                "symptom_te": "వరి ఆకుల చివర్లు పసుపు రంగులోకి మారి కిందికి ఎండిపోతున్నాయి.",
                "disease": "Requires further diagnosis"
            },
            {
                "id": "rice_dead_heart",
                "label_en": "Dead heart in central shoot",
                "label_te": "పిలకల సుడి చనిపోవడం (డెడ్ హార్ట్)",
                "symptom_en": "Central tillers are drying up and easily pull out (dead heart symptom).",
                "symptom_te": "వరి దుబ్బుల్లోని మధ్య పిలకలు ఎండిపోయి సులభంగా ఊడివస్తున్నాయి.",
                "disease": "Stem Borer"
            }
        ],
        "diagnostic_questions": {
            "te": [
                "ఆకుల చివర్లు మాత్రమే పసుపుగా ఉన్నాయా లేక ఆకు మొత్తం ప్రభావితమైందా?",
                "పొలంలో నీరు ఎక్కువసేపు నిలిచి తేమ అధికంగా ఉందా?",
                "మొక్కల మొదళ్ల వద్ద గోధుమ రంగు పురుగులు లేదా తేనె వంటి జిగురు ఉందా?",
                "మచ్చలు కండె ఆకారంలో ఉన్నాయా లేక గుండ్రంగా ఉన్నాయా?"
            ],
            "en": [
                "Are only leaf tips yellowing or is the entire leaf blade discolored?",
                "Is there prolonged water stagnation and excessive nitrogen use?",
                "Are small brown planthoppers or honeydew secretions present at stem bases?",
                "Are lesions spindle-shaped with greyish centers or circular?"
            ]
        }
    },
    "Cotton": {
        "crop": "Cotton",
        "crop_te": "పత్తి",
        "major_diseases": ["Pink Bollworm", "Whitefly", "Leaf Curl"],
        "symptoms": [
            {
                "id": "cotton_boll_holes",
                "label_en": "Boll holes & stained lint",
                "label_te": "కాయలకు రంధ్రాలు & రంగు మారిన దూది",
                "symptom_en": "Small bore holes on cotton bolls with pink larva inside and stained lint.",
                "symptom_te": "పత్తి కాయలకు రంధ్రాలు పడి లోపల గులాబీ రంగు పురుగు దూదిని తిని పాడుచేస్తోంది.",
                "disease": "Pink Bollworm"
            },
            {
                "id": "cotton_rosette_flower",
                "label_en": "Rosette flowers (not opening)",
                "label_te": "గులాబీ పువ్వులా ముడుచుకున్న పూలు",
                "symptom_en": "Flowers fail to open properly and remain twisted like rosette petals.",
                "symptom_te": "పత్తి పూలు విచ్చుకోకుండా ముడుచుకుపోయి రాలిపోతున్నాయి.",
                "disease": "Pink Bollworm"
            },
            {
                "id": "cotton_whitefly_sooty",
                "label_en": "Whiteflies under leaves & sooty mould",
                "label_te": "ఆకుల కింద తెల్లదోమ & నల్లటి బూజు",
                "symptom_en": "Underside of leaves covered with whiteflies and upper surface has black sooty mould.",
                "symptom_te": "ఆకుల అడుగు భాగం తెల్లదోమతో నిండి ఉంది, ఆకులపై నల్లటి మసి బూజు ఏర్పడింది.",
                "disease": "Whitefly"
            },
            {
                "id": "cotton_leaf_curl",
                "label_en": "Leaf curling & thickening",
                "label_te": "ఆకులు పైకి ముడుచుకోవడం & దళసరి కావడం",
                "symptom_en": "Cotton leaves are curling upwards and veins are thickened.",
                "symptom_te": "పత్తి ఆకులు పైకి దోనెలా ముడుచుకుని ఈనెలు గట్టిపడి ఎదుగుదల తగ్గింది.",
                "disease": "Leaf Curl / Whitefly"
            },
            {
                "id": "cotton_leaf_reddening",
                "label_en": "Leaf reddening & drying",
                "label_te": "ఆకులు ఎర్రబారడం & ఎండిపోవడం",
                "symptom_en": "Lower leaves are turning reddish-purple and drying from edges.",
                "symptom_te": "పత్తి ఆకులు ఎర్రగా మారి అంచుల నుంచి ఎండిపోతున్నాయి.",
                "disease": "Requires further diagnosis"
            },
            {
                "id": "cotton_boll_drop",
                "label_en": "Premature boll & square drop",
                "label_te": "పిందెలు, కాయలు రాలిపోవడం",
                "symptom_en": "Small cotton squares and young bolls are shedding heavily.",
                "symptom_te": "పత్తి తోటలో లేత పిందెలు మరియు కాయలు విపరీతంగా రాలిపోతున్నాయి.",
                "disease": "Pink Bollworm / Stress"
            }
        ],
        "diagnostic_questions": {
            "te": [
                "కాయలను తెరిచి చూస్తే లోపల గులాబీ రంగు పురుగు లేదా విత్తనాలు తిన్న ఆనవాళ్లు ఉన్నాయా?",
                "ఆకుల అడుగు భాగంలో తెల్లటి రెక్కల పురుగులు కదులుతున్నాయా?",
                "ఆకులపై జిగురు లేదా నల్లటి మసి లాంటి పొర కనిపిస్తోందా?",
                "నేలలో మెగ్నీషియం లేదా పొటాష్ పోషక లోపం ఉండే అవకాశం ఉందా?"
            ],
            "en": [
                "When young bolls are opened, are pink caterpillars or damaged seeds found inside?",
                "Are tiny white-winged insects actively fluttering under the leaf surface?",
                "Is sticky honeydew or black sooty fungus present on leaf surfaces?",
                "Could nutritional deficiency (magnesium or potassium) be causing leaf reddening?"
            ]
        }
    },
    "Chilli": {
        "crop": "Chilli",
        "crop_te": "మిరప",
        "major_diseases": ["Thrips", "Leaf Curl Virus", "Fruit Rot (Anthracnose)"],
        "symptoms": [
            {
                "id": "chilli_upward_curl",
                "label_en": "Upward curling & silvery leaves",
                "label_te": "పైకి ముడుచుకున్న ఆకులు & వెండి మెరుపు",
                "symptom_en": "Chilli leaves are curling upward like a boat with silvery patches beneath.",
                "symptom_te": "మిరప ఆకులు దోనెలా పైకి ముడుచుకుని అడుగు భాగంలో వెండి రంగు మెరుపు కనిపిస్తోంది.",
                "disease": "Thrips"
            },
            {
                "id": "chilli_thrips_damage",
                "label_en": "Thrips scratching & flower drop",
                "label_te": "తామర పురుగు నష్టం & పూత రాలడం",
                "symptom_en": "Tiny insects scratching young leaves and flowers resulting in heavy flower drop.",
                "symptom_te": "చిన్న పురుగులు లేత చిగుళ్లను గోకి రసం పీల్చడం వల్ల పూత రాలిపోతోంది.",
                "disease": "Thrips"
            },
            {
                "id": "chilli_leaf_curl_virus",
                "label_en": "Severe downward curl & stunting",
                "label_te": "కిందికి ముడుచుకున్న ఆకులు & గిడసబారడం",
                "symptom_en": "Leaves severely curled downwards, puckered, with bushy stunted plant growth.",
                "symptom_te": "ఆకులు కిందికి ముడుచుకుని ముడతలు పడి మొక్క గిడసబారి గుబురుగా మారింది.",
                "disease": "Leaf Curl Virus"
            },
            {
                "id": "chilli_fruit_rot",
                "label_en": "Sunken dark spots on ripe fruits",
                "label_te": "కాయలపై నల్లటి మచ్చలు & కుళ్లు (కొమ్మకుళ్లు)",
                "symptom_en": "Circular sunken dark spots appearing on red chillies with concentric black dots.",
                "symptom_te": "పండిన మిరప కాయలపై గుండ్రటి నల్లటి మచ్చలు ఏర్పడి కాయలు ఎండి కుళ్ళిపోతున్నాయి.",
                "disease": "Fruit Rot / Anthracnose"
            },
            {
                "id": "chilli_shoot_drying",
                "label_en": "Die-back / tip drying",
                "label_te": "కొమ్మలు పైనుంచి ఎండిపోవడం (డై-బ్యాక్)",
                "symptom_en": "Twigs and branches drying from tip downwards turning straw-colored.",
                "symptom_te": "మిరప కొమ్మలు పైనుంచి కిందికి ఎండుతూ గడ్డి రంగులోకి మారుతున్నాయి.",
                "disease": "Die-back / Anthracnose"
            },
            {
                "id": "chilli_yellowing",
                "label_en": "Yellow leaves & poor fruit set",
                "label_te": "ఆకులు పసుపుబారడం & పిందె కట్టకపోవడం",
                "symptom_en": "Leaves turning pale yellow with poor flowering and fruit set.",
                "symptom_te": "ఆకులు పసుపు రంగులోకి మారి పూత పిందె సరిగ్గా నిలవడం లేదు.",
                "disease": "Requires further diagnosis"
            }
        ],
        "diagnostic_questions": {
            "te": [
                "ఆకులు దోనెలా పైకి ముడుచుకున్నాయా (తామర పురుగు) లేక కిందికి బోర్లించినట్లు ముడుచుకున్నాయా (నల్లి)?",
                "కాయల మీద నల్లటి మచ్చలు వలయాకార బిందువులతో ఉన్నాయా?",
                "వర్షం తర్వాత కొమ్మలు పైనుంచి కిందికి ఎండిపోతున్నాయా?",
                "ఆకుల అడుగు భాగంలో రసం పీల్చే నల్లటి లేదా పసుపు పురుగులు కనిపిస్తున్నాయా?"
            ],
            "en": [
                "Are leaves curling upward like a boat (thrips) or downward like an inverted cup (mites)?",
                "Are circular sunken spots with black concentric rings visible on ripe fruits?",
                "Did twigs start drying from the tip downwards after recent rains?",
                "Are tiny sucking pests visible under magnifying observation on young foliage?"
            ]
        }
    },
    "Tomato": {
        "crop": "Tomato",
        "crop_te": "టమాట",
        "major_diseases": ["Early Blight", "Fruit Borer", "Leaf Curl"],
        "symptoms": [
            {
                "id": "tom_early_blight",
                "label_en": "Concentric target ring spots",
                "label_te": "లక్ష్యపు పలక (టార్గెట్ బోర్డ్) మచ్చలు",
                "symptom_en": "Brown circular spots with concentric target rings appearing on lower tomato leaves.",
                "symptom_te": "టమాట కింది ఆకులపై గుండ్రటి గోధుమ రంగు వలయాల (టార్గెట్ బోర్డ్) మచ్చలు కనిపిస్తున్నాయి.",
                "disease": "Early Blight"
            },
            {
                "id": "tom_lower_drying",
                "label_en": "Lower leaves drying & falling",
                "label_te": "కింది ఆకులు ఎండి రాలిపోవడం",
                "symptom_en": "Lower leaves turning yellow, developing large brown patches and drying up.",
                "symptom_te": "కింది ఆకులు పసుపుగా మారి ఎండిపోయి పై ఆకులకు వ్యాపిస్తోంది.",
                "disease": "Early Blight"
            },
            {
                "id": "tom_fruit_borer_holes",
                "label_en": "Circular bore holes in fruits",
                "label_te": "కాయలకు గుండ్రటి రంధ్రాలు",
                "symptom_en": "Round holes bored into green and ripe tomato fruits with caterpillar feeding inside.",
                "symptom_te": "టమాట కాయలకు గుండ్రటి రంధ్రాలు పడి లోపల పురుగు కాయ గుజ్జును తింటోంది.",
                "disease": "Fruit Borer"
            },
            {
                "id": "tom_hollow_fruits",
                "label_en": "Hollow rotting fruits & frass",
                "label_te": "బోలు కాయలు & పురుగు విసర్జితాలు",
                "symptom_en": "Bored fruits have larval droppings near the hole and quickly rot.",
                "symptom_te": "రంధ్రం పడిన కాయలలో పురుగు మలం ఉండి కాయలు త్వరగా కుళ్ళిపోతున్నాయి.",
                "disease": "Fruit Borer"
            },
            {
                "id": "tom_wilting",
                "label_en": "Sudden wilting without yellowing",
                "label_te": "ఆకులు పచ్చగా ఉండగానే మొక్క వడలిపోవడం",
                "symptom_en": "Tomato plants suddenly wilting during daytime while still green.",
                "symptom_te": "పగటిపూట ఆకులు పచ్చగా ఉండగానే మొక్కలు ఒక్కసారిగా వడలిపోతున్నాయి.",
                "disease": "Requires further diagnosis"
            },
            {
                "id": "tom_leaf_curling",
                "label_en": "Curling & yellow margins",
                "label_te": "ఆకులు ముడుచుకోవడం & పసుపు అంచులు",
                "symptom_en": "Leaves curling upwards with yellow chlorotic margins and stunted growth.",
                "symptom_te": "టమాట ఆకులు పైకి ముడుచుకుని అంచులు పసుపు రంగులోకి మారుతున్నాయి.",
                "disease": "Leaf Curl Virus"
            }
        ],
        "diagnostic_questions": {
            "te": [
                "ఆకులపై మచ్చల్లో లక్ష్యపు పలక (టార్గెట్ బోర్డు) వంటి వలయాలు స్పష్టంగా కనిపిస్తున్నాయా?",
                "కాయల మీద ఉన్న రంధ్రాల వద్ద పురుగు విసర్జితాలు (మలం) ఉన్నాయా?",
                "మొక్క మొదలు కోసి నీటిలో ఉంచితే తెల్లటి జిగురు ద్రవం (బ్యాక్టీరియా) వస్తోందా?",
                "నష్టం కింది ఆకుల నుంచి పైకి విస్తరిస్తోందా?"
            ],
            "en": [
                "Do leaf spots display distinct concentric rings resembling a target board?",
                "Is larval frass visible near entrance holes on damaged fruits?",
                "Does a cut stem base placed in clear water release milky bacterial streaming?",
                "Is disease progression advancing from lower foliage towards upper canopy?"
            ]
        }
    },
    "Okra": {
        "crop": "Okra",
        "crop_te": "బెండ",
        "major_diseases": ["Yellow Vein Mosaic Virus", "Fruit Borer"],
        "symptoms": [
            {
                "id": "okra_vein_yellowing",
                "label_en": "Bright yellow leaf veins (mosaic)",
                "label_te": "ఆకు ఈనెలు పసుపుగా మారడం (పసుపు ఈనెల తెగులు)",
                "symptom_en": "Veins of okra leaves turn bright yellow while interveinal areas remain green.",
                "symptom_te": "బెండ ఆకులలో ఈనెలు స్పష్టంగా పసుపు రంగులోకి మారి పచ్చటి వల లాగా కనిపిస్తున్నాయి.",
                "disease": "Yellow Vein Mosaic Virus"
            },
            {
                "id": "okra_yellow_fruits",
                "label_en": "Yellowish, fibrous & small pods",
                "label_te": "కాయలు పసుపుగా మారి గట్టిపడటం",
                "symptom_en": "Okra pods turn pale yellowish-white, small, fibrous and unmarketable.",
                "symptom_te": "బెండ కాయలు పసుపు-తెలుపు రంగులోకి మారి నార కట్టి చిన్నవిగా ఉండిపోతున్నాయి.",
                "disease": "Yellow Vein Mosaic Virus"
            },
            {
                "id": "okra_fruit_holes",
                "label_en": "Bore holes in pods & caterpillar",
                "label_te": "కాయలకు రంధ్రాలు & కాయతొలుచు పురుగు",
                "symptom_en": "Caterpillar bores into tender okra pods leaving round entrance holes.",
                "symptom_te": "లేత బెండ కాయలకు రంధ్రాలు పడి లోపలికి పురుగు దూరి కాయలను నాశనం చేస్తోంది.",
                "disease": "Fruit Borer"
            },
            {
                "id": "okra_shoot_wilting",
                "label_en": "Shoot drooping & tip withering",
                "label_te": "కొన చిగుర్లు వడలి ఎండిపోవడం",
                "symptom_en": "Tender shoots and growing tips are drooping and withering due to internal boring.",
                "symptom_te": "లేత కొమ్మలు, చిగుర్లు వడలిపోయి ఎండిపోతున్నాయి (పురుగు కొమ్మ లోపల ఉంది).",
                "disease": "Fruit and Shoot Borer"
            },
            {
                "id": "okra_whitefly_presence",
                "label_en": "Whiteflies under leaves",
                "label_te": "ఆకుల కింద తెల్లదోమ ఉనికి",
                "symptom_en": "Flocks of whiteflies flying when okra plants are disturbed.",
                "symptom_te": "మొక్కలను కదిలిస్తే ఆకుల కింద నుంచి తెల్లటి దోమలు గుంపులుగా ఎగురుతున్నాయి.",
                "disease": "Whitefly (Vector)"
            },
            {
                "id": "okra_flower_drop",
                "label_en": "Flower drop & poor fruiting",
                "label_te": "పూత రాలిపోవడం & పిందెలు నిలవకపోవడం",
                "symptom_en": "Flowers are dropping off before pod formation due to heat or pest stress.",
                "symptom_te": "పూత పిందెగా మారకముందే రాలిపోతోంది, కాయల సంఖ్య బాగా తగ్గింది.",
                "disease": "Requires further diagnosis"
            }
        ],
        "diagnostic_questions": {
            "te": [
                "ఆకు ఈనెలు మాత్రమే పసుపుగా మారాయా లేక ఆకు మొత్తం పసుపుగా మారిందా?",
                "తోటలో తెల్లదోమ ఉనికి ఎక్కువగా గమనించారా?",
                "లేత కొమ్మలు లేదా కాయలకు రంధ్రాలు పడి లోపల నల్లటి విసర్జితాలు ఉన్నాయా?",
                "కాయలు వంకర్లు తిరిగి గట్టిగా మారాయా?"
            ],
            "en": [
                "Are only the veins turning bright yellow with green tissue or is entire leaf chlorotic?",
                "Have you observed dense whitefly populations under the canopy?",
                "Are bore holes and dark frass present on tender shoots or pods?",
                "Are harvested pods deformed, stunted, and unusually fibrous?"
            ]
        }
    },
    "Bengal Gram": {
        "crop": "Bengal Gram",
        "crop_te": "శనగ",
        "major_diseases": ["Fusarium Wilt", "Pod Borer"],
        "symptoms": [
            {
                "id": "bg_wilt_sudden",
                "label_en": "Sudden wilting & root blackening",
                "label_te": "ఆకస్మిక వడలడం & వేర్లు నల్లబడటం",
                "symptom_en": "Plants suddenly wilt and dry in patches; internal root xylem shows black discoloration.",
                "symptom_te": "శనగ మొక్కలు గుంపులుగా ఒక్కసారిగా వాడిపోయి ఎండుతున్నాయి, వేరు లోపల నల్లటి చారలు ఉన్నాయి.",
                "disease": "Fusarium Wilt"
            },
            {
                "id": "bg_pod_holes",
                "label_en": "Pod holes with green caterpillar",
                "label_te": "కాయలకు రంధ్రాలు & పచ్చ పురుగు",
                "symptom_en": "Green caterpillar (Helicoverpa) feeds on seeds thrusting head inside pod.",
                "symptom_te": "పచ్చటి శనగ కాయతొలుచు పురుగు కాయకు రంధ్రం చేసి తల లోపలికి పెట్టి గింజలను తింటోంది.",
                "disease": "Pod Borer"
            },
            {
                "id": "bg_defoliation",
                "label_en": "Leaflets chewed & droppings",
                "label_te": "ఆకులు కొరికి తినడం & మలం",
                "symptom_en": "Young leaves and tender leaflets heavily chewed with green fecal pellets visible.",
                "symptom_te": "లేత ఆకులు కొరికి వేయబడి మొక్కల కింద పచ్చటి పురుగు విసర్జితాలు కనిపిస్తున్నాయి.",
                "disease": "Pod Borer"
            },
            {
                "id": "bg_poor_filling",
                "label_en": "Hollow pods & poor seed filling",
                "label_te": "బోలు కాయలు & గింజ పట్టకపోవడం",
                "symptom_en": "Pods remain empty or have partially eaten shriveled seeds.",
                "symptom_te": "శనగ కాయలు గింజ లేకుండా బోలుగా మారుతున్నాయి.",
                "disease": "Pod Borer / Drought"
            }
        ],
        "diagnostic_questions": {
            "te": [
                "వాడిపోయిన మొక్క వేరును నిలువుగా చీల్చి చూస్తే లోపల నల్లటి లేదా గోధుమ రంగు చారలు ఉన్నాయా?",
                "కాయలకు గుండ్రటి రంధ్రాలు పడి లోపలి గింజలు తినివేయబడ్డాయా?",
                "పొలంలో మొక్కలు ఒకేసారి కాకుండా క్రమంగా ప్యాచ్‌లుగా వాడిపోతున్నాయా?"
            ],
            "en": [
                "Does longitudinal splitting of wilted tap roots reveal black or dark vascular browning?",
                "Are circular holes bored into pods with seeds eaten inside?",
                "Is plant wilting occurring in expanding patches across the field?"
            ]
        }
    },
    "Maize": {
        "crop": "Maize",
        "crop_te": "మొక్కజొన్న",
        "major_diseases": ["Fall Armyworm", "Turcicum Leaf Blight"],
        "symptoms": [
            {
                "id": "mz_whorl_damage",
                "label_en": "Whorl damage & sawdust frass",
                "label_te": "సుడులలో రంధ్రాలు & రంపపు పొట్టు వంటి మలం",
                "symptom_en": "Extensive feeding damage in central whorl with abundant sawdust-like larval frass.",
                "symptom_te": "మొక్కజొన్న సుడిలో రంపపు పొట్టు లాంటి పురుగు మలం ఉండి ఆకులు విపరీతంగా కొరికి ఉన్నాయి.",
                "disease": "Fall Armyworm"
            },
            {
                "id": "mz_window_paning",
                "label_en": "Window pane leaf scraping",
                "label_te": "ఆకులపై అద్దం లాంటి తెల్లటి గీతలు",
                "symptom_en": "Young larvae scraping leaf surface leaving thin papery transparent patches.",
                "symptom_te": "లేత ఆకుల పైపొరను గోకి తినడం వల్ల పలచటి కాగితం లాంటి తెల్లటి మచ్చలు వచ్చాయి.",
                "disease": "Fall Armyworm"
            },
            {
                "id": "mz_turcicum_blight",
                "label_en": "Long boat-shaped brown lesions",
                "label_te": "పడవ ఆకారపు పొడవాటి గోధుమ మచ్చలు",
                "symptom_en": "Long, elliptical, boat-shaped greyish-brown lesions on maize leaves.",
                "symptom_te": "ఆకులపై పొడవాటి పడవ ఆకారపు గోధుమ రంగు ఎండిన మచ్చలు కనిపిస్తున్నాయి.",
                "disease": "Turcicum Leaf Blight"
            },
            {
                "id": "mz_leaf_drying",
                "label_en": "Lower leaves scorching & drying",
                "label_te": "కింది ఆకులు మాడి ఎండిపోవడం",
                "symptom_en": "Severe blight lesions coalescing causing premature drying of whole lower leaves.",
                "symptom_te": "మచ్చలు కలిసిపోయి ఆకులు నిలువుగా ఎండిపోయి మాడిపోతున్నాయి.",
                "disease": "Turcicum Leaf Blight"
            }
        ],
        "diagnostic_questions": {
            "te": [
                "మొక్క సుడి లోపల రంపపు పొట్టు వంటి పురుగు మలం మరియు తల భాగంలో నాలుగు నల్లటి చుక్కలు గల లార్వా ఉందా?",
                "ఆకులపై మచ్చలు పడవ ఆకారంలో పొడవుగా ఉన్నాయా?",
                "నష్టం సుడి దశలోనే ప్రారంభమైందా లేక వెన్ను వచ్చే దశలోనా?"
            ],
            "en": [
                "Is coarse sawdust frass present deep inside the whorl with inverted Y-mark on caterpillar head?",
                "Are leaf blight lesions long, elliptical and boat-shaped?",
                "Did symptoms initiate during vegetative whorl phase or post-tasseling?"
            ]
        }
    },
    "Red Gram": {
        "crop": "Red Gram",
        "crop_te": "కంది",
        "major_diseases": ["Pod Borer", "Fusarium Wilt"],
        "symptoms": [
            {
                "id": "rg_pod_borer",
                "label_en": "Pod holes & webbed flowers",
                "label_te": "కాయలకు రంధ్రాలు & పూత నష్టం",
                "symptom_en": "Caterpillar bores into developing pods and feeds on flowers and buds.",
                "symptom_te": "కంది కాయలకు రంధ్రాలు పడి పురుగు లోపల ఉన్న గింజలను తింటోంది, పూత రాలుతోంది.",
                "disease": "Pod Borer"
            },
            {
                "id": "rg_fusarium_wilt",
                "label_en": "Wilting with black xylem streak",
                "label_te": "మొక్కలు వాడిపోవడం & కాండంపై నల్లటి చార",
                "symptom_en": "Gradual wilting of branches, dark purple band visible under bark of stem.",
                "symptom_te": "కొమ్మలు ఒకదాని తర్వాత ఒకటి వాడిపోయి ఎండుతున్నాయి, కాండం బెరడు కింద నల్లటి చార ఉంది.",
                "disease": "Fusarium Wilt"
            },
            {
                "id": "rg_sterility_mosaic",
                "label_en": "Bushy growth & no flowering",
                "label_te": "గుబురుగా మారడం & పూత రాకపోవడం",
                "symptom_en": "Excessive vegetative growth, leaves become pale green mosaic, plants do not flower.",
                "symptom_te": "మొక్క గుబురుగా పెరిగి ఆకులు లేత ఆకుపచ్చగా మారి ఎంతకీ పూత పిందె రావడం లేదు.",
                "disease": "Sterility Mosaic / Further diagnosis"
            }
        ],
        "diagnostic_questions": {
            "te": [
                "కాండం లేదా వేరు పై బెరడు తీసి చూస్తే లోపల నల్లటి లేదా ఊదా రంగు చార కనిపిస్తోందా?",
                "కాయలకు గుండ్రటి రంధ్రాలు ఉన్నాయా?",
                "మొక్కలు గుబురుగా పెరిగి పూత పూర్తిగా ఆగిపోయిందా?"
            ],
            "en": [
                "Does scraping stem base reveal a dark purple internal vascular band?",
                "Are round bore holes evident on ripening pigeonpea pods?",
                "Has vegetative proliferation occurred with complete suppression of flowering?"
            ]
        }
    }
}


def get_crop_symptoms(crop_name: Optional[str], lang: Optional[str] = None) -> Dict[str, Any]:
    """
    Returns verified crop-specific symptom chips and diagnostic questions.
    Normalizes crop alias and falls back gracefully.
    Supports optional lang ('te' or 'en') for convenient localized question list.
    """
    user_lang = str(lang or 'en').lower().strip()
    if user_lang not in ['te', 'en']:
        user_lang = 'en'

    if not crop_name:
        return {
            "crop": "",
            "crop_te": "",
            "available": False,
            "message_en": "Please select a target crop to display common symptoms.",
            "message_te": "పంటను ఎంచుకుంటే ఆ పంటకు సంబంధించిన లక్షణాలు కనిపిస్తాయి.",
            "symptoms": [],
            "diagnostic_questions": {"en": [], "te": []},
            "diagnostic_questions_list": []
        }

    norm_crop = normalize_crop_name(crop_name)
    data = CROP_SYMPTOM_CATALOG.get(norm_crop)

    if not data:
        # Fallback for crops in dataset without special catalog
        questions = {
            "en": [
                "What part of the plant is showing symptoms (leaves, stems, fruits)?",
                "Are spots circular, irregular, or water-soaked?",
                "Are insects or webbing visible on foliage?"
            ],
            "te": [
                "మొక్కలోని ఏ భాగంపై లక్షణాలు కనిపిస్తున్నాయి (ఆకులు, కాండం, కాయలు)?",
                "మచ్చలు గుండ్రంగా ఉన్నాయా, వెడల్పుగా ఉన్నాయా లేక నీటి మచ్చల్లా ఉన్నాయా?",
                "ఆకులపై పురుగులు లేదా బూజు ఆనవాళ్లు ఉన్నాయా?"
            ]
        }
        return {
            "crop": norm_crop,
            "crop_te": norm_crop,
            "available": False,
            "message_en": f"Generic symptoms available for {norm_crop}. Please describe symptoms in detail.",
            "message_te": f"{norm_crop} పంటకు నిర్దిష్ట లక్షణాలు లోడ్ కాలేదు. దయచేసి లక్షణాలను వివరించండి.",
            "symptoms": [],
            "diagnostic_questions": questions,
            "diagnostic_questions_list": questions.get(user_lang, questions["en"])
        }

    return {
        "crop": data["crop"],
        "crop_te": data["crop_te"],
        "available": True,
        "major_diseases": data.get("major_diseases", []),
        "symptoms": data["symptoms"],
        "diagnostic_questions": data["diagnostic_questions"],
        "diagnostic_questions_list": data["diagnostic_questions"].get(user_lang, data["diagnostic_questions"]["en"])
    }


def get_all_crop_catalogs() -> Dict[str, Any]:
    """Returns the full crop symptom dictionary for client-side instant switching."""
    return CROP_SYMPTOM_CATALOG
