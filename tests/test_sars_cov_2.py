from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from PageObject.BasePages import basepage
from selenium.webdriver.common.by import By
import time
import allure
from PageObject.UserPage import AuthPage
import pytest
from PageObject.SarsCoV.sequence import PathogenCovidSequence
from PageObject.SarsCoV.Sample import PathogenCovidSample
from PageObject.SarsCoV.API import AuthTokenPage
from PageObject.SarsCoV.API import DictionaryPage
from PageObject.SarsCoV.API import PackagePage

@pytest.mark.parametrize('username, password, code, pathogenName',
                         [('crie_kurochkin', '2CZSudsG', 'af042a44-b8d5-4c96-8f19-3a28e8a667b4', 'Sars')])
@allure.feature('Патоген Sars-CoV-2')
@allure.title('Переход на страницу SarsCoV-2')
def test_open_pathogen_sars_cov_2(browser, base_url, username, password, code, pathogenName):
    basepage(browser).get_open_auth_page(base_url)
    basepage(browser).is_present(AuthPage(browser).LOGIN_INPUT)
    AuthPage(browser).get_login(username, password, code)
    basepage(browser).is_present(basepage(browser).waiting)
    basepage(browser).search_sars_cov_2(pathogenName)
    pathogen_name = browser.find_element(By.XPATH, '//*[@id="app"]/div/div/header/div[2]/div[1]/div[2]/p')
    assert 'SARS-CoV-2' in pathogen_name.text


@pytest.mark.parametrize(
    'username, password, code, pathogenName, seq_name, date_st, sample_name, date_bm, ter_sample, ct, age, author',
    [('crie_kurochkin', '2CZSudsG', 'af042a44-b8d5-4c96-8f19-3a28e8a667b4', 'Sars', 'test_sequence', '25052023',
      'test_sample', '25052023', 'Moscow', '26', '25', 'test_author')])
@allure.feature('Патоген Sars-CoV-2')
@allure.title('Заполнение сиквенса по обязательным полям')
def test_add_seq(browser, base_url, username, password, code, pathogenName, seq_name, date_st, sample_name, date_bm,
                 ter_sample, ct, age, author):
    basepage(browser).get_open_auth_page(base_url)
    basepage(browser).is_present(AuthPage(browser).LOGIN_INPUT)
    AuthPage(browser).get_login(username, password, code)
    basepage(browser).is_present(basepage(browser).waiting)
    basepage(browser).search_sars_cov_2(pathogenName)
    basepage(browser).is_present(PathogenCovidSequence.SEQUENCES)
    PathogenCovidSequence(browser).go_to_add_seq()
    PathogenCovidSequence(browser).add_info_placeholders(seq_name, date_st, sample_name, date_bm, ter_sample, ct, age,
                                                         author)
    element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/p/h3')))
    assert 'Сиквенс успешно создан' in element.text


@pytest.mark.parametrize(
    'username, password, code, pathogenName, seq_name, date_st, sample_name, date_bm, ter_sample, ct, age, author',
    [('crie_kurochkin', '2CZSudsG', 'af042a44-b8d5-4c96-8f19-3a28e8a667b4', 'Sars', 'test_sequence', '25052023',
      'test_sample', '25052023', 'Moscow', '26', '25', 'test_author')])
@allure.feature('Патоген Sars-CoV-2')
@allure.title('Проверка заполненых у сиквенса')
def test_check_seq_info(browser, base_url, username, password, code, pathogenName, seq_name, date_st, sample_name,
                        date_bm, ter_sample, ct, age, author):
    basepage(browser).get_open_auth_page(base_url)
    basepage(browser).is_present(AuthPage(browser).LOGIN_INPUT)
    AuthPage(browser).get_login(username, password, code)
    basepage(browser).is_present(basepage(browser).waiting)
    basepage(browser).search_sars_cov_2(pathogenName)
    basepage(browser).is_present(PathogenCovidSequence.SEQUENCES)
    PathogenCovidSequence(browser).go_to_add_seq()
    PathogenCovidSequence(browser).add_info_placeholders(seq_name, date_st, sample_name, date_bm, ter_sample, ct, age,
                                                         author)
    PathogenCovidSequence(browser).grid_sequence()
    PathogenCovidSequence(browser).check_seq_placeholders()
    response = WebDriverWait(browser, 10).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="app"]/div/div/section/div/div[6]/div/div/div[1]/div[2]/div[1]/div/div[1]/p')))
    assert 'test_sequence' in response.text


