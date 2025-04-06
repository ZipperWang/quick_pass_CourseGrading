from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time

from Config import config


class GetCookie:

    def __init__(self):
        EDGEDRIVER_PATH = config['EDGEDRIVER_PATH']
        service = Service(EDGEDRIVER_PATH)
        self.driver = webdriver.Edge(service=service)
        self.driver.get(config['url']['login'])
        time.sleep(2)
        username_input = self.driver.find_element(By.NAME, "username")
        password_input = self.driver.find_element(By.NAME, "password")
        username_input.send_keys(config['username'])
        password_input.send_keys(config['password'])
        login_button = self.driver.find_element(By.ID, "login_submit")
        login_button.click()
        time.sleep(2)
        self.cookies = self.driver.get_cookies()
        self.cookie = {}
        for element in self.cookies:
            self.cookie[element['name']] = element['value']

    def get_cookie(self):
        print(self.cookies)
        return self.cookie

    def get_driver(self):
        return self.driver
