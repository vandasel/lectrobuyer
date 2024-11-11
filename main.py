import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
# driver.get("https://www.selenium.dev/selenium/web/web-form.html")

# title = driver.title

# driver.implicitly_wait(0.5)

# text_box = driver.find_element(by=By.NAME, value="my-text")
# submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

# text_box.send_keys("Selenium")
# submit_button.click()

# message = driver.find_element(by=By.ID, value="message")
# text = message.text

# driver.quit()


class ElectroImporter:
    
    with open('mapping.json', 'r') as file:
        MAPPING = json.load(file)

    REGEX = r'www\.(.*)\.pl'

    def __init__(self,url):
        self.url = url
        self.driver = webdriver.Chrome()
        self.title = self.get_title(url,self.REGEX)

    @staticmethod
    def get_title(url,pattern):
        match = re.search(pattern,url)
        if match:
            text = match.group(1)    
        if text:
            return text
        return "deferror"
        

    def get_price(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(0.5)
        mapping = self.MAPPING.get(self.title,{})
        button = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, mapping.get("button")))
        )
        button.click()
        price = self.driver.find_element(by=By.XPATH,value=mapping.get("price"))
        self.driver.implicitly_wait(0.5)
        return price.text
    

    def run(self):
        return self.get_price()
    

        