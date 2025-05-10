import pandas as pd
import random
from typing import Tuple, List

def generate_location_phrase(df: pd.DataFrame) -> Tuple[str, List[str], List[str], List[str]]:
    """
    Sinh cụm địa điểm ngôn ngữ tự nhiên và điều kiện SQL tương ứng.

    Trả về:
    - location_natural: ví dụ "phường 5, quận Gò Vấp"
    - cond_cols: ['ward', 'district', 'city']
    - cond_vals: ['5', 'Gò Vấp', 'Hồ Chí Minh']
    - cond_ops: ['=', '=', '=']
    """
    row = df[['city', 'district', 'ward']].dropna().sample(1).iloc[0]
    city, district, ward = row['city'], row['district'], row['ward']

    templates = [
        ("phường {ward}, quận {district}, {city}", ['ward', 'district', 'city'], [ward, district, city]),
        ("phường {ward}, quận {district}", ['ward', 'district'], [ward, district]),
        ("quận {district}, {city}", ['district', 'city'], [district, city]),
        ("quận {district}", ['district'], [district]),
        ("{city}", ['city'], [city]),
    ]

    template, cond_cols, cond_vals = random.choice(templates)
    location_natural = template.format(ward=ward, district=district, city=city)

    cond_ops = ['='] * len(cond_cols)

    return location_natural, cond_cols, cond_vals, cond_ops