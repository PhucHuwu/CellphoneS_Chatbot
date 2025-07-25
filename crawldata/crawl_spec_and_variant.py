from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

updated_products = []

for product in products:
    try:
        driver.get(product["url"])
        driver.execute_script("document.body.style.zoom='25%'")

        time.sleep(5)

        color_price_list = []

        try:
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".box-product-variants .list-variants"))
            )
            variants = driver.find_elements(By.CSS_SELECTOR, ".box-product-variants .list-variants li.item-variant")
            for variant in variants:
                try:
                    color_name = variant.find_element(By.CSS_SELECTOR, "strong.item-variant-name").text.strip()
                    price = variant.find_element(By.CSS_SELECTOR, "span.item-variant-price").text.strip()
                    color_price_list.append({
                        "color": color_name,
                        "price": price
                    })
                except:
                    continue
        except:
            print(f"Không tìm thấy biến thể màu sắc và giá tiền của sản phẩm {product['name']}")

        xem_tat_ca_button = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button.button__show-modal-technical'))
        )
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", xem_tat_ca_button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", xem_tat_ca_button)

        time.sleep(5)

        try:
            WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CLASS_NAME, "teleport-modal_content")))
            sections = driver.find_elements(By.CSS_SELECTOR, "section.technical-content-section")

            specs = {}

            for section in sections:
                try:
                    title = section.find_element(By.CSS_SELECTOR, "p.title").text.strip()
                    rows = section.find_elements(By.CSS_SELECTOR, "tr.technical-content-item")
                    for row in rows:
                        spec_name = row.find_element(By.CSS_SELECTOR, "td:first-child").text.strip()
                        spec_value = row.find_element(By.CSS_SELECTOR, "td:last-child").text.strip()
                        specs[spec_name] = spec_value
                except:
                    continue
        except:
            print(f"Không tìm thấy thông số kỹ thuật của sản phẩm {product['name']}")

        updated_products.append({
            "id": product["url"].split("/")[-1].replace(".html", ""),
            "name": product["name"],
            "url": product["url"],
            "specs": specs,
            "variants": color_price_list
        })

        # break  # Uncomment to debug
    except Exception as e:
        print(e)

with open("crawldata/product_details.json", "w", encoding="utf-8") as f:
    json.dump(updated_products, f, ensure_ascii=False, indent=2)

driver.quit()
