# Text-to-SQL Dataset Generation Pipeline

This project provides a full pipeline to automatically generate Vietnamese Text-to-SQL training data for real estate domain.

---

## Features

- Clean and normalize a raw CSV housing dataset
- Export both CSV and SQLite formats for training & query execution
- Generate natural language questions and SQL queries across various logic types:
  - Range query
  - Comparison query
  - Count query
  - Location + Price query
  - Extreme (Top-K)
- Validate SQL by executing against real SQLite DB (only keep samples with non-empty results)
- Automatically infer minimal schema (column[type]) from query content
- Split final dataset into train/val/test sets

---

## Folder Structure

```
Project_Text_to_SQL - NLP/
├── data/
│   ├── raw/                        # Raw CSV files
│   └── processing/                # Cleaned CSV, SQLite DB, generated samples
├── realestate_text_to_sql_modules/
│   ├── data_preprocessing.py     # Clean + normalize input data
│   ├── schema_generator.py       # Generate minimal schema per query
│   ├── sql_utils.py              # Run SQL to validate query
│   ├── templates.py              # Natural language templates
│   ├── natural_query_generator.py # Logic to generate question + query pairs
│   ├── realestate_text_to_sql.py # Main controller class
│   └── sql_type_manager.py       # Manages query type distribution
├── run_pipeline.py               # Main execution script
└── README.md                     # Project overview (this file)
```

---

## How to Run

### 1. Place raw data:
Put your input file at:
```
data/raw/vietnam_housing_dataset_cleaned.csv
```

### 2. Run full pipeline:
```bash
python run_pipeline.py
```
This will:
- Clean the raw CSV
- Generate valid training samples
- Split and save to:
  - `data/processing/train_text2sql.json`
  - `data/processing/val_text2sql.json`
  - `data/processing/test_text2sql.json`

---

## Configuration
Edit the following in `run_pipeline.py` if needed:
```python
NUM_SAMPLES = 2000
RAW_PATH = "data/raw/vietnam_housing_dataset_cleaned.csv"
DB_PATH = "data/processing/SQLite_real_estate.db"
```

---

## Output Format
Each sample has 3 fields:
```json
{
  "Question": "Bạn thống kê giúp mình số căn giá trên 5600000000 nha!",
  "SQL": "SELECT COUNT(*) FROM price_house WHERE price > 5600000000",
  "Schema": "address[str], area[float], price[float], ..."
}
```

---

## Notes
- SQL queries are only kept if they return at least one row on the actual database.
- The schema is minimal — only columns used in the SQL query are listed.
- The whole system is designed to ensure high-quality, executable training samples.

---

## 📫 Contact
For support or questions, contact [your team name or author here].

