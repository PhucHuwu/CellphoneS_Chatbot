from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import time

with open("crawldata/product_details.json", "r", encoding="utf-8") as f:
    products = json.load(f)

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-notifications")

driver = webdriver.Chrome(options=chrome_options)

faq_data = []

for product in products:
    try:
        driver.get(product["url"])
        driver.execute_script("document.body.style.zoom='25%'")
        
        time.sleep(2)
        
        try:
            box_faq = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "boxFAQ"))
            )

            html_content = box_faq.get_attribute('innerHTML')
            soup = BeautifulSoup(html_content, 'html.parser')

            accordion_items = soup.find_all('div', class_='accordion-item')

            for item in accordion_items:
                question_tag = item.find('h3')
                if question_tag:
                    question = question_tag.text.strip()

                    answer_container = item.find('div', class_='accordion-content')
                    if answer_container:
                        answer_parts = []
                        for element in answer_container.find_all(text=True):
                            text = element.strip()
                            if text:
                                answer_parts.append(text)

                        answer = " ".join(answer_parts).strip()

                        if question and answer:
                            faq_data.append({
                                "question": question,
                                "answer": answer
                            })
        except Exception as e:
            print(f"Không tìm thấy FAQ cho sản phẩm {product.get('name', '')}: {str(e)}")
        time.sleep(1)

    except Exception as e:
        print(e)

with open("crawldata/faq.json", "w", encoding="utf-8") as f:
    json.dump(faq_data, f, ensure_ascii=False, indent=2)

driver.quit()
