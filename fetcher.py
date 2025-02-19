import json
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

class ElectroImporter:
    if getattr(sys, 'frozen', False):  
        BASE_DIR = sys._MEIPASS
    else:  
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    json_path = os.path.join(BASE_DIR, "mapping.json")

   
    try:
        with open(json_path, "r", encoding="utf-8") as file:
            MAPPING = json.load(file)
    except FileNotFoundError:
        print(f"Error: mapping.json not found at {json_path}")
        sys.exit(1)  

    REGEX = r'www\.(.*)\.pl'
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_argument("--disable-extensions")  
    options.add_argument("--disable-infobars")  
    options.add_argument("--log-level=3") 
    options.add_argument("--disable-popup-blocking")  
    options.add_argument("--disable-background-networking") 
    options.add_argument("--disable-sync")  
    options.add_argument("--disable-translate") 
    def __init__(self,url):
        self.url = url
        self.driver = webdriver.Chrome(options=self.options)
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
        result = ""
        self.driver.get(self.url)
        mapping = self.MAPPING.get(self.title, {})
        button_selector = mapping.get("button")
        if button_selector:
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector))
            )
            button.click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, mapping.get("price")))
        )
        prices = self.driver.find_elements(By.CSS_SELECTOR, mapping.get("price"))

        visible_prices = [p for p in prices if p.is_displayed()]

        if not visible_prices:
            raise ValueError("No visible price element found!")

        price_text = visible_prices[0].text

        for char in price_text:
            if char.isdigit() or char == ",":
                result += char

        return float(result.replace(",", "."))

        

    def run(self):
        return self.get_price()
    

        