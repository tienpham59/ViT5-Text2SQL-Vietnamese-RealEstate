"""
Module: natural_query_generator.py

Purpose:
    Generate natural language questions and corresponding SQL queries for Vietnamese real estate data.
    This module supports diverse question types (e.g., range, comparison, count, location-based) and returns clean training triples for Text-to-SQL models.

Key Function:
    - NaturalQueryGenerator.generate_query(df, question_type=None):
        Returns a tuple (question: str, sql: str, extras: dict) where `extras` includes:
        - Schema: string schema with column names and types (e.g., "price[float], area[float], ...")

Supported Question Types:
    - specific_query
    - location_price_query
    - range_query
    - comparison_query
    - count_query
    - like_query
    - or_query
    - top_k_query
    - extreme_min / extreme_max
    - between_location_query
    - fallback (default simple query)

Example Output:
    Question: "Bạn thống kê giúp mình số căn giá trên 5 tỷ nha!"
    Schema: "price[float], area[float], ..."
    SQL: "SELECT COUNT(*) FROM price_house WHERE price > 5000000000"

Note:
    Output is standardized to a 3-column format for training: Question | Schema | SQL
"""

import random
from typing import List, Tuple
import pandas as pd

from realestate_text_to_sql_modules.utils import (
    format_number,
    format_price_for_display,
    reverse_price_string_to_number,
    sanitize_question
)
from realestate_text_to_sql_modules.sql_type_manager import SQLTypeManager
from realestate_text_to_sql_modules.templates import (
    TEMPLATES_LOCATION_PRICE,
    TEMPLATES_COMPARISON_OP,
    TEMPLATES_COMPARISON_EQUAL,
    TEMPLATES_PRICE_COMPARISON,
    TEMPLATES_RANGE,
    TEMPLATES_SPECIFIC,
    TEMPLATES_LIKE,
    TEMPLATES_EXTREME_MAX,
    TEMPLATES_EXTREME_MIN,
    TEMPLATES_OR,
    TEMPLATES_LOCATION_PRICE_AREA
)
from realestate_text_to_sql_modules.constants import COLUMN_TRANSLATIONS, COMPARISON_TERMS, SCHEMA_DEFINITION
from realestate_text_to_sql_modules.schema_generator import SchemaGenerator

def generate_location_price_question(price_condition: str, location_natural: str, value: float) -> str:
    """Sinh câu hỏi về vị trí và giá bất động sản"""

    # Làm sạch điều kiện giá nếu nó đã là 1 câu hỏi
    is_full_question = any(kw in price_condition.lower() for kw in ["có", "không", "?"])
    price_text = format_price_for_display(value)

    template = random.choice(TEMPLATES_LOCATION_PRICE)

    if is_full_question:
        # Nếu price_condition đã là 1 câu hỏi rồi, wrap lại
        question = f"{location_natural} có nhà nào {price_condition.strip('?').lower()} không?"
    else:
        # Nếu chưa phải câu đầy đủ, dùng template chuẩn
        question = template.format(
            price_condition=price_condition,
            location=location_natural,
            price_text=price_text
        )

    # Làm sạch lỗi lặp từ
    question = question.replace("??", "?").replace("không? không?", "không?")
    question = question.strip()

    return question

def format_sql_value(val: float) -> str:
    if isinstance(val, float) and val.is_integer():
        return str(int(val))
    return str(val)

def cleanup_question(text: str) -> str:
    """Làm sạch câu hỏi sau khi format"""
    text = text.replace("tỷtỷ", "tỷ")
    text = text.replace("tỷKhu", "tỷ. Khu")
    text = text.replace("tỷphường", "tỷ. Phường")
    text = text.replace("tỷquận", "tỷ. Quận")
    text = text.replace("  ", " ")
    return text.strip()

def generate_comparison_question(translated_col: str, comparison_term: str, value_str: str, unit: str) -> str:
    if translated_col == "giá":
        template = random.choice(TEMPLATES_PRICE_COMPARISON)
    elif comparison_term in ["bằng", "đúng", "khoảng", "tầm"]:
        template = random.choice(TEMPLATES_COMPARISON_EQUAL)
    else:
        template = random.choice(TEMPLATES_COMPARISON_OP)

    question = template.format(
        col_name=translated_col,
        comparison_term=comparison_term,
        value_str=value_str,
        unit=unit
    )

    # Loại từ không phù hợp nếu không đúng cột
    blacklist = {
        "hướng": "hướng",
        "nội thất": "nội thất",
        "pháp lý": "pháp lý"
    }

    for word, required_col in blacklist.items():
        if translated_col != required_col and word in question:
            question = question.replace(word, translated_col)

    return question