@pytest.mark.parametrize('username, password, code, pathogenName, sample_name, date_bm, ter_sample, ct, age',
                         [('crie_kurochkin', '2CZSudsG', 'af042a44-b8d5-4c96-8f19-3a28e8a667b4', 'Sars', 'test_sample',
                           '25052023', 'Moscow', '25', '27')])
@allure.feature('Патоген Sars-CoV-2')
@allure.title('Заполнение обязательных полей у образца')
def test_add_sample(browser, base_url, username, password, code, pathogenName, sample_name, date_bm, ter_sample, ct,
                    age):
    basepage(browser).get_open_auth_page(base_url)
    basepage(browser).is_present(AuthPage(browser).LOGIN_INPUT)
    AuthPage(browser).get_login(username, password, code)
    basepage(browser).is_present(basepage(browser).waiting)
    basepage(browser).search_sars_cov_2(pathogenName)
    basepage(browser).is_present(PathogenCovidSample.SAMPLES)
    PathogenCovidSample(browser).go_to_sample()
    PathogenCovidSample(browser).add_info_placeholders_for_sample(sample_name, date_bm, ter_sample, ct, age)
    response = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/p/h3')))
    assert 'Образец успешно создан' in response.text


@pytest.mark.parametrize('username, password, code, pathogenName, sample_name, date_bm, ter_sample, ct, age',
                         [('crie_kurochkin', '2CZSudsG', 'af042a44-b8d5-4c96-8f19-3a28e8a667b4', 'Sars', 'test_sample',
                           '25052023', 'Moscow', '25', '27')])
@allure.feature('Патоген Sars-CoV-2')
@allure.title('Проверка заполненных полей у образца')
def test_check_sample_info(browser, base_url, username, password, code, pathogenName, sample_name, date_bm, ter_sample,
                           ct, age):
    basepage(browser).get_open_auth_page(base_url)
    basepage(browser).is_present(AuthPage(browser).LOGIN_INPUT)
    AuthPage(browser).get_login(username, password, code)
    basepage(browser).is_present(basepage(browser).waiting)
    basepage(browser).search_sars_cov_2(pathogenName)
    basepage(browser).is_present(PathogenCovidSample.SAMPLES)
    PathogenCovidSample(browser).go_to_sample()
    PathogenCovidSample(browser).add_info_placeholders_for_sample(sample_name, date_bm, ter_sample, ct, age)
    PathogenCovidSample(browser).grid_samples()
    PathogenCovidSample(browser).check_sample_placeholders()
    time.sleep(5)
    response = WebDriverWait(browser, 10).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="app"]/div/div/section/div/div[6]/div/div/div[1]/div[2]/div[1]/div/div[1]/p')))
    assert 'test_sample' in response.text


@pytest.mark.parametrize(
    'username, password, code, pathogenName, seq_name, date_st, sample_name, date_bm, ter_sample, ct, age, author,  edit_seq_name',
    [('crie_kurochkin', '2CZSudsG', 'af042a44-b8d5-4c96-8f19-3a28e8a667b4', 'Sars', 'test_sequence', '25052023',
      'test_sample', '25052023', 'Moscow', '26', '25', 'test_author', '_edit_v1')])
@allure.feature('Патоген Sars-CoV-2')
@allure.title('Проверка кнопки "Редактирования" сиквенс')
def test_edit_button_seq(browser, base_url, username, password, code, pathogenName, seq_name, date_st, sample_name,
                         date_bm, ter_sample, ct, age, author, edit_seq_name):
    basepage(browser).get_open_auth_page(base_url)
    basepage(browser).is_present(AuthPage(browser).LOGIN_INPUT)
    AuthPage(browser).get_login(username, password, code)
    basepage(browser).is_present(basepage(browser).waiting)
    basepage(browser).search_sars_cov_2(pathogenName)
    basepage(browser).is_present(PathogenCovidSequence.SEQUENCES)
    PathogenCovidSequence(browser).go_to_add_seq()
    PathogenCovidSequence(browser).add_info_placeholders(seq_name, date_st, sample_name, date_bm, ter_sample, ct, age,
                                                         author)
    PathogenCovidSequence(browser).grid_sequence()
    PathogenCovidSequence(browser).all_edit_menu()
    PathogenCovidSequence(browser).check_button_edit_seq(edit_seq_name)
    PathogenCovidSequence(browser).check_seq_placeholders()
    response = WebDriverWait(browser, 10).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="app"]/div/div/section/div/div[6]/div/div/div[1]/div[2]/div[1]/div/div[1]/p')))
    assert 'test_sequence_edit_v1' in response.text


