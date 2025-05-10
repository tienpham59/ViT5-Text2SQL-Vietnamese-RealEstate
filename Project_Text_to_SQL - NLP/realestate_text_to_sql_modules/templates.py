import random
from typing import List

TEMPLATES_LOCATION_PRICE = [
    "Có bất động sản nào {price_condition} ở {location} không?",
    "Tìm nhà {price_condition} ở {location}",
    "Tìm nhà {price_condition} tại {location}",  
    "Nhà nào đang rao bán {price_condition} tại {location}?",
    "Tôi muốn mua nhà {price_condition} ở {location}, có không?",
    "Liệt kê các nhà đất {price_condition} tại {location}",
    "Với tầm giá {price_text}, có nhà nào ở {location} không?",  
    "Bạn có nhà {price_condition} nào ở {location} không?",    
    "Tôi đang tìm nhà ở {location} giá {price_text}, có gợi ý nào không?",
    "Tìm nhà {location} giá {price_condition}",
    "Khu vực {location} có nhà nào {price_condition} không?",
    "Ở {location} có căn nào {price_condition} không?",
    "Tôi muốn tìm nhà ở {location} giá {price_condition}, có không?",
    "Có nhà nào ở {location} mà giá {price_condition} không?",
    "Tôi đang cần mua nhà tại {location} trong tầm giá {price_condition}, có không?",
    "Tôi đang nhắm khu {location}, có căn nào {price_condition} không bạn?"
]

TEMPLATES_PRICE_COMPARISON = [
    "Nhà nào giá {comparison_term} {value_str}{unit}?",
    "Tìm nhà giá {comparison_term} {value_str}{unit}",
    "Giá nhà nào {comparison_term} {value_str}{unit} vậy?",
    "Có căn nào giá {comparison_term} {value_str}{unit} không?",
    "Bạn có biết nhà nào giá {comparison_term} {value_str}{unit} không?",
    "Tôi đang tìm nhà tầm giá {value_str}{unit}, có không?"
]

TEMPLATES_COMPARISON_EQUAL = [
    "Tìm nhà có {col_name} là {value_str}{unit}",
    "Liệt kê các nhà có {col_name} là {value_str}{unit}",
    "Có nhà nào có {value_str}{unit} {col_name} không?",
    "Nhà nào quay hướng {value_str}?",
    "Có căn nào hướng {value_str} không?",
    "Tôi muốn tìm nhà hướng {value_str}, có không?",
    "Bạn có biết nhà nào hướng {value_str} không?",
    "Nhà nào có hướng {value_str} vậy?",
    "Nhà nào có tình trạng pháp lý là {value_str}?",
    "Có nhà nào pháp lý {value_str} không?",
    "Tôi muốn tìm nhà có pháp lý {value_str}, có không?",
    "Nhà nào nội thất {value_str}?",
    "Có căn nào nội thất {value_str} không?",
    "Tôi muốn tìm nhà nội thất {value_str}, có không?",
    "Nhà nào có {value_str} phòng ngủ?",
    "Tôi muốn tìm nhà có {value_str} phòng ngủ, có không?",
    "Có căn nào có {value_str} phòng tắm không?",
    "Tôi cần tìm nhà có {value_str} phòng tắm, có không?",
    "Nhà nào có {value_str} tầng?",
    "Tôi muốn tìm nhà có {value_str} tầng, có không?",
    "Có căn nào {value_str} tầng không?",
    "Bạn có biết nhà nào {value_str} tầng không?"
]


TEMPLATES_COMPARISON_OP = [
    "Nhà nào mà {col_name} {comparison_term} {value_str}{unit} vậy?",
    "Có nhà nào {col_name} {comparison_term} {value_str}{unit} không bạn?",
    "Tìm nhà có {col_name} {comparison_term} {value_str}{unit}",
    "Bất động sản nào có {col_name} {comparison_term} {value_str}{unit}?"
]

TEMPLATES_RANGE = [
    "Tìm nhà có {col_name} từ {value1}{unit} đến {value2}{unit}",
    "Có bất động sản nào {col_name} trong khoảng {value1}{unit} – {value2}{unit} không?",
    "Tôi muốn tìm nhà với {col_name} từ {value1}{unit} đến {value2}{unit}",
    "Liệt kê nhà đất có {col_name} từ {value1}{unit} đến {value2}{unit}",
    "Nhà nào có {col_name} nằm giữa {value1}{unit} và {value2}{unit}?",
    "Khoảng {value1}-{value2}{unit} {col_name} thì có nhà nào không?",
    "Bạn lọc giúp tôi nhà {col_name} cỡ {value1}{unit} tới {value2}{unit}"
]

TEMPLATES_SPECIFIC = [
    "Liệt kê {column_list} của các bất động sản",
    "Cho tôi danh sách {column_list} trong bảng nhà đất",
    "Tôi muốn xem {column_list} của các nhà đang rao bán",
    "Có thể hiển thị {column_list} giúp tôi được không?",
    "Cần xem thông tin {column_list} của toàn bộ bất động sản",
    "Tôi cần xem {column_list}, bạn có thể show giúp không?",
    "Hiện {column_list} của tất cả nhà đất cho tôi xem với"
]

