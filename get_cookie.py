from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time

from Config import config


class GetCookie:

    def __init__(self):
        EDGEDRIVER_PATH = config['EDGEDRIVER_PATH']
        service = Service(EDGEDRIVER_PATH)
        driver = webdriver.Edge(service=service)
        driver.get(config['url']['login'])
        time.sleep(2)
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        username_input.send_keys(config['username'])
        password_input.send_keys(config['password'])
        login_button = driver.find_element(By.ID, "login_submit")
        login_button.click()
        time.sleep(2)
        cookies = driver.get_cookies()
        self.cookie = {}
        for element in cookies:
            self.cookie[element['name']] = element['value']
        driver.quit()

    def get_cookie(self):
        return self.cookie