def generate_range_question(translated_col: str, value1: str, value2: str, unit: str) -> str:
    return random.choice(TEMPLATES_RANGE).format(
        col_name=translated_col,
        value1=value1,
        value2=value2,
        unit=unit
    )

def generate_specific_question(translated_cols: List[str]) -> str:
    col_display = ", ".join(translated_cols)
    return random.choice(TEMPLATES_SPECIFIC).format(column_list=col_display)

def generate_count_question(col: str, value: float, unit: str, op: str = "=") -> str:
    translated_col = COLUMN_TRANSLATIONS.get(col, col).replace("số ", "")
    if col == "price":
        value_str = format_price_for_display(value)
        unit_display = ""
    else:
        value_str = format_number(value)
        unit_display = unit

    if op == "=":
        condition = f"{translated_col} là {value_str}{unit_display}"
    elif op == ">":
        condition = f"trên {value_str}{unit_display} {translated_col}"
    elif op == "<":
        condition = f"dưới {value_str}{unit_display} {translated_col}"
    elif op == ">=":
        condition = f"từ {value_str}{unit_display} trở lên {translated_col}"
    elif op == "<=":
        condition = f"tối đa {value_str}{unit_display} {translated_col}"
    else:
        condition = f"{translated_col} {op} {value_str}{unit_display}"

    options = [
        f"Có bao nhiêu nhà có {condition}?",
        f"Số lượng bất động sản {condition} là bao nhiêu?",
        f"Ủa, nhiều nhà {condition} không ta?",
        f"Tôi muốn biết có nhiều căn {condition} không?",
        f"Bạn thống kê giúp mình số căn {condition} nha!"
    ]
    return random.choice(options)


def generate_like_question(kw: str) -> str:
    return random.choice(TEMPLATES_LIKE).format(kw=kw)

def generate_extreme_question(col: str, mode: str = "max") -> str:
    translated_col = COLUMN_TRANSLATIONS.get(col, col)
    templates = TEMPLATES_EXTREME_MAX if mode == "max" else TEMPLATES_EXTREME_MIN
    return random.choice(templates).format(col_name=translated_col)

def get_unit_for_column(col: str) -> str:
    if col == "price":
        return "tỷ"
    elif col == "area":
        return "m2"
    elif col in ["frontage", "access_road"]:
        return "m"
    else:
        return ""


def extract_relevant_columns(question: str) -> List[str]:
    mapping = {
        "diện tích": "area",
        "giá": "price",
        "phòng ngủ": "bedrooms",
        "phòng tắm": "bathrooms",
        "tầng": "floors",
        "đường vào": "access_road",
        "mặt tiền": "frontage",
        "địa chỉ": "address",
        "quận": "district",
        "thành phố": "city",
        "phường": "ward"
    }
    relevant = []
    lower_question = question.lower()
    for keyword, col in mapping.items():
        if keyword in lower_question and col not in relevant:
            relevant.append(col)
    if not relevant:
        relevant = ["price", "area", "bedrooms", "floors", "bathrooms"]
    return relevant

def get_natural_comparison_phrase(col_type: str, comparison: str) -> str:
    terms = COMPARISON_TERMS.get(col_type, {})
    options = terms.get(comparison, [comparison])
    return random.choice(options)

