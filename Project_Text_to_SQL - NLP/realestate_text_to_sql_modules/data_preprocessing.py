"""
File: data_preprocessing.py

Purpose:
    Preprocess and normalize raw real estate tabular data before training a Text-to-SQL model.

Main Function:
    - clean_dataframe(df, save_path=None, sqlite_path=None):
        + Normalize column names to snake_case.
        + Transform values: price units, label mapping, type casting.
        + Optionally export the cleaned data to CSV and/or SQLite.

Usage:
    from realestate_text_to_sql_modules.data_preprocessing import clean_dataframe

    df_raw = pd.read_csv("data/raw/vietnam_housing_dataset_cleaned.csv")
    df_cleaned = clean_dataframe(
        df_raw,
        save_path="data/processing/df_cleaned.csv",
        sqlite_path="data/processing/SQLite_real_estate.db"
    )

Args:
    df (pd.DataFrame): Raw housing dataset.
    save_path (str, optional): Output path to save cleaned CSV.
    sqlite_path (str, optional): Output path to save SQLite database.

Returns:
    pd.DataFrame: Cleaned and normalized DataFrame.
"""

import pandas as pd
import sqlite3

def clean_dataframe(df, save_path=None, sqlite_path=None):
    """
    Clean and normalize a real estate DataFrame.

    - Maps raw labels to readable Vietnamese strings.
    - Converts price from billions to absolute values.
    - Converts types of numeric columns.
    - Normalizes column names to snake_case.

    Args:
        df (pd.DataFrame): The raw DataFrame.
        save_path (str, optional): Path to export cleaned CSV file.
        sqlite_path (str, optional): Path to export SQLite database.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    df['Legal status'] = df['Legal status'].replace({
        'Have certificate': 'Đã có sổ',
        'Sale contract': 'Hợp đồng mua bán',
        'Unk': 'Không rõ pháp lý'
    })

    df['Furniture state'] = df['Furniture state'].replace({
        'Basic': 'Nội thất cơ bản',
        'Full': 'Nội thất đầy đủ',
        'Unk': 'Không rõ nội thất'
    })

    df['Price'] = (df['Price'] * 1_000_000_000).round()

    df.drop(columns=['House_Level','is_project','Cluster_Label','Access Road'], inplace=True)

    df[['Floors', 'Bedrooms', 'Bathrooms']] = df[['Floors', 'Bedrooms', 'Bathrooms']].astype('int')

    df.columns = [col.lower().strip().replace(" ", "_") for col in df.columns]

    df['ward'] = df['ward'].replace('5', 'Phường 5')
    df['district'] = df['district'].replace('5', 'Quận 5')
    
    if sqlite_path:
        conn = sqlite3.connect(sqlite_path)
        df.to_sql('price_house', conn, if_exists='replace', index=False)
        conn.close()

    if save_path:
        df.to_csv(save_path, index=False, encoding='utf-8-sig')

    return df
