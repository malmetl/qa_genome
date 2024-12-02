from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
import time
from PageObject.BasePages import basepage
from faker import Faker
from PageObject.UserPage import AuthPage
import pyautogui
from selenium.webdriver.common.keys import Keys
import os
import pytest

class PathogenCovidSample(basepage):
    PATHOGEN_NAME = By.XPATH, '//*[@id="app"]/div/div/header/div[2]/div[1]/div[2]/p' #Полен имя патогена
    SAMPLES = By.XPATH, '//*[@id="sample"]/div/button/h3' #Вкладка "Образцы"
    GRID_SAMPLES = By.XPATH, '//*[@id="sample"]/div[2]/ul/li[1]/a'
    UPLOAD_SAMPLES = By.XPATH, '//*[@id="sample"]/div[2]/ul/li[2]/a' #Загрузка образца
    SAMPLE_NAME = By.XPATH, '//*[@id="app"]/div/div/section/div/form/div[2]/div/div/div[1]/div/div/div/div[1]/div/div[2]/div/div[1]/input' #Название сиквенса
    DATE_BIOMATER = By.XPATH, '//*[@id="app"]/div/div/section/div/form/div[2]/div/div/div[3]/div/div/div/div[1]/div/div[2]/div/div[1]/input' #Дата забора образца
    TERRITORY_SAMPLE = By.XPATH, '//*[@id="app"]/div/div/section/div/form/div[2]/div/div/div[4]/div/div/div/div[1]/div/div/div/div[2]/div/div[1]/input' #Территория забора образца
    CT = By.XPATH, '//*[@id="app"]/div/div/section/div/form/div[2]/div/div/div[7]/div/div/div/div[1]/div/div[2]/div/input'
    AGE_PATIENT = By.XPATH, '//*[@id="app"]/div/div/section/div/form/div[3]/div/div/div[10]/div/div/div/div[1]/div/div[2]/div/div[1]/input' #Вораст пациента
    BUTTON_SAVE = By.XPATH, '//*[@id="app"]/div/div/section/div/form/div[6]/button' #Кнопка сохранить
    BUTTON_CONTINUE = By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/button' #Кнопка продолжить
    BUTTON_INFO = By.XPATH, '//*[@id="app"]/div/div/section/div/div[4]/ul/li[1]/div[2]/p[1]/button' #Кнопка инфо
    CHECK_SEQ_NAME = By.XPATH, '//*[@id="app"]/div/div/section/div/div[6]/div/div/div[1]/div[2]/div[1]/div/div[1]/p'

    def __init__(self, browser):
        super().__init__(browser)

    @allure.step('Переход на вкладку "Загрузка образца')
    def go_to_sample(self):
        time.sleep(2)
        self.logger.info(f'Going to add sequence using locator {self.SAMPLES}')
        self.is_present(PathogenCovidSample.SAMPLES)
        self.browser.find_element(*self.SAMPLES).click()
        time.sleep(2)
        self.logger.info(f'Going to add seq using {self.UPLOAD_SAMPLES} locator')
        self.browser.find_element(*self.UPLOAD_SAMPLES).click()

    @allure.step('Заполнение обязательных полей во вкладке "Загрузка Образца"')
    def add_info_placeholders_for_sample(self, sample_name, date_bm, ter_sample,ct, age):
        self.is_present(PathogenCovidSample.SAMPLE_NAME)
        self.logger.info(f'Send key {sample_name} to locator {self.SAMPLE_NAME}')
        self.browser.find_element(*self.SAMPLE_NAME).send_keys(sample_name)
        self.logger.info(f'Send key {date_bm} to locator {self.DATE_BIOMATER}')
        self.browser.find_element(*self.DATE_BIOMATER).send_keys(date_bm)
        self.logger.info(f'Send key {ter_sample} to locator {self.TERRITORY_SAMPLE}')
        self.browser.find_element(*self.TERRITORY_SAMPLE).send_keys(ter_sample)
        self.logger.info(f'Send key {ct} to locator {self.CT}')
        self.browser.find_element(*self.CT).send_keys(ct)
        time.sleep(1)
        self.browser.find_element(*self.TERRITORY_SAMPLE).send_keys(Keys.ENTER)
        self.logger.info(f'Send key {age} to locator {self.AGE_PATIENT}')
        self.browser.find_element(*self.AGE_PATIENT).send_keys(age)
        time.sleep(1)
        self.logger.info(f'Click to using {self.BUTTON_SAVE} button')
        self.browser.find_element(*self.BUTTON_SAVE).click()

    @allure.step('Переход на список сиквенсов')
    def grid_samples(self):
        self.is_present(PathogenCovidSample.BUTTON_CONTINUE)
        self.logger.info(f'Click to the {self.BUTTON_CONTINUE} button ')
        self.browser.find_element(*self.BUTTON_CONTINUE).click()
        self.logger.info(f'Going to add sequence using {self.SAMPLES} locator ')
        self.is_present(PathogenCovidSample.SAMPLES)
        self.browser.find_element(*self.SAMPLES).click()
        self.logger.info(f'Check info using {self.GRID_SAMPLES} locator')
        self.browser.find_element(*self.GRID_SAMPLES).click()

    @allure.step('Проверка полей образца')
    def check_sample_placeholders(self):
        self.is_present(PathogenCovidSample.BUTTON_INFO)
        self.logger.info(f'Click to the using{self.BUTTON_INFO} button ')
        self.browser.find_element(*self.BUTTON_INFO).click()