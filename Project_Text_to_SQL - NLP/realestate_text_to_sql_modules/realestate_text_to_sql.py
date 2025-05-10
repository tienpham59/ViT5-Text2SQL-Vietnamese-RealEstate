import json
import pandas as pd
from typing import List, Dict

from realestate_text_to_sql_modules.schema_generator import SchemaGenerator
from realestate_text_to_sql_modules.sql_type_manager import SQLTypeManager
from realestate_text_to_sql_modules.natural_query_generator import NaturalQueryGenerator

class RealEstateTextToSQL:
    def __init__(self, df: pd.DataFrame):
        """Khởi tạo class RealEstateTextToSQL với DataFrame đầu vào."""
        self.df = df
        self.full_schema = SchemaGenerator.generate_schema(df)
        self.generator = NaturalQueryGenerator()

    def generate_samples(self, n: int) -> pd.DataFrame:
        """
        Sinh ra nhiều cặp câu hỏi - SQL - schema (n mẫu) để huấn luyện model text-to-SQL.

        Trả về:
            pd.DataFrame gồm 3 cột: Question, Schema, SQL
        """
        samples = []
        attempt = 0
        skipped = 0
        max_attempts = n * 5  # tránh vòng lặp vô hạn

        while len(samples) < n and attempt < max_attempts:
            attempt += 1
            question_type = SQLTypeManager.sample_question_type()

            try:
                question, query, extras = NaturalQueryGenerator.generate_query(self.df, question_type)
                samples.append({
                    "Question": question,
                    "Schema": ", ".join(self.full_schema),
                    "SQL": query
                })
            except Exception as e:
                skipped += 1
                print(f"[SKIP] {e}")
                continue

        print(f"[DONE] Đã sinh {len(samples)} mẫu hợp lệ trên {attempt} lượt thử.")
        print(f"[INFO] Bỏ qua {skipped} mẫu không hợp lệ.")
        return pd.DataFrame(samples)
