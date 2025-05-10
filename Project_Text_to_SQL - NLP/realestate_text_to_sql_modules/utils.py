import re

# Các hàm tiện ích dùng trong xử lý văn bản và hiển thị giá trị

def format_number(value: float) -> str:
    """
    Định dạng số:
    - Nếu là số nguyên → không hiển thị phần thập phân
    - Nếu là số thực → làm tròn 1 chữ số và đổi dấu '.' thành ','
    """
    if int(value) == value:
        return str(int(value))
    else:
        return str(round(value, 1)).replace(".", ",")

def format_price_for_display(value: float) -> str:
    """
    Chuyển giá trị số sang định dạng dễ đọc kiểu "4,5 tỷ"
    """
    if value > 1_000_000_000:
        value = value / 1_000_000_000

    if value.is_integer():
        return f"{int(value)} tỷ"
    else:
        return f"{str(round(value, 1)).replace('.', ',')} tỷ"

def reverse_price_string_to_number(price_str: str) -> int:
    """
    Chuyển chuỗi dạng "4,5 tỷ" thành số nguyên 4500000000
    """
    raw = float(price_str.replace(" tỷ", "").replace(",", "."))
    return int(raw * 1_000_000_000)

def sanitize_question(text: str) -> str:
    """
    Làm sạch câu hỏi: loại các lỗi thường gặp, ngữ pháp sai
    """
    text = text.replace("nhà nhà", "nhà")
    text = text.replace("liệt kê nhà nhà", "liệt kê nhà")
    text = text.replace("liệt kê các nhà có", "các nhà có")
    text = text.replace("tôi cần nhà và là", "tôi cần nhà có")
    text = text.replace("option nào", "")
    text = text.replace("giá?", "giá")
    text = text.replace("và là", "có")
    text = text.replace("liệt kê các nhà", "có nhà")
    return text.strip()
