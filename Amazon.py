from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# 1. Setup Chrome Options
options = Options()

# Argument 1: run browser normally (you can add headless later)
options.add_argument("--start-maximized")

# Argument 2: avoid detection
options.add_argument("--disable-blink-features=AutomationControlled")

# Argument 3: user-agent (important for Amazon)
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
)

# 2. Open Browser
driver = webdriver.Chrome(options=options)

url = "https://www.amazon.com/s?k=headset"
driver.get(url)

# wait for page to load
time.sleep(5)

# 3. Get Page Source
soup = BeautifulSoup(driver.page_source, "html.parser")

products = soup.find_all("div", {"data-component-type": "s-search-result"})

data = []

# 4. Extract Data
for item in products:

    # Product Name
    name_tag = item.h2
    name = name_tag.text.strip() if name_tag else "N/A"

    # Price
    price_whole = item.find("span", "a-price-whole")
    price_fraction = item.find("span", "a-price-fraction")

    if price_whole and price_fraction:
        price = price_whole.text + price_fraction.text
    else:
        price = "N/A"

    # Rating
    rating_tag = item.find("span", "a-icon-alt")
    rating = rating_tag.text if rating_tag else "N/A"

    # Image
    img_tag = item.find("img", "s-image")
    image = img_tag["src"] if img_tag else "N/A"

    data.append({
        "name": name,
        "price": price,
        "rating": rating,
        "image": image
    })

# 5. Print Output
print("\nName | Price | Rating | Image\n")
print("-" * 120)

for d in data[:10]:   # first 10 products
    print(f"{d['name']} | {d['price']} | {d['rating']} | {d['image']}")

driver.quit()

import csv

# 6. Save to CSV
import csv
import os

# Get Downloads path automatically
downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")

file_path = os.path.join(downloads_path, "amazon_headsets.csv")

# Save to CSV
with open(file_path, "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)

    # Header
    writer.writerow(["Name", "Price", "Rating", "Image"])

    # Data
    for d in data:
        writer.writerow([d["name"], d["price"], d["rating"], d["image"]])

print("File saved at:", file_path)
