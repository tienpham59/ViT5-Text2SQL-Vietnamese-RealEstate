"""
File: run_pipeline.py

Purpose:
    This script runs the full pipeline to generate exactly N valid Text-to-SQL training samples.
    A valid sample must generate a SQL query that returns non-empty results on the SQLite database.

Steps:
    1. Clean the raw housing dataset and export:
        - Cleaned CSV file
        - SQLite database file

    2. Randomly sample rows from the cleaned data, and iteratively generate N valid question-SQL pairs.

    3. Split the validated samples into train / validation / test sets.
       Save them as JSON files for training downstream models.
"""

import pandas as pd
import json
import os
from sklearn.model_selection import train_test_split
from realestate_text_to_sql_modules.data_preprocessing import clean_dataframe
from realestate_text_to_sql_modules.realestate_text_to_sql import RealEstateTextToSQL
from realestate_text_to_sql_modules.sql_utils import is_valid_sql

# Configuration
NUM_SAMPLES = 15
RAW_PATH = "data/raw/vietnam_housing_dataset_cleaned.csv"
DB_PATH = "data/processing/SQLite_real_estate.db"

# Step 1: Clean the raw CSV
df_raw = pd.read_csv(RAW_PATH)
df_cleaned = clean_dataframe(
    df_raw,
    save_path="data/processing/df_cleaned.csv",
    sqlite_path=DB_PATH
)
print(f"Cleaned dataset has {len(df_cleaned)} rows")

# Step 2: Iteratively generate valid samples
pipeline = RealEstateTextToSQL(df_cleaned)
validated_samples = []
attempt = 0
max_attempts = NUM_SAMPLES * 10

while len(validated_samples) < NUM_SAMPLES and attempt < max_attempts:
    attempt += 1
    try:
        question, query, extras = pipeline.generator.generate_query(df_cleaned)
        print(f"[TRY {attempt}] Question: {question}")
        print(f"[TRY {attempt}] SQL: {query}")
        if is_valid_sql(query, db_path=DB_PATH):
            validated_samples.append({
                "Question": question,
                "SQL": query,
                **extras
            })
    except Exception as e:
        print(f"[SKIP] Error at attempt {attempt}: {e}")
        continue

print(f"Generated {len(validated_samples)} valid samples after {attempt} attempts")

# Step 3: Split into train / val / test
if len(validated_samples) == 0:
    print("[ERROR] No valid samples were generated. Consider debugging generate_query() or relaxing conditions.")
    exit(1)
    
train, temp = train_test_split(validated_samples, test_size=0.15, random_state=42)
val, test = train_test_split(temp, test_size=1/3, random_state=42)

print(f"Train set: {len(train)} samples")
print(f"Validation set: {len(val)} samples")
print(f"Test set: {len(test)} samples")

# Save to files
os.makedirs("data/processing", exist_ok=True)

with open("data/processing/train_text2sql.json", "w", encoding="utf-8") as f:
    json.dump(train, f, ensure_ascii=False, indent=2)
with open("data/processing/val_text2sql.json", "w", encoding="utf-8") as f:
    json.dump(val, f, ensure_ascii=False, indent=2)
with open("data/processing/test_text2sql.json", "w", encoding="utf-8") as f:
    json.dump(test, f, ensure_ascii=False, indent=2)

print("Saved output files to data/processing")