import time
import os
from dotenv import load_dotenv
load_dotenv()

WEBSITE_LINK = os.getenv('WEBSITE_LINK', 'https://appbrewery.github.io/Zillow-Clone/')
FORM_LINK = os.getenv('FORM_LINK', 'https://docs.google.com/forms/d/e/1FAIpQLSeQkdVgb0uCnkFg_FndM2D3OOGrx4kji2hwNfN0YvefYF62zg/viewform?usp=sharing')
from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

request = requests.get(WEBSITE_LINK)
soup = BeautifulSoup(request.text, "html.parser")
addresses = soup.select("ul a address")
addresses_list = [element.get_text(strip=True).replace("|", "") for element in addresses]
print(addresses_list)

prices = soup.select('ul span[data-test="property-card-price"]')
prices_list = []
for element in prices:
    money = element.get_text(strip=True)
    new_price_text = money.replace(" 1 bd", "")
    next_new_price = new_price_text.replace(" 1bd", "")
    re_only_money = re.sub("/mo+","", next_new_price)
    only_money = re_only_money.replace("+", "")
    prices_list.append(only_money)
print(prices_list)

links = soup.select("ul a[data-test='property-card-link']")
links_list = [element.get("href") for element in links]
print(links_list)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.get(FORM_LINK)
time.sleep(1)
bot = True
list_added_links_to_form = []
count = 0
while bot is True:
    if links_list[count] in list_added_links_to_form:
        count += 1
        print("element already added")
        print("count +1")
    else:
        count += 1
        property_address = driver.find_element(By.XPATH,
                                               '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        property_address.send_keys(addresses_list[count])
        property_price = driver.find_element(By.XPATH,
                                             '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        property_price.send_keys(prices_list[count])
        property_link = driver.find_element(By.XPATH,
                                            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        property_link.send_keys(links_list[count])
        submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
        submit_button.click()
        submit_another_response_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
        time.sleep(1)
        submit_another_response_button.click()
        time.sleep(1)
        list_added_links_to_form.append(links_list[count])
        count += 1