@pytest.mark.parametrize('username, password, code, pathogenName',
                         [('crie_kurochkin', '2CZSudsG', 'af042a44-b8d5-4c96-8f19-3a28e8a667b4', 'Sars')])
@allure.feature('Патоген Sars-CoV-2')
@allure.title('Проверка кнопки "Копировать" сиквенс')
def test_copy_button_seq(browser, base_url, username, password, code, pathogenName):
    basepage(browser).get_open_auth_page(base_url)
    basepage(browser).is_present(AuthPage(browser).LOGIN_INPUT)
    AuthPage(browser).get_login(username, password, code)
    basepage(browser).is_present(basepage(browser).waiting)
    basepage(browser).search_sars_cov_2(pathogenName)
    basepage(browser).is_present(PathogenCovidSequence.SEQUENCES)
    PathogenCovidSequence(browser).all_edit_menu()
    PathogenCovidSequence(browser).check_button_copy_seq()
    SeqOrig = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.sequences-list-item__field-wrapper p')))
    SeqCopy = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.sequences-list-item__field-wrapper p')))
    assert SeqCopy == SeqOrig


@pytest.mark.parametrize('username, password, code, pathogenName',
                         [('crie_kurochkin', '2CZSudsG', 'af042a44-b8d5-4c96-8f19-3a28e8a667b4', 'Sars')])
@allure.feature('Патоген Sars-CoV-2')
@allure.title('Проверка кнопки "Инструкция"')
def test_instruction_page(browser, base_url, username, password, code, pathogenName):
    basepage(browser).get_open_auth_page(base_url)
    basepage(browser).is_present(AuthPage(browser).LOGIN_INPUT)
    AuthPage(browser).get_login(username, password, code)
    basepage(browser).is_present(basepage(browser).waiting)
    basepage(browser).search_sars_cov_2(pathogenName)
    basepage(browser).check_instruction()
    Instruction_1 = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/section/div/ul/li[1]/button')))
    Instruction_2 = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/section/div/ul/li[2]/button')))
    Instruction_3 = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/section/div/ul/li[3]/button')))
    Instruction_4 = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/section/div/ul/li[4]/button')))
    Instruction_5 = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/section/div/ul/li[5]/button')))
    Instruction_6 = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/section/div/ul/li[6]/button')))
    assert 'Пример пакетной загрузки SARS-CoV-2' in Instruction_1.text
    assert 'Инструкция по работе с SARS-CoV-2' in Instruction_2.text
    assert 'Инструкция Genome' in Instruction_3.text
    assert 'Инструкция Genome для роли "Образцы"' in Instruction_4.text
    assert 'Инструкция Genome API' in Instruction_5.text
    assert 'Инструкция загрузка через Excel' in Instruction_6.text


@allure.feature("Auth Token Tests")
@allure.story("Тестирование различных сценариев токена на API 'Upload sequence'")
@allure.title('Проверка API Upload_sequence на токен"')
def test_auth_token(test_data):
    test_name, expected_status_code, token, status_code_message, body_message = test_data
    with allure.step(f"Running test: {test_name}"):
        auth_token_page = AuthTokenPage()
        response = auth_token_page.send_request(token)

        with allure.step(f"Asserting status code: {expected_status_code}"):
            assert response.status_code == expected_status_code, status_code_message.format(response=response)

        if expected_status_code == 200:
            with allure.step("Asserting response body is not empty"):
                assert response.json() is not None, body_message
        elif expected_status_code == 401:
            pass


