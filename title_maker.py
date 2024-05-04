from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from random import randint
from time import sleep

class Title:
    def __init__(self):
        pass

    def make_name(self):
        URL = 'https://wargm.ru/generator?g=male&r=human&f=japanese&l=ru'
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(URL)

        x = True
        while x:
            element = driver.find_element(By.ID, 'name1').text
            if element == 'Ожидайте...':
                sleep(0.5)
                continue
            x = False
        return element

    def gen_year(self):
        return randint(1185, 1868)

    def make_title(self):
        name = self.make_name()
        year = self.gen_year()
        return name, year


