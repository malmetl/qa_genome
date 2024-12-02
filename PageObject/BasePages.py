import time
import selenium
from selenium.webdriver.support import expected_conditions as EC
import json
import os
import logging
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import allure
import pytest
from PageObject.SarsCoV.API import AuthTokenPage


class basepage:
    waiting = By.XPATH, '//*[@id="app"]/div/div/header/div[2]/div[1]/div[1]/div/div[2]/div/div/div[2]/div/div[1]/input'
    SEARCH_TABLE = By.XPATH, '//*[@id="app"]/div/div/header/div[2]/div[1]/div[1]/div/div[2]/div/div/div[2]/div/div[1]/input'
    FIRST_PATHOGEN = By.XPATH, '//*[@id="0"]'
    Instruction_covid19 = By.XPATH, '//*[@id="app"]/div/div/header/div[2]/div[2]/div/div[1]/div/div[7]/div[1]/a'

    def __init__(self, browser, log_level=logging.INFO, to_file=False, wait=50):
        self.browser = browser
        self.actions = ActionChains(browser)
        self.__config_logger(log_level, to_file)
        self.wait = WebDriverWait(browser, wait)
        self.session = requests.Session()
        self.environment_info = self.__get_environment_info()
        self.__add_environment_info(self.environment_info)

    def __config_logger(self, log_level, to_file):
        self.logger = logging.getLogger(type(self).__name__)
        self.logger.setLevel(log_level)
        if not self.logger.hasHandlers():
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            if to_file:
                os.makedirs("logs", exist_ok=True)
                file_handler = logging.FileHandler('logs/application.log')
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def __get_environment_info(self):
        return {
            "Browser": os.getenv("BROWSER", "Chrome"),
            "Browser.Version": os.getenv("BROWSER_VERSION", "130.0.6613.84"),
            "Stand": os.getenv("STAND", "Production"),
            "API_URL": os.getenv("API_URL", "https://genomenvpn.crie.ru/new/app/main")
        }

    def __add_environment_info(self, info):
        with open('allure-results/environment.properties', 'w') as f:
            for key, value in info.items():
                f.write(f"{key}={value}\n")

    def __wait_element(self, locator):
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except selenium.common.exceptions.TimeoutException:
            allure.attach(
                name="screenshot",
                body=self.browser.get_screenshot_as_png()
            )
            raise AssertionError(f"Element {locator} not found.")

    @allure.step(f'Ожидание локатора')
    def is_present(self, locator):
        self.__wait_element(locator)


    @allure.step('Открыть страницу авторизации')
    def get_open_auth_page(self, base_url):
        self.logger.info(f'Going to {base_url} url')
        self.browser.get(base_url)

    @allure.step('Найти патоген Sars-CoV-2')
    def search_sars_cov_2(self, pathogenName):
        self.logger.info(f'Going to Sars-Cov-2')
        self.browser.find_element(*self.SEARCH_TABLE).click()
        self.logger.info(f'Send key {pathogenName} to table {self.SEARCH_TABLE}')
        self.browser.find_element(*self.SEARCH_TABLE).send_keys(pathogenName)
        self.logger.info(f'Click to Sars-Cov-2')
        time.sleep(1)
        self.browser.find_element(*self.FIRST_PATHOGEN).click()

    @allure.step('Переход на вкладку "Инструкции"')
    def check_instruction(self):
        time.sleep(1)
        self.is_present(self.Instruction_covid19)
        self.logger.info(f'Click to the {self.Instruction_covid19} locator ')
        self.browser.find_element(*self.Instruction_covid19).click()