@allure.feature("Upload Sequence API")
@allure.story("Успешная загрузка сиквенса")
@allure.title('Проверка успешного загрузки API Upload_seq"')
def test_successful_sequence_upload():
    auth_token_page = AuthTokenPage()
    with allure.step("Отправка запроса для загрузки сиквенса"):
        with allure.step(f"Request body: {auth_token_page.data}"):
            response = auth_token_page.send_request('Bearer b8a58b7999ae944f3bd1fd1781442fb14433504ff6fd648493c4d0c780514944')

    with allure.step("Статус кода"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    with allure.step("Asserting response body"):
        assert response.json() is not None, "Response body is empty"

@allure.feature("Upload Sequence API")
@allure.story("Задублированный sample number")
@allure.title('Проверка загрузки задублированного sample_number на API Upload_seq')
def test_duplicate_sample_number():
    auth_token_page = AuthTokenPage()
    auth_token_page.data['sample_number'] = "crie1SM346533"
    with allure.step("Sending request to upload sequence"):
        with allure.step(f"Request body: {auth_token_page.data}"):
            response = auth_token_page.send_request('Bearer b8a58b7999ae944f3bd1fd1781442fb14433504ff6fd648493c4d0c780514944')

    with allure.step("Asserting status code"):
        assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"

    with allure.step("Asserting error message"):
        assert "Sequence: Sequence already exists!." in response.text, "Expected error message not found"

@allure.feature("Upload Sequence API")
@allure.story("Ошибка невалидный seq_area")
@allure.title('Проверка невалидного seq_area на API Upload_seq')
def test_invalid_seq_area():
    auth_token_page = AuthTokenPage()
    auth_token_page.data['seq_area'] = "2"
    with allure.step("Sending request to upload sequence"):
        with allure.step(f"Request body: {auth_token_page.data}"):
            response = auth_token_page.send_request('Bearer b8a58b7999ae944f3bd1fd1781442fb14433504ff6fd648493c4d0c780514944')

    with allure.step("Asserting status code"):
        assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"


@allure.feature("Upload Sequence API")
@allure.story("Ошибка в валидации формата даты")
@allure.title('Проверка невалидной даты на API Upload_seq')
def test_invalid_sequencing_date_format():
    auth_token_page = AuthTokenPage()
    auth_token_page.data['sequencing_date'] = "2023/04/04"
    with allure.step("Sending request to upload sequence"):
        with allure.step(f"Request body: {auth_token_page.data}"):
            response = auth_token_page.send_request('Bearer b8a58b7999ae944f3bd1fd1781442fb14433504ff6fd648493c4d0c780514944')

    with allure.step("Asserting status code"):
        assert response.status_code ==  400, f"Expected status code 400, but got {response.status_code}"


@allure.feature("Upload Sequence API")
@allure.story("Ошибка в теле функции не указан sample_number")
@allure.title('Проверка отправки тела функции  на API Upload_seq без sample_number')
def test_missing_required_field():
    auth_token_page = AuthTokenPage()
    del auth_token_page.data['sample_number']
    with allure.step("Sending request to upload sequence"):
        with allure.step(f"Request body: {auth_token_page.data}"):
            response = auth_token_page.send_request('Bearer b8a58b7999ae944f3bd1fd1781442fb14433504ff6fd648493c4d0c780514944')

    with allure.step("Asserting status code"):
        assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"


@allure.feature("Dictionary API Tests")
@allure.story("Разные сценарии с pathogen_type_id в Dictionary API")
@allure.title('Проверка pathogen_type_id в API Dictionary')
def test_dictionary(test_data_dictionary):
    pathogen_type_id, expected_status_code, status_code_message = test_data_dictionary
    with allure.step(f"Running test with pathogen_type_id: {pathogen_type_id}"):
        dictionary_page = DictionaryPage()

        with allure.step(f"Отпарвка GET запроса с pathogen_type_id: {pathogen_type_id}"):
            response = dictionary_page.send_request(pathogen_type_id)

        with allure.step(f"Asserting status code: {expected_status_code}"):
            assert response.status_code == expected_status_code, status_code_message.format(response=response)

        with allure.step("Asserting response body is not empty"):
            assert response.json() is not None, "Response body is empty"


@allure.feature("Package API Tests")
@allure.story("Проверка различных сценариев API с pathogen_type_id")
@allure.title('Проверка удачной загрузки package')
def test_successful_package_upload():
    package_page = PackagePage()
    with allure.step("Отправка POST запроса с pathogen_type_id: 1"):
        response = package_page.send_request(1)

    with allure.step("Asserting status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    with allure.step("Asserting response body"):
        assert response.json() is not None, "Response body is empty"

@allure.feature("Package API Tests")
@allure.story("Тест на валидность переменной seq_area")
@allure.title('Проверка валидности seq_area в body')
def test_invalid_seq_area():
    package_page = PackagePage()
    package_page.set_invalid_seq_area()
    with allure.step("Отправка POST запроса с pathogen_type_id: 1"):
        response = package_page.send_request(1)

    with allure.step("Asserting status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    with allure.step("Asserting response body"):
        assert response.json() is not None, "Response body is empty"

@allure.feature("Package API Tests")
@allure.story("Отправка запроса без переменной: sample_name")
@allure.title('Проверка валидности переменной sample_name')
def test_missing_sample_name():
    package_page = PackagePage()
    package_page.remove_required_field("sample_name")
    with allure.step("Отправка POST запроса с pathogen_type_id: 1"):
        response = package_page.send_request(1)

    with allure.step("Asserting status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    with allure.step("Asserting response body"):
        assert response.json() is not None, "Response body is empty"

@allure.feature("Package API Tests")
@allure.story("Отправка запроса без переменной: sequence_name")
@allure.title('Проверка валидности переменной sequence_name')
def test_missing_sequence_name():
    package_page = PackagePage()
    package_page.remove_required_field("sequence_name")
    with allure.step("Отправка POST запроса с pathogen_type_id: 1"):
        response = package_page.send_request(1)

    with allure.step("Asserting status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    with allure.step("Asserting response body"):
        assert response.json() is not None, "Response body is empty"

@allure.feature("Package API Tests")
@allure.story("Проверка валидности переменной patient_gender")
@allure.title('Проверка валидности переменной patient_gender')
def test_invalid_patient_gender():
    package_page = PackagePage()
    package_page.set_invalid_patient_gender()
    with allure.step("Отправка POST запроса с pathogen_type_id: 1"):
        response = package_page.send_request(1)

    with allure.step("Asserting status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    with allure.step("Asserting response body"):
        assert response.json() is not None, "Response body is empty"

@allure.feature("Package API Tests")
@allure.story("Отправка запроса без переменной sample_pick_date")
@allure.title('Проверка валидности переменной sample_pick_date')
def test_missing_sample_pick_date():
    package_page = PackagePage()
    package_page.remove_sample_pick_date()
    with allure.step("Отправка POST запроса с pathogen_type_id: 1"):
        response = package_page.send_request(1)

    with allure.step("Asserting status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    with allure.step("Asserting response body"):
        assert response.json() is not None, "Response body is empty"

@allure.feature("Package API Tests")
@allure.story("Проверка валидности переменной sequencing_date на формат")
@allure.title('Проверка валидности переменной sequencing_date')
def test_invalid_sequencing_date_format():
    package_page = PackagePage()
    package_page.data[0]["sample_data"]["sequencing_date"] = "2023/01/01"
    with allure.step("Отправка POST запроса с pathogen_type_id: 1"):
        response = package_page.send_request(1)

    with allure.step("Asserting status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    with allure.step("Asserting response body"):
        assert response.json() is not None, "Response body is empty"

@allure.feature("Package API Tests")
@allure.story("Проверка валидности переменной foreign_income на формат")
@allure.title('Проверка валидности переменной foreign_income')
def test_invalid_foreign_income_format():
    package_page = PackagePage()
    package_page.data[0]["sample_data"]["foreign_income"] = "2023/01/01"
    with allure.step("Отправка POST запроса с pathogen_type_id: 1"):
        response = package_page.send_request(1)

    with allure.step("Asserting status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    with allure.step("Asserting response body"):
        assert response.json() is not None, "Response body is empty"

@allure.feature("Package API Tests")
@allure.story("Проверка валидности переменной sick_date на формат")
@allure.title('Проверка валидности переменной sick_date')
def test_invalid_sick_date_format():
    package_page = PackagePage()
    package_page.data[0]["sample_data"]["sick_date"] = "2023/01/01"
    with allure.step("Отправка POST запроса с pathogen_type_id: 1"):
        response = package_page.send_request(1)

    with allure.step("Asserting status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    with allure.step("Asserting response body"):
        assert response.json() is not None, "Response body is empty"

@allure.feature("Package API Tests")
@allure.story("Проверка валидности переменной vaccine date на формат")
@allure.title('Проверка валидности переменной vaccine date')
def test_invalid_vaccine_date_format():
    package_page = PackagePage()
    package_page.data[0]["sample_data"]["vaccine"][0]["date"] = "2022/01/01"
    with allure.step("Отправка POST запроса с pathogen_type_id: 1"):
        response = package_page.send_request(1)

    with allure.step("Asserting status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    with allure.step("Asserting response body"):
        assert response.json() is not None, "Response body is empty"