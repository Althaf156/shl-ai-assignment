from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json

options = Options()

options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

url = "https://www.shl.com/solutions/products/product-catalog/"

driver.get(url)

print("Opening SHL catalog...")

time.sleep(5)

last_height = driver.execute_script("return document.body.scrollHeight")

for i in range(10):

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    print(f"Scrolling {i+1}...")

    time.sleep(3)

    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        break

    last_height = new_height

links = driver.find_elements(By.TAG_NAME, "a")

assessments = []

for link in links:

    try:
        text = link.text.strip()
        href = link.get_attribute("href")

        if text and href:
            if "/products/product-catalog/view/" in href:

                assessments.append({
                    "name": text,
                    "url": href
                })

    except:
        pass

unique_assessments = []

seen = set()

for item in assessments:

    if item["url"] not in seen:
        seen.add(item["url"])
        unique_assessments.append(item)

print("Assessments Found:", len(unique_assessments))

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(unique_assessments, f, indent=4)

print("Data saved successfully")

input("Press Enter to close browser...")

driver.quit()