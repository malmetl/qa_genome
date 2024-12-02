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


class PathogenCovidSequence(basepage):
    PATHOGEN_NAME = By.XPATH, '//*[@id="app"]/div/div/header/div[2]/div[1]/div[2]/p' #Полен имя патогена
    SEQUENCES = By.XPATH, '//*[@id="sequence"]/div/button/h3' #Вкладка "Сиквенсы"
    GRID_SEQ = By.XPATH, '//*[@id="sequence"]/div[2]/ul/li[1]/a'
    UPLOAD_SEQ = By.XPATH, '//*[@id="sequence"]/div[2]/ul/li[2]/a' #Загрузка сиквенса
    SEQUENCE_NAME = By.XPATH, '//*[@id="app"]/div/div/section/div/form/div[2]/div/div/div[1]/div/div/div/div[1]/div/div[2]/div/div[1]/input' #Название сиквенса
    DATE_STUDY = By.XPATH, '//*[@id="app"]/div/div/section/div/form/div[2]/div/div/div[3]/div/div/div/div[1]/div/div[2]/div/div[1]/input' #Дата проведение исследования
    SAMPLE_NAME = By.XPATH, '//*[@id="app"]/div/div/section/div/form/div[3]/div/div/div[1]/div/div/div/div[1]/div/div[2]/div/div[1]/input' #Имя образца
    DATE_BIOMATER = By.XPATH, '//*[@id="app"]/div/div/section/div/form/div[3]/div/div/div[3]/div/div/div/div[1]/div/div[2]/div/div[1]/input' #Дата забора образца
    TERRITORY_SAMPLE = By.XPATH, '/html/body/div[1]/div/div/section/div/form/div[3]/div/div/div[4]/div/div/div/div[1]/div/div/div/div[2]/div/div[1]/input' #Территория забора образца
    OBJECT_TOWN = By.XPATH, '//button[contains(text(), "Россия, г Москва")]'
    CT = By.XPATH, '//*[@id="app"]/div/div/section/div/form/div[3]/div/div/div[7]/div/div/div/div[1]/div/div[2]/div/input' #CT
    AGE_PATIENT = By.XPATH, '//*[@id="app"]/div/div/section/div/form/div[4]/div/div/div[10]/div/div/div/div[1]/div/div[2]/div/div[1]/input' #Вораст пациента
    AUTHORS = By.XPATH, '//*[@id="app"]/div/div/section/div/form/div[6]/div/div/div[3]/div/div/div/div[1]/div/div[2]/div/div[1]/input' #ПОле авторы
    IMPORT_FILE = By.XPATH, '//*[@id="15300"]' #Загрузка файла
    BUTTON_SAVE = By.XPATH, '//*[@id="app"]/div/div/section/div/form/div[8]/button' #Кнопка сохранить
    BUTTON_CONTINUE = By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/button' #Кнопка продолжить
    BUTTON_INFO = By.XPATH, '//*[@id="app"]/div/div/section/div/div[4]/ul/li[1]/div[2]/p[1]/button' #Кнопка инфо
    CHECK_SEQ_NAME = By.XPATH, '//*[@id="app"]/div/div/section/div/div[6]/div/div/div[1]/div[2]/div[1]/div/div[1]/p'
    ALL_EDIT = By.XPATH, '//*[@id="app"]/div/div/section/div/div[4]/ul/li[1]/div[1]/div[1]/div/div/button/img' #Что можно делать с сиквенсом
    EDIT_BUTTON = By.XPATH, '//*[@id="app"]/div/div/section/div/div[4]/ul/li[1]/div[1]/div[1]/div[2]/div[1]/div[1]/p' #Редактировать
    EDIT_SEQ_NAME = By.XPATH, '//*[@id="app"]/div/div/section/div/div[6]/div/div/div/form/div[2]/div/div/div[1]/div/div/div/div[1]/div/div[2]/div/div[1]/input' #Поле редактирования сиквенса
    EDIT_BUTTON_SAVE = By.XPATH, '//*[@id="app"]/div/div/section/div/div[6]/div/div/div/form/div[8]/button' #Кнопка в окне редактирования
    COPY_SEQ = By.XPATH, '//*[@id="app"]/div/div/section/div/div[4]/ul/li[1]/div[1]/div[1]/div[2]/div[1]/div[2]/p' #Кнопка "Копировать"
    EDIT_BUTTON_CONTINUE = By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/button'
    BUTTON_SAVE_COPY = By.XPATH, '//*[@id="app"]/div/div/section/div/div[6]/div/div/div/form/div[8]/button'
    EDIT_IMPORT_FILE = By.XPATH, '/html/body/div[1]/div/div/section/div/div[6]/div/div/div/form/div[7]/div/div/div/div/div/div/div[1]/div/div/input' #При копии заказака
    DELETE_SEQ = By.XPATH, '//*[@id="app"]/div/div/section/div/div[4]/ul/li[1]/div[1]/div[1]/div[2]/div[3]/div/p'
    TRUE_DELETE = By.XPATH, '//*[@id="app"]/div/div/section/div/div[6]/div/div/div[2]/button[1]'
    def __init__(self, browser):
        super().__init__(browser)

    @allure.step('Переход на вкладку "Загрузка сиквенса')
    def go_to_add_seq(self):
        time.sleep(2)
        self.logger.info(f'Going to add sequence using locator {self.SEQUENCES}')
        self.is_present(PathogenCovidSequence.SEQUENCES)
        self.browser.find_element(*self.SEQUENCES).click()
        time.sleep(2)
        self.logger.info(f'Going to add seq using {self.UPLOAD_SEQ} locator')
        self.browser.find_element(*self.UPLOAD_SEQ).click()

    @allure.step('Заполнение обязательных полей во вкладке "Загрузка сиквенса"')
    def add_info_placeholders(self, seq_name, date_st, sample_name, date_bm, ter_sample, ct, age, author):
        self.logger.info(f'Send key {seq_name} to locator {self.SEQUENCE_NAME}')
        self.is_present(PathogenCovidSequence.SEQUENCE_NAME)
        self.browser.find_element(*self.SEQUENCE_NAME).send_keys(seq_name)
        self.logger.info(f'Send key {date_st} to locator {self.DATE_STUDY}')
        self.browser.find_element(*self.DATE_STUDY).send_keys(date_st)
        self.logger.info(f'Send key {sample_name} to locator {self.SAMPLE_NAME}')
        self.browser.find_element(*self.SAMPLE_NAME).send_keys(sample_name)
        self.logger.info(f'Send key {date_bm} to locator {self.DATE_BIOMATER}')
        self.browser.find_element(*self.DATE_BIOMATER).send_keys(date_bm)
        self.logger.info(f'Send key {ter_sample} to locator {self.TERRITORY_SAMPLE}')
        self.browser.find_element(*self.TERRITORY_SAMPLE).send_keys(ter_sample)
        time.sleep(1)
        self.browser.find_element(*self.TERRITORY_SAMPLE).send_keys(Keys.ENTER)
        self.logger.info(f'Send key {ct} to locator {self.CT}')
        self.browser.find_element(*self.CT).send_keys(ct)
        self.logger.info(f'Send key {age} to locator {self.AGE_PATIENT}')
        self.browser.find_element(*self.AGE_PATIENT).send_keys(age)
        self.logger.info(f'Send key {author}to locator {self.AUTHORS}')
        self.browser.find_element(*self.AUTHORS).send_keys(author)
        self.logger.info(f'Click to import file for seq using {self.IMPORT_FILE} button')
        file_path = os.path.abspath("test_files/566431.fasta")
        self.logger.info(f'Uploading file {file_path}')
        self.browser.find_element(*self.IMPORT_FILE).send_keys(file_path)
        time.sleep(2)
        self.logger.info(f'Click to using {self.BUTTON_SAVE} button')
        self.browser.find_element(*self.BUTTON_SAVE).click()

    @allure.step('Переход на список сиквенсов')
    def grid_sequence(self):
        self.is_present(PathogenCovidSequence.BUTTON_CONTINUE)
        self.logger.info(f'Click to the button {self.BUTTON_CONTINUE}')
        self.browser.find_element(*self.BUTTON_CONTINUE).click()
        self.logger.info(f'Going to add sequence using {self.SEQUENCES} locator ')
        self.is_present(PathogenCovidSequence.SEQUENCES)
        self.browser.find_element(*self.SEQUENCES).click()
        self.logger.info(f'Check info using {self.GRID_SEQ} locator')
        self.browser.find_element(*self.GRID_SEQ).click()

    @allure.step('Проверка полей сиквенса')
    def check_seq_placeholders(self):
        self.is_present(PathogenCovidSequence.BUTTON_INFO)
        self.logger.info(f'Click to the using{self.BUTTON_INFO} button ')
        self.browser.find_element(*self.BUTTON_INFO).click()
    @allure.step('Полное меню работы с сиквенсом')
    def all_edit_menu(self):
        self.is_present(PathogenCovidSequence.ALL_EDIT)
        self.logger.info(f'Click to the menu edit to sequence using {self.ALL_EDIT} locator')
        self.browser.find_element(*self.ALL_EDIT).click()

    @allure.step('Нажатие на "Редактировать" сиквенс')
    def check_button_edit_seq(self, edit_seq_name):
        self.logger.info(f'Click to the edit button using{self.EDIT_BUTTON} locator')
        self.browser.find_element(*self.EDIT_BUTTON).click()
        self.is_present(PathogenCovidSequence.EDIT_SEQ_NAME)
        self.logger.info(f'Click to the name using {self.EDIT_SEQ_NAME} locator')
        self.browser.find_element(*self.EDIT_SEQ_NAME).send_keys(edit_seq_name)
        time.sleep(2)
        self.logger.info(f'Click to using {self.EDIT_BUTTON_SAVE} button')
        self.browser.find_element(*self.EDIT_BUTTON_SAVE).click()
        self.is_present(PathogenCovidSequence.EDIT_BUTTON_CONTINUE)
        self.logger.info(f'Click to the button {self.EDIT_BUTTON_CONTINUE}')
        self.browser.find_element(*self.EDIT_BUTTON_CONTINUE).click()


    @allure.step('Нажать на кнопку "Копировать" сиквенс')
    def check_button_copy_seq(self):
        self.is_present(PathogenCovidSequence.COPY_SEQ)
        self.logger.info(f'Click to the copy using {self.COPY_SEQ} button')
        self.browser.find_element(*self.COPY_SEQ).click()
        time.sleep(2)
        file_path = os.path.abspath("test_files/566431.fasta")
        self.logger.info(f'Uploading file {file_path}')
        self.browser.find_element(*self.EDIT_IMPORT_FILE).send_keys(file_path)
        time.sleep(1)
        self.logger.info(f'Click to {self.EDIT_BUTTON_SAVE} this sequence')
        self.browser.find_element(*self.EDIT_BUTTON_SAVE).click()





