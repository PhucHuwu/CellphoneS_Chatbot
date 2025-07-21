from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import time


def split_into_sections(html_soup):
    known_section_titles = [
        "I. Nguyên tắc chung:",
        "II. Định nghĩa:",
        "I. Dành cho người mua hàng tại Website:",
        "II. Quy trình giao nhận vận chuyển",
        "I.Đổi mới 30 ngày miễn phí",
        "II.Bảo hành tiêu chuẩn",
        "I. Chính sách hủy giao dịch",
        "II.Chính sách đổi, trả hàng",
        "I. Sự chấp thuận",
        "II. Phạm vi thu thập",
        "III. Mục đích thu thập và sử dụng thông tin",
        "IV. Thời gian lưu trữ thông tin",
        "V. Đơn vị thu thập và quản lý thông tin cá nhân:",
        "VI. Quyền của Khách hàng đối với thông tin cá nhân - Phương tiện và công cụ để Khách hàng tiếp cận và chỉnh sửa, xóa dữ liệu cá nhân",
        "VII. Cam kết bảo mật thông tin cá nhân khách hàng và an toàn dữ liệu",
        "VIII. Quản lý thông tin xấu",
        "IX. Trách nhiệm trong trường hợp phát sinh lỗi kỹ thuật",
        "X. Quy trình tiếp nhận & giải quyết khiếu nại",
        "XI. Quyền và nghĩa vụ của Ban quản lý website TMĐT Cellphones.com.vn",
        "XII. Quyền và trách nhiệm khách hàng tham gia website TMĐT Cellphones.com.vn",
        "XIII. Những trường hợp từ chối hoặc hạn chế phục vụ khách hàng của Website TMĐT Cellphones.com.vn (*)",
        "XIV. Hiệu lực",
        "XV. Điều khoản cam kết"
    ]

    elements = html_soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div'])

    sections = []
    current_section = None
    current_content = []

    for element in elements[1:]:
        text = element.get_text().strip()
        if not text:
            continue

        is_known_title = False
        for title in known_section_titles:
            normalized_text = ' '.join(text.lower().split())
            normalized_title = ' '.join(title.lower().split())
            if normalized_text.startswith(normalized_title) or normalized_text == normalized_title:
                is_known_title = True
                if current_section:
                    sections.append({
                        "title": current_section,
                        "content": "\n".join(current_content).strip()
                    })

                current_section = text
                current_content = []
                break

        if not is_known_title and current_section:
            current_content.append(text)

    if current_section:
        sections.append({
            "title": current_section,
            "content": "\n".join(current_content).strip()
        })

    return sections


chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-notifications")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://cellphones.com.vn/tos")
driver.execute_script("document.body.style.zoom='25%'")

try:
    policy_list = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "warranty-options-item"))
    )

    all_policy_sections = []
    for idx, policy_item in enumerate(policy_list):
        if idx == 5:
            break
        driver.execute_script("arguments[0].click();", policy_item)
        time.sleep(1)

        category = policy_item.text.strip()
        content_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "warranty-content"))
        )

        html_content = content_element.get_attribute('innerHTML')
        soup = BeautifulSoup(html_content, 'html.parser')

        sections = split_into_sections(soup)

        for section in sections:
            all_policy_sections.append({
                "category": category,
                "title": section["title"],
                "content": section["content"]
            })

    with open("crawldata/policy_dataset.json", "w", encoding="utf-8") as f:
        json.dump(all_policy_sections, f, ensure_ascii=False, indent=2)

except Exception as e:
    print(e)
finally:
    driver.quit()
