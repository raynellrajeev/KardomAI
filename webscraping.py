from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
url = 'https://www.indianspices.com/marketing/price/domestic/daily-price-small.html?page=1'
all_data = []

while True:
    driver.get(url)
    rows = driver.find_elements(By.XPATH, '//*[@id="block-system-main"]/div/div[6]/table/tbody/tr')
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        row_data = [cell.text for cell in cells]
        all_data.append(row_data)
    try:
        next_link = driver.find_element(By.PARTIAL_LINK_TEXT, "next")
        url = next_link.get_attribute('href')
    except NoSuchElementException:
        break

df = pd.DataFrame(all_data)
df.to_csv('scraped_data.csv', index=False)

driver.quit()
