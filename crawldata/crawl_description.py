from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json

with open("crawldata/data.json", "r", encoding="utf-8") as f:
    products = json.load(f)

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-notifications")

driver = webdriver.Chrome(options=chrome_options)

updated_products = []

for product in products:
    try:
        driver.get(product["url"])
        driver.execute_script("document.body.style.zoom='25%'")

        description = ""
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "block-content-product-left"))
            )

            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            block = soup.find("div", class_="block-content-product-left")
            if not block:
                description = ""
            else:
                for table in block.find_all("div", class_="table-content"):
                    table.decompose()

                first_p = block.find('p')
                if first_p:
                    content_parts = []
                    for node in first_p.contents:
                        if hasattr(node, 'get_text'):
                            text = node.get_text(strip=True)
                        else:
                            text = str(node).strip()
                        if text:
                            content_parts.append(text)
                    description = ' '.join(content_parts)
                else:
                    description = ""
        except:
            print(f"Không tìm thấy mô tả của sản phẩm {product['name']}")
            description = ""

        product_info = product.copy()
        product_info["description"] = description
        updated_products.append(product_info)

    except Exception as e:
        print(e)

with open("crawldata/data.json", "w", encoding="utf-8") as f:
    json.dump(updated_products, f, ensure_ascii=False, indent=2)

driver.quit()
