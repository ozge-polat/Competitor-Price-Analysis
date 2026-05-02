from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

driver = webdriver.Chrome() 
url = "https://www.vatanbilgisayar.com/notebook/"
driver.get(url)
time.sleep(3)

def smooth_scrool(driver):
    total_height = driver.execute_script("return document.body.scrollHeight")
    step = 1000
    current_pos = 0
    while current_pos < total_height:
        current_pos += step
        driver.execute_script(f"window.scrollTo(0, {current_pos});")
        time.sleep(1)
        total_height = driver.execute_script("return document.body.scrollHeight")
        print(f"total_height: {total_height}, current_pos: {current_pos}") #for flow control

all_products = []
smooth_scrool(driver)
current_cards = driver.find_elements(By.CSS_SELECTOR, ".product-list.product-list--list-page")
print(f"Total selected card: {len(current_cards)}")

for card in current_cards:
        try:
            name = card.find_element(By.CSS_SELECTOR, ".product-list__product-name").text 
            price = card.find_element(By.CSS_SELECTOR, ".product-list__price").text 

            clean_price = price.replace(".","").strip() 
            print(f"{name},{clean_price}") #for flow control

            all_products.append({
                "Product Name": name,
                "Price": clean_price
            })

        except:
            continue
        
        print(f"Total product count: {len(all_products)}") 

        df = pd.DataFrame(all_products)
        df.to_csv("VatanNotebookPrices.csv", index=False)

print(f"{len(all_products)} product successfully processed")
driver.quit()