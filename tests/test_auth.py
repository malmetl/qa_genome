from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from PageObject.BasePages import basepage
from selenium.webdriver.common.by import By
import time
import allure
from PageObject.UserPage import AuthPage
import pytest


@allure.feature('Authorization Page')
@allure.title('Авторизация с верными данными')
def test_authorization(browser, base_url):
    basepage(browser).get_open_auth_page(base_url)
    AuthPage(browser).get_login('crie_kurochkin', '2CZSudsG', 'af042a44-b8d5-4c96-8f19-3a28e8a667b4')
    response = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="user"]/div/button/h3')))
    assert 'crie_kurochkin' in response.text


@allure.feature('Authorization Page')
@allure.title('Авторизация с ошибочными данными')
def test_bad_authorization(browser, base_url):
    basepage(browser).get_open_auth_page(base_url)
    AuthPage(browser).get_bad_login()
    response = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/section/div/div/div[1]/div[1]/div/form/div[3]/div/div[2]/div/span')))
    assert 'Введенные символы должны совпадать с символами на картинке' in response.text


