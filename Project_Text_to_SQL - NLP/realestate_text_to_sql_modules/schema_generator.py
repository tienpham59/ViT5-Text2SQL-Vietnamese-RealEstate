import pandas as pd
from typing import List

class SchemaGenerator:
    @staticmethod
    def generate_schema(df: pd.DataFrame, relevant_columns: List[str] = None) -> List[str]:
        """
        Generate schema from DataFrame in the format: ["column_name[type]", ...].

        Column types are mapped from actual dtypes to simplified types:
        - int32, int64   => int
        - float32, float64 => float
        - object, string => str
        """
        if relevant_columns is not None:
            df = df[relevant_columns]

        type_mapping = {
            'int64': 'int',
            'int32': 'int',
            'float64': 'float',
            'float32': 'float',
            'object': 'str',
            'string': 'str'
        }

        schema = []
        for col, dtype in df.dtypes.items():
            dtype_str = str(dtype)
            col_type = type_mapping.get(dtype_str, 'str')  # default to str if unknown
            schema.append(f"{col}[{col_type}]")

        return schema
