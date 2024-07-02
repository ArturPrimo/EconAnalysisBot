# Script for Name and URL Gathering

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# Set up the web driver
driver = webdriver.Chrome()

companies = {}

try:
    # Open br.investing.com
    driver.get("https://br.investing.com/equities/brazil")

    # Wait for the page to load
    time.sleep(5)  

    # Find all company elements
    company_elements = driver.find_elements(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[4]/div[2]/div[1]/table/tbody/tr/td/div/a')
    
    texts = [element.text for element in company_elements]
    print(texts)

    urls = [element.get_attribute('href') for element in company_elements]
    print(urls)

    companies = {texts[i]: urls[i] for i in range(len(texts))}
    print(companies)

        

finally:
    # Close the web driver
    time.sleep(2)
    driver.quit()

#Data found was then formatted using a JSON formatter which can be easily found online