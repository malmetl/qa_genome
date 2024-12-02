from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from PageObject.BasePages import basepage
from selenium.webdriver.support import expected_conditions as EC
import allure
from faker import Faker
import json
import time


@allure.title('Авторизация')
class AuthPage(basepage):
    LOGIN_INPUT = By.XPATH, '//*[@id="app"]/div/div/section/div/div/div[1]/div[1]/div/form/div[1]/div[1]/div[2]/div/div[1]/input'
    PASSWORD_INPUT = By.XPATH, '//*[@id="app"]/div/div/section/div/div/div[1]/div[1]/div/form/div[2]/div[1]/div[2]/div/div[1]/input'
    SUMBIT_LOGIN_BUTTON = By.XPATH, '//*[@id="app"]/div/div/section/div/div/div[1]/div[1]/div/form/div[4]/button/span'
    CODE_IMAGE = By.ID, 'captcha-input'

    def __init__(self, browser):
        super().__init__(browser)
        self.fake = Faker()

    @allure.step("Заполнение формы входа")
    def get_login(self, username, password, code):
        self.logger.info(f'Send key "{username}" using locator  {self.LOGIN_INPUT}')
        self.browser.find_element(*self.LOGIN_INPUT).send_keys(username)
        self.logger.info(f'Send key "{password}" using locator  {self.PASSWORD_INPUT}')
        self.browser.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.logger.info(f'Send key "{code}" using locator {self.CODE_IMAGE}')
        self.browser.find_element(*self.CODE_IMAGE).send_keys(code)
        self.logger.info(f'Click button using locator {self.SUMBIT_LOGIN_BUTTON}')
        self.browser.find_element(*self.SUMBIT_LOGIN_BUTTON).click()

    @allure.step('Ошибочное заполнение формы входа')
    def get_bad_login(self):
        username_fake = self.fake.user_name()
        password_fake = self.fake.password()
        code_fake = self.fake.bothify(text='MPN-#####')
        time.sleep(3)
        with allure.step(f'Заполнение поля "Username" значением "{username_fake}"'):
            self.logger.info(f'Send key "{username_fake}" using locator  {self.LOGIN_INPUT}')
            self.browser.find_element(*self.LOGIN_INPUT).send_keys(username_fake)
        with allure.step(f'Заполнение поля "Password" значением "{password_fake}"'):
            self.logger.info(f'Send key "{password_fake}" using locator  {self.PASSWORD_INPUT}')
            self.browser.find_element(*self.PASSWORD_INPUT).send_keys(password_fake)
        with allure.step(f'Заполнение поля "Code" значением "{code_fake}"'):
            self.logger.info(f'Send key "{code_fake}" using locator {self.CODE_IMAGE}')
            self.browser.find_element(*self.CODE_IMAGE).send_keys(code_fake)
        with allure.step('Нажатие кнопки отправки формы'):
            self.logger.info(f'Click button using locator {self.SUMBIT_LOGIN_BUTTON}')
            self.browser.find_element(*self.SUMBIT_LOGIN_BUTTON).click()



