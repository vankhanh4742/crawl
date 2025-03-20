import json
import re
import unicodedata
from bs4 import BeautifulSoup

def remove_accents(text):
    """Loại bỏ dấu tiếng Việt và ký tự đặc biệt"""
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

def format_folder_name(text):
    """Chuyển chuỗi thành PascalCase: không dấu, không dấu gạch ngang"""
    text = remove_accents(text)  # Xóa dấu
    text = re.sub(r'[^a-zA-Z0-9-]', '', text)  # Chỉ giữ lại chữ, số và dấu gạch ngang
    return text.replace("-", "").title()  # Chuyển thành PascalCase

# Đọc file JSON
with open("extracted_links.json", "r", encoding="utf-8") as f:
    subjects = json.load(f)

updated_subjects = []

for subject in subjects:
    name = subject["name"]
    url = subject["url"]
    
    # Trích xuất main_folder từ URL
    match = re.search(r'vietjack\.me\/([a-z-]+\d+)', url)  # Lấy phần môn học từ URL
    if match:
        main_folder_raw = match.group(1)  # VD: 'dia-li-12'
        main_folder = format_folder_name(main_folder_raw)  # Chuyển thành: 'Diali12'
    else:
        main_folder = "Unknown"

    # Xác định danh mục con (KNTT, CD, CT, Default)
    if "-kn" in url:
        folder_category = "KNTT"
    elif "-cd" in url:
        folder_category = "CD"
    elif "-ct" in url:
        folder_category = "CT"
    else:
        folder_category = "Default"

    # Tạo folder_save đúng định dạng
    folder_save = f"{main_folder}/downloads_{main_folder}_{folder_category}"

    # Cập nhật dữ liệu
    updated_subjects.append({
        "name": name,
        "url": url,
        "folder_save": folder_save
    })

# Ghi kết quả ra file JSON mới
output_filename = "updated_links.json"
with open(output_filename, "w", encoding="utf-8") as f:
    json.dump(updated_subjects, f, ensure_ascii=False, indent=4)

print(f"✅ Đã cập nhật {len(updated_subjects)} mục và lưu vào '{output_filename}'.")
