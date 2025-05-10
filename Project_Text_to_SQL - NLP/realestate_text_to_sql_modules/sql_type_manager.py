import random

class SQLTypeManager:
    SQL_TYPE_RULES = {
    'simple_query':               {'sql_type': 'select',                        'ratio': 0.01},
    'top_k_query':                {'sql_type': 'select_orderby_desc_limit_k',   'ratio': 0.03},
    'range_query':               {'sql_type': 'select_where',                  'ratio': 0.06},  
    'comparison_query':          {'sql_type': 'select_where',                  'ratio': 0.10},
    'count_query':               {'sql_type': 'count_where',                   'ratio': 0.06},
    'like_query':                {'sql_type': 'select_where_like',             'ratio': 0.02},
    'extreme_max':               {'sql_type': 'select_orderby_desc_limit',     'ratio': 0.025},
    'extreme_min':               {'sql_type': 'select_orderby_asc_limit',      'ratio': 0.025},
    'location_price_query':      {'sql_type': 'select_where_and',              'ratio': 0.18},  
    'location_price_area_query': {'sql_type': 'select_where_and',              'ratio': 0.15},  
    'between_location_query':    {'sql_type': 'select_where_between_and',      'ratio': 0.10},
    'or_query':                  {'sql_type': 'select_where_or',               'ratio': 0.03}, 
}


    @classmethod
    def sample_question_type(cls) -> str:
        """
        Chọn ngẫu nhiên một question_type theo tỉ lệ đã định sẵn.
        """
        question_types = list(cls.SQL_TYPE_RULES.keys())
        weights = [cls.SQL_TYPE_RULES[q]['ratio'] for q in question_types]
        return random.choices(question_types, weights=weights, k=1)[0]

    @classmethod
    def get_sql_type(cls, question_type: str) -> str:
        """
        Chuyển đổi question_type (so sánh, khoảng, đếm...) sang sql_type để tổ chức output phù hợp.
        """
        return cls.SQL_TYPE_RULES.get(question_type, {}).get('sql_type', 'select')