def generate_or_question(col1: str, val1: float, unit1: str, col2: str, val2: float, unit2: str, op: str) -> str:
    translated_col1 = COLUMN_TRANSLATIONS.get(col1, col1)
    translated_col2 = COLUMN_TRANSLATIONS.get(col2, col2)

    # Ưu tiên để phòng ngủ, phòng tắm, số tầng lên trước
    priority_cols = ['bedrooms', 'bathrooms', 'floors']
    if col2 in priority_cols and col1 not in priority_cols:
        # Hoán đổi toàn bộ
        col1, col2 = col2, col1
        val1, val2 = val2, val1
        unit1, unit2 = unit2, unit1
        translated_col1, translated_col2 = translated_col2, translated_col1

    def op_to_phrase(op, val, col):
        if col == "price":
            val_str = format_price_for_display(val)
        else:
            val_str = format_number(val)

        if op == "=":
            return f"là {val_str}"
        elif op == ">":
            return f"hơn {val_str}"
        elif op == "<":
            return f"dưới {val_str}"
        elif op == ">=":
            return f"từ {val_str} trở lên"
        elif op == "<=":
            return f"tối đa {val_str}"
        return f"{op} {val_str}"

    phrase1 = op_to_phrase(op, val1, col1)
    phrase2 = op_to_phrase(op, val2, col2)

    unit1_disp = "" if col1 == "price" else f" {unit1}" if unit1 else ""
    unit2_disp = "" if col2 == "price" else f" {unit2}" if unit2 else ""

    return random.choice(TEMPLATES_OR).format(
        col1=translated_col1, phrase1=phrase1, unit1=unit1_disp,
        col2=translated_col2, phrase2=phrase2, unit2=unit2_disp
    )

def is_value_type_valid(col: str, value) -> bool:
    """Kiểm tra xem giá trị có phù hợp kiểu dữ liệu mong đợi cho cột đó không"""
    if col in ['house_direction', 'legal_status', 'furniture_state']:
        return isinstance(value, str) or isinstance(value, int) or isinstance(value, float)

    if col in ['price', 'area', 'frontage', 'access_road', 'bedrooms', 'bathrooms', 'floors']:
        return isinstance(value, (int, float)) or (isinstance(value, str) and value.replace('.', '', 1).isdigit())
    return True

def fix_col_for_text_column(col: str, value, op: str):
    if col in ['house_direction', 'legal_status', 'furniture_state']:
        return str(value), '='
    return value, op