TEMPLATES_LIKE = [
    "Tìm nhà ở khu vực có thành phố chứa từ '{kw}'?",
    "Có nhà nào ở địa danh có từ '{kw}' không?",
    "Tôi muốn tìm nhà ở nơi có tên gồm '{kw}'",
    "Thành phố nào có tên chứa từ '{kw}' đang có nhà bán?",
    "Có nhà nào ở chỗ nào đó có chữ '{kw}' trong tên không?",
    "Tìm giúp tôi nhà ở khu vực nào đó liên quan đến '{kw}'"
]

TEMPLATES_OR = [
    "Có nhà nào có {col1} {phrase1}{unit1} hoặc {col2} {phrase2}{unit2} không?",
    "Nhà nào có {value_str} {col1} hoặc {value_str} {col2} không?",
    "Tôi muốn tìm nhà có {col1} là {value_str}, hoặc {col2} là {value_str}, có không?"
    "Bạn có biết căn nào có {col1} {phrase1}{unit1} hoặc {col2} {phrase2}{unit2} không?"
]

TEMPLATES_EXTREME_MAX = [
    "Nhà nào có {col_name} cao nhất?",
    "Bất động sản nào có {col_name} lớn nhất?",
    "Cho tôi biết nhà có {col_name} cao nhất",
    "Nhà nào đứng đầu về {col_name}?",
    "Top 1 {col_name} là nhà nào?"
]

TEMPLATES_EXTREME_MIN = [
    "Nhà nào có {col_name} thấp nhất?",
    "Bất động sản nào có {col_name} nhỏ nhất?",
    "Cho tôi biết nhà có {col_name} thấp nhất",
    "Nhà nào ít {col_name} nhất?",
    "Top nhà thấp nhất về {col_name} là nhà nào?"
]

TEMPLATES_COUNT = [
    "Có bao nhiêu nhà có {condition}?",
    "Số lượng bất động sản {condition} là bao nhiêu?",
    "Ủa, nhiều nhà {condition} không ta?",
    "Tôi muốn biết có nhiều căn {condition} không?",
    "Bạn thống kê giúp mình số căn {condition} nha!",
    "Có nhiều nhà giá {comparison_term} {value_str}{unit} không?",
    "Số lượng căn có giá {comparison_term} {value_str}{unit} là bao nhiêu?",
    "Bao nhiêu nhà có giá {comparison_term} {value_str}{unit}?"
]

TEMPLATES_TOP_K = [
    "Top {k} căn có {col_name} cao nhất là gì?",
    "Cho tôi biết {k} nhà có {col_name} lớn nhất",
    "Top {k} bất động sản có {col_name} lớn nhất hiện tại?",
    "{k} căn nhà có {col_name} cao nhất đang rao bán là gì?",
    "Tôi muốn biết top {k} nhà có {col_name} lớn nhất"
]

TEMPLATES_RANGE_LOCATION = [
    "Tìm nhà có {col_name} từ {value1}{unit} đến {value2}{unit} ở {location}",
    "Có bất động sản nào {col_name} khoảng {value1}{unit} – {value2}{unit} tại {location} không?",
    "Tôi muốn mua nhà {col_name} trong khoảng {value1}{unit} đến {value2}{unit} ở {location}",
    "Nhà nào có {col_name} từ {value1}{unit} đến {value2}{unit} nằm tại {location}?",
    "Tôi đang tìm nhà diện tích {value1}{unit}–{value2}{unit} ở {location}, có không?"
]

TEMPLATES_LOCATION_PRICE_AREA = [
    "Tìm nhà ở {location}, giá {price_condition}, diện tích {area_condition}.",
    "Có nhà nào ở {location} diện tích {area_condition}, giá {price_condition} không?",
    "Tôi đang cần nhà ở {location}, khoảng {price_condition}, từ {area_condition} trở lên.",
    "Bạn gợi ý giúp nhà nào ở {location} giá {price_condition}, diện tích {area_condition} nhé.",
    "Tìm nhà tại {location}, {price_condition}, diện tích {area_condition}.",
    "Tìm nhà ở {location} diện tích {area_condition}, giá {price_condition}.",
    "Tôi muốn mua nhà ở {location}, diện tích {area_condition}, giá {price_condition}.",
    "Có căn nào {area_condition} ở {location}, giá {price_condition} không?",
    "Tôi đang tìm nhà khoảng {area_condition}, ở {location}, giá {price_condition}.",
    "Tìm nhà ở {location} giá {price_condition}, diện tích {area_condition}.",
    "Tôi muốn mua nhà giá {price_condition}, ở {location}, diện tích {area_condition}.",
    "Có nhà nào giá {price_condition}, diện tích {area_condition}, ở {location} không?",
    "Khoảng {price_condition}, diện tích {area_condition}, có căn nào ở {location} không?"
]
