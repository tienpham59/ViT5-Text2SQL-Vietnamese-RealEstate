"""
Module: constants.py

Purpose:
    Stores schema definitions and column/operator mappings for the Text-to-SQL system.

Key Components:
    - SCHEMA_DEFINITION: Full schema with column names and types
    - COLUMN_TRANSLATIONS: Maps schema column names to natural Vietnamese descriptions
    - COMPARISON_TERMS: Maps SQL operators to natural Vietnamese phrases

Usage:
    from realestate_text_to_sql_modules.constants import SCHEMA_DEFINITION
    print(SCHEMA_DEFINITION)
"""

SCHEMA_DEFINITION = [
    "address[str]", "area[float]", "frontage[float]", "access_road[float]", "house_direction[str]",
    "balcony_direction[str]", "floors[int]", "bedrooms[int]", "bathrooms[int]", "legal_status[str]",
    "furniture_state[str]", "price[float]", "city[str]", "district[str]", "ward[str]", "cluster_label[str]"
]

COLUMN_TRANSLATIONS = {
    'address': 'địa chỉ',
    'area': 'diện tích',
    'price': 'giá',
    'frontage': 'mặt tiền',
    'access_road': 'đường vào',
    'house_direction': 'hướng nhà',
    'balcony_direction': 'hướng ban công',
    'floors': 'tầng',
    'bedrooms': 'phòng ngủ',
    'bathrooms': 'phòng tắm',
    'legal_status': 'tình trạng pháp lý',
    'furniture_state': 'tình trạng nội thất',
    'city': 'thành phố',
    'district': 'quận huyện',
    'ward': 'phường xã',
    'cluster_label': 'phân khúc'
}

COMPARISON_TERMS = {
    'price': {
        '>': ['đắt hơn', 'cao hơn', 'trên'],
        '<': ['rẻ hơn', 'thấp hơn', 'dưới'],
        '=': ['bằng', 'khoảng', 'tầm'],
        'BETWEEN': ['từ', 'đến']
    },
    'quantity': {
        '>': ['nhiều hơn','hơn', 'trên'],
        '<': ['ít hơn', 'dưới'],
        '=': ['đúng', 'bằng'],
        'BETWEEN': ['từ', 'đến']
    }
}
