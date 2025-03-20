import json
import re
import requests
from bs4 import BeautifulSoup

def sanitize_filename(filename):
    """
    Hàm làm sạch tên (loại bỏ các ký tự không hợp lệ cho tên file hay folder)
    """
    filename = re.sub(r'[\\/:*?"<>|]', "", filename)
    return filename.strip().replace(" ", "")

def slugify(text):
    """
    Chuyển đổi chuỗi thành dạng chỉ còn chữ và số (loại bỏ khoảng trắng, ký tự đặc biệt)
    """
    return "".join(char for char in text if char.isalnum())

# URL của trang cần crawl (bạn có thể thay đổi URL tại đây)
url = "https://vietjack.me/"

# Lấy nội dung trang
response = requests.get(url)
if response.status_code != 200:
    print("Lỗi khi lấy nội dung trang:", response.status_code)
    exit(1)

soup = BeautifulSoup(response.content, "lxml")

# Danh sách chứa kết quả theo cấu trúc yêu cầu
subjects_list = []

# Tìm tất cả các thẻ h3 đại diện cho thông tin môn học
subject_headers = soup.find_all("h3", class_="title font-weight-bold text-uppercase")
if not subject_headers:
    print("Không tìm thấy thẻ môn học (h3) nào trên trang!")
else:
    for subject_header in subject_headers:
        # Lấy tên môn học, ví dụ: "Lớp 11"
        subject_name = subject_header.get_text(strip=True)
        print(f"Đã tìm thấy môn học: {subject_name}")

        # Tìm các thẻ anh (a) chứa thẻ h2 với class "object-title"
        # Ta sẽ duyệt các phần tử anh em (sibling) sau thẻ h3 cho đến khi gặp thẻ h3 tiếp theo
        sibling = subject_header.find_next_sibling()
        while sibling and sibling.name != "h3":
            if sibling.name == "a":
                h2 = sibling.find("h2", class_="object-title")
                if h2:
                    # Lấy tiêu đề danh mục (có thể là "Đề thi các môn lớp 11" hoặc "Lớp 11 - Kết nối tri thức")
                    category_title = h2.get_text(strip=True)
                    link = sibling.get("href")
                    if link:
                        # Tạo folder_save dựa trên tên môn học và danh mục (loại bỏ khoảng trắng và ký tự đặc biệt)
                        folder_save = f"{sanitize_filename(subject_name)}/downloads_{slugify(category_title)}"
                        subjects_list.append({
                            "name": subject_name,
                            "url": link,
                            "folder_save": folder_save
                        })
                        print(f"  >> Tìm thấy danh mục: '{category_title}' với link: {link}")
            sibling = sibling.find_next_sibling()

# Ghi kết quả ra file JSON với định dạng đẹp
output_filename = "subjects.json"
with open(output_filename, "w", encoding="utf-8") as f:
    json.dump(subjects_list, f, ensure_ascii=False, indent=4)

print(f"\nĐã ghi thông tin crawl vào file '{output_filename}' với {len(subjects_list)} mục.")
