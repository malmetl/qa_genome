import json
import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
import logging
from PageObject.SarsCoV.API import AuthTokenPage
from PageObject.SarsCoV.API import DictionaryPage
from PageObject.SarsCoV.API import PackagePage
logging.basicConfig(level=logging.INFO)


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to use (chrome or firefox)")
    parser.addoption("--base_url", action="store", default="https://genomepre-frontend.crie.ru/new/app/main",
                     help="Base URL for the application")
    parser.addoption("--executor", action="store", default="127.0.0.1", help="Selenoid executor host")
    parser.addoption("--vnc", action="store_true", help="Enable VNC for Selenoid")
    parser.addoption("--logs", action="store_true", help="Enable Selenoid logs")
    parser.addoption("--bv", action="store", help="Browser version")
    parser.addoption("--headless", action="store_true", help="Run browser in headless mode")


@pytest.fixture
def browser(request):
    browser_name = request.config.getoption("--browser")
    executor = request.config.getoption("--executor")
    vnc = request.config.getoption("--vnc")
    logs = request.config.getoption("--logs")
    version = request.config.getoption("--bv")
    headless = request.config.getoption("--headless")
    base_url = request.config.getoption("--base_url")

    executor_url = f"http://{executor}:4444/wd/hub"
    logging.info(f"Starting browser: {browser_name} on {executor_url}")

    if browser_name == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
    elif browser_name == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    capabilities = {
        "browserName": browser_name,
        "browserVersion": version,
        "selenoid:options": {
            "enableVNC": True,
            "enableLog": logs,
            "name": request.node.name,
            "screenResolution": "3920x1080",
        },
        "acceptInsecureCerts": True,
    }

    for k, v in capabilities.items():
        options.set_capability(k, v)

    driver = webdriver.Remote(
        command_executor=executor_url,
        options=options
    )

    allure.attach(
        name="Browser Capabilities",
        body=json.dumps(driver.capabilities, indent=4, ensure_ascii=False),
        attachment_type=allure.attachment_type.JSON
    )

    driver.test_name = request.node.name
    driver.base_url = base_url
    driver.log_level = logging.DEBUG

    yield driver
    driver.quit()
    logging.info(f"Closed browser: {browser_name}")


@pytest.fixture(params=AuthTokenPage.get_test_data(), ids=[data[0] for data in AuthTokenPage.get_test_data()])
def test_data(request):
    return request.param
@pytest.fixture(params=DictionaryPage.get_test_data_dictionary(), ids=[f"pathogen_type_id={data[0]}" for data in DictionaryPage.get_test_data_dictionary()])
def test_data_dictionary(request):
    return request.param

@pytest.fixture
def base_url(request):
    return request.config.getoption("--base_url")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    if rep.when == "call" and rep.failed:
        try:
            driver = item.funcargs['browser']
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            logging.error(f"Failed to take screenshot: {e}")
