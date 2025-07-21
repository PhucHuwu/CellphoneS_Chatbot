from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-notifications")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://cellphones.com.vn/mobile/apple.html")

while True:
    try:
        show_more_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.button.btn-show-more.button__show-more-product'))
        )
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", show_more_button)
        show_more_button.click()
        time.sleep(1)
    except:
        break

product_elements = driver.find_elements(By.CSS_SELECTOR, 'div.product-info-container.product-item')
products = []

for product in product_elements:
    try:
        a_tag = product.find_element(By.CSS_SELECTOR, 'a.product__link.button__link')
        href = a_tag.get_attribute("href")

        name_tag = a_tag.find_element(By.CSS_SELECTOR, 'div.product__name')
        name = name_tag.text.strip()

        if name and href:
            products.append({
                "name": name,
                "url": href
            })
    except:
        continue

with open("crawldata/data.json", "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

driver.quit()