class NaturalQueryGenerator:
    @staticmethod
    def generate_price_range_around(value: float) -> Tuple[float, float]:
        """Trả về khoảng giá ± phù hợp với tầm giá gốc"""
        if value < 2_000_000_000:
            delta = 200_000_000
        elif value < 5_000_000_000:
            delta = 500_000_000
        else:
            delta = 1_000_000_000
        return value - delta, value + delta

    @staticmethod
    def generate_natural_condition(col: str, value: float, comparison: str) -> Tuple[str, str, str, List[str], List[str], List[float], str]:
        translated_col = COLUMN_TRANSLATIONS.get(col, col)

        # --- Đặc biệt cho các cột dạng text ---
        if col in ['house_direction', 'legal_status', 'furniture_state']:
            value_str = str(value)
            unit = ''
            if col == 'house_direction':
                # Chỉ sinh template hỏi về hướng, ví dụ: "Nhà quay hướng Đông"
                question = f"Nhà nào quay hướng {value_str}?"
            elif col == 'furniture_state':
                # Ví dụ: "Nhà nào có nội thất cơ bản"
                question = f"Nhà nào có {value_str.lower()}?"
            elif col == 'legal_status':
                # Ví dụ: "Có nhà nào pháp lý là Sổ hồng riêng không?"
                question = f"Có nhà nào pháp lý là {value_str} không?"

            sql = f"{col} = '{value_str}'"
            return question.strip(), sql, col, [col], ['='], [value_str], col

        # --- Còn lại là dạng số ---
        if col == 'price':
            term_type = 'price'
            unit = ""
        elif col in ['bedrooms', 'bathrooms', 'floors']:
            term_type = 'quantity'
            unit = ""
            value = int(value)
        else:
            term_type = 'quantity'
            unit = "m2" if col == 'area' else "m" if col in ['frontage', 'access_road'] else ""

        # Chuyển đổi value
        if col == 'price':
            value_str = format_price_for_display(value)
            value_sql = reverse_price_string_to_number(value_str)
        else:
            value_str = format_number(value)
            value_sql = float(value_str.replace(",", "."))

        # Nếu dạng khoảng
        if comparison == 'BETWEEN':
            if col == 'price':
                val1, val2 = NaturalQueryGenerator.generate_price_range_around(value)
                val1_str = format_price_for_display(val1)
                val2_str = format_price_for_display(val2)
            else:
                val1 = value
                val2 = value + 1
                if col in ['bedrooms', 'bathrooms', 'floors']:
                    val1, val2 = int(val1), int(val2)
                val1_str = format_number(val1)
                val2_str = format_number(val2)

            val1_sql = float(val1)
            val2_sql = float(val2)

            natural = generate_range_question(translated_col, val1_str, val2_str, unit)
            return natural.strip(), f"{col} >= {format_sql_value(val1_sql)} AND {col} <= {format_sql_value(val2_sql)}", translated_col, [col, col], [">=", "<="], [val1_sql, val2_sql], col

        # Nếu là các dạng so sánh còn lại
        comparison_term = get_natural_comparison_phrase(term_type, comparison)
        natural = generate_comparison_question(translated_col, comparison_term, value_str, unit)

        return natural.strip(), f"{col} {comparison} {format_sql_value(value_sql)}", translated_col, [col], [comparison], [value_sql], col


        # Các phép so sánh khác
        comparison_term = get_natural_comparison_phrase(term_type, comparison)
        natural = generate_comparison_question(translated_col, comparison_term, value_str, unit)

        return natural.strip(), f"{col} {comparison} {format_sql_value(value_sql)}", translated_col, [col], [comparison], [value_sql], col
    
    @staticmethod
    def generate_query(df: pd.DataFrame, question_type: str = None) -> Tuple[str, str, dict]:
        if not question_type:
            question_type = SQLTypeManager.sample_question_type()

        def build_output(question: str, query: str) -> Tuple[str, str, dict]:
            used_cols = [c for c in df.columns if c in query]
            schema_str = ", ".join(SchemaGenerator.generate_schema(df, relevant_columns=used_cols))
            return question, query, {"Schema": schema_str}

        all_possible_cols = [
            'price', 'area', 'frontage', 'access_road',
            'floors', 'bedrooms', 'bathrooms',
            'house_direction', 'legal_status', 'furniture_state'
        ]

        col = random.choice([
            c for c in all_possible_cols
            if c in df.columns and df[c].dropna().shape[0] >= 10
        ])

        valid_values = df[col][df[col].notna()]
        valid_values = valid_values[valid_values.apply(lambda v: is_value_type_valid(col, v))]

        # Bỏ giá trị 'Unk' nếu cột dạng text
        if col in ['house_direction', 'legal_status', 'furniture_state']:
            valid_values = valid_values[~valid_values.astype(str).str.lower().isin(['unk', 'unknown'])]

        if col not in ['house_direction', 'legal_status', 'furniture_state']:
            valid_values = valid_values[valid_values > 0]
        if valid_values.empty:
            raise ValueError(f"Không có giá trị hợp lệ cho cột {col}")
        value = random.choice(valid_values.values)
        if col in ['floors', 'bedrooms', 'bathrooms']:
            value = int(value)
        op = random.choice(['>', '<', '='])
        unit = get_unit_for_column(col)

        if question_type == 'specific_query':
            cols_specific = ['price', 'district', 'area']
            translated_cols = [COLUMN_TRANSLATIONS[c] for c in cols_specific]
            question = generate_specific_question(translated_cols)
            query = f"SELECT {', '.join(cols_specific)} FROM price_house"
            return build_output(question, query)

        if question_type == 'location_price_query':
            from realestate_text_to_sql_modules.location_utils import generate_location_phrase
            location_natural, loc_cols, loc_vals, loc_ops = generate_location_phrase(df)

            op_price = random.choice(['<', '=', 'BETWEEN'])

            if op_price == 'BETWEEN':
                valid_prices = df['price'][df['price'] > 0].dropna().sort_values().values
                if len(valid_prices) < 2:
                    return None
                idx = random.randint(0, len(valid_prices) - 2)
                low = round(valid_prices[idx] / 100_000_000) * 100_000_000
                high = round(valid_prices[idx + 1] / 100_000_000) * 100_000_000
                if low >= high:
                    high = low + 100_000_000

                price_display_1 = format_price_for_display(low)
                price_display_2 = format_price_for_display(high)
                natural_cond = f"giá từ {price_display_1} đến {price_display_2}"
                sql_cond = f"price >= {low} AND price <= {high}"
            else:
                value = df['price'][df['price'] > 0].dropna().sample(1).values[0]
                price_display = format_price_for_display(value)
                price_value = reverse_price_string_to_number(price_display)
                natural_cond = f"giá {get_natural_comparison_phrase('price', op_price)} {price_display}"
                sql_cond = f"price {op_price} {format_sql_value(price_value)}"


            location_sql = " AND ".join(f"{col} {op} '{val}'" for col, op, val in zip(loc_cols, loc_ops, loc_vals))
            question = f"Có nhà nào ở {location_natural} có {natural_cond} không?"
            question = sanitize_question(question)
            query = f"SELECT * FROM price_house WHERE {sql_cond} AND {location_sql}"
            used_cols = ["price"] + loc_cols
            schema_str = ", ".join(SchemaGenerator.generate_schema(df, relevant_columns=used_cols))
            return question, query, {"Schema": schema_str}

        if question_type == 'range_query':
            valid_prices = df['price'][df['price'] > 0].dropna().sort_values().values
            if len(valid_prices) < 2:
                return None
            idx = random.randint(0, len(valid_prices) - 2)
            low = round(valid_prices[idx] / 100_000_000) * 100_000_000
            high = round(valid_prices[idx + 1] / 100_000_000) * 100_000_000
            if low >= high:
                high = low + 100_000_000
            price_display_1 = format_price_for_display(low)
            price_display_2 = format_price_for_display(high)
            question = f"Tìm nhà có giá từ {price_display_1} đến {price_display_2}?"
            question = sanitize_question(question)
            sql = f"SELECT * FROM price_house WHERE price >= {low} AND price <= {high}"
            return build_output(question, sql)

        if question_type == 'comparison_query':
            value_fixed, op_fixed = fix_col_for_text_column(col, value, op)
            natural_cond, sql_cond, *_ = NaturalQueryGenerator.generate_natural_condition(col, value_fixed, op_fixed)
            return build_output(natural_cond, f"SELECT * FROM price_house WHERE {sql_cond}")

        if question_type == 'count_query':
            value_fixed, op_fixed = fix_col_for_text_column(col, value, op)
            natural_cond, sql_cond, *_ = NaturalQueryGenerator.generate_natural_condition(col, value_fixed, op_fixed)
            question = generate_count_question(col=col, value=value_fixed, unit=unit, op=op_fixed)
            return build_output(question, f"SELECT COUNT(*) FROM price_house WHERE {sql_cond}")
        
        if question_type == 'like_query':
            city_value = df['city'].dropna().sample(1).values[0]
            keyword = city_value[:3]
            question = generate_like_question(keyword)
            return build_output(question, f"SELECT * FROM price_house WHERE city LIKE '%{keyword}%'")

        if question_type == 'or_query':
            col1, col2 = random.sample(['price', 'area', 'frontage', 'access_road', 'floors', 'bedrooms', 'bathrooms'], 2)
            valid1 = df[col1][df[col1].notna()]
            valid2 = df[col2][df[col2].notna()]
            val1 = int(valid1.sample(1).values[0]) if col1 in ['floors', 'bedrooms', 'bathrooms'] else round(valid1.sample(1).values[0], 1)
            val2 = int(valid2[valid2 > val1].sample(1).values[0]) if col2 in ['floors', 'bedrooms', 'bathrooms'] else round(valid2[valid2 > val1].sample(1).values[0], 1)
            op = random.choice(["=", ">", "<"])
            conds_sql = f"{col1} {op} {format_sql_value(val1)} OR {col2} {op} {format_sql_value(val2)}"
            question = generate_or_question(col1, val1, get_unit_for_column(col1), col2, val2, get_unit_for_column(col2), op)
            return build_output(question, f"SELECT * FROM price_house WHERE {conds_sql}")

        if question_type == 'extreme_max':
            col = random.choice(['price', 'area', 'frontage', 'access_road'])
            question = generate_extreme_question(col, mode="max")
            return build_output(question, f"SELECT * FROM price_house ORDER BY {col} DESC LIMIT 1")

        if question_type == 'extreme_min':
            col = random.choice(['price', 'area', 'frontage', 'access_road'])
            question = generate_extreme_question(col, mode="min")
            return build_output(question, f"SELECT * FROM price_house ORDER BY {col} ASC LIMIT 1")

        if question_type == 'top_k_query':
            col = random.choice(['price', 'area', 'frontage', 'access_road'])
            k = random.choice([3, 5, 10])
            question = generate_top_k_question(COLUMN_TRANSLATIONS.get(col, col), k)
            return build_output(question, f"SELECT * FROM price_house ORDER BY {col} DESC LIMIT {k}")

        if question_type == 'between_location_query':
            col = random.choice(['price', 'area', 'frontage', 'access_road'])
            valid = df[col][df[col].notna()].dropna().sort_values().values
            if len(valid) < 2:
                return None
            idx = random.randint(0, len(valid) - 2)
            val1_raw, val2_raw = valid[idx], valid[idx + 1]
            val1 = round(val1_raw / 100_000_000) * 100_000_000 if col == 'price' else round(val1_raw, 1)
            val2 = round(val2_raw / 100_000_000) * 100_000_000 if col == 'price' else round(val2_raw, 1)
            if val1 >= val2:
                val2 = val1 + (100_000_000 if col == 'price' else 1)
            unit = get_unit_for_column(col)
            from realestate_text_to_sql_modules.location_utils import generate_location_phrase
            location_natural, location_cols, location_vals, location_ops = generate_location_phrase(df)
            question = generate_between_location_question(
                COLUMN_TRANSLATIONS.get(col, col),
                format_number(val1), format_number(val2),
                unit, location_natural
            )
            question = cleanup_question(question)
            location_sql = " AND ".join(
                f"{col} {op} '{val}'" for col, op, val in zip(location_cols, location_ops, location_vals)
            )
            query = f"SELECT * FROM price_house WHERE {col} >= {format_sql_value(val1)} AND {col} <= {format_sql_value(val2)} AND {location_sql}"
            return build_output(question, query)

        if question_type == 'location_price_area_query':
            from realestate_text_to_sql_modules.location_utils import generate_location_phrase
            location_natural, location_cols, location_vals, location_ops = generate_location_phrase(df)
            location_sql = " AND ".join(
                f"{col} {op} '{val}'" for col, op, val in zip(location_cols, location_ops, location_vals)
            )
            price_val = df['price'][df['price'] > 0].dropna().sample(1).values[0]
            price_op = random.choice(['<', '>', '='])
            price_phrase = random.choice(COMPARISON_TERMS['price'][price_op])
            price_text = f"{price_phrase} {format_price_for_display(price_val)}"
            price_sql = f"price {price_op} {int(price_val)}"
            area_val = df['area'][df['area'] > 0].dropna().sample(1).values[0]
            area_op = random.choice(['<', '>', '='])
            area_phrase = random.choice(COMPARISON_TERMS['quantity'][area_op])
            area_text = f"{area_phrase} {format_number(area_val)}m2"
            area_sql = f"area {area_op} {int(area_val)}"
            template = random.choice(TEMPLATES_LOCATION_PRICE_AREA)
            question = template.format(
                location=location_natural,
                price_condition=price_text,
                area_condition=area_text
            )
            question = sanitize_question(question)
            sql = f"SELECT * FROM price_house WHERE {price_sql} AND {area_sql} AND {location_sql}"
            used_cols = ["price", "area"] + location_cols
            schema_str = ", ".join(SchemaGenerator.generate_schema(df, relevant_columns=used_cols))
            return question, sql, {"Schema": schema_str}

        # fallback xử lý riêng cho hướng nhà, pháp lý, nội thất
        value_fixed, op_fixed = fix_col_for_text_column(col, value, op)
        natural_cond, sql_cond, *_ = NaturalQueryGenerator.generate_natural_condition(col, value_fixed, op_fixed)
        return build_output(natural_cond, f"SELECT * FROM price_house WHERE {sql_cond}")

def generate_top_k_question(translated_col: str, k: int = 5) -> str:
    from realestate_text_to_sql_modules.templates import TEMPLATES_TOP_K
    return random.choice(TEMPLATES_TOP_K).format(k=k, col_name=translated_col)

def generate_between_location_question(translated_col: str, value1: str, value2: str, unit: str, location: str) -> str:
    from realestate_text_to_sql_modules.templates import TEMPLATES_RANGE_LOCATION

    if translated_col == 'giá':
        value1 = format_price_for_display(float(value1.replace(",", ".")))
        value2 = format_price_for_display(float(value2.replace(",", ".")))

    return random.choice(TEMPLATES_RANGE_LOCATION).format(
        col_name=translated_col,
        value1=value1,
        value2=value2,
        unit=unit,
        location=location
    )


