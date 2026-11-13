# Data Directory

This folder is reserved for reference datasets, training data, and agricultural knowledge corpora for Rythu Mithra.

## Recommended Structure
```
data/
├── datasets/
│   ├── plant_village/       # Raw or processed crop disease images
│   └── multilingual_qa/     # Multilingual agricultural Q&A pairs (Telugu, Hindi, English)
├── sample_queries.json      # Standard evaluation and sample queries
└── README.md
```

## Important Safety Note
- The application will **never** overwrite or delete any datasets, notebooks, or training scripts you place in this directory.
- For large image datasets (> 100MB), consider keeping them in your external storage or keeping a local symlink.
