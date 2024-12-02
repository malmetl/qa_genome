import requests
import logging
import allure
from requests.auth import HTTPBasicAuth

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AuthTokenPage:
    def __init__(self):
        self.url = 'https://genomepre.crie.ru/form/upload-sequence?pathogen_type_id=1'
        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self.data = {
            "sequence_name": "SequenceName",
            "method_ready_lib": "Artic",
            "author": "Ivanov",
            "seq_area": "1",
            "gisaid_id": "EPI_ISL_1234567",
            "sequencing_date": "2023-04-04",
            "tech": "2",
            "sample_number": "crie1SM346533",
            "comment": "Дополнительная информация",
            "sequence": [
                ">fasta-content-fasta-content-fasta-content-fasta-content-fasta-content-fasta-content"
            ]
        }

    @allure.step("Sending request with token: {token}")
    def send_request(self, token=None):
        if token:
            self.headers['Authorization'] = token
        logger.info(f"Sending request with token: {token}")
        response = requests.post(self.url, headers=self.headers, json=self.data)
        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response body: {response.text}")
        return response

    @staticmethod
    def get_test_data():
        return [
            (
                'valid_token', 200,
                'Bearer b8a58b7999ae944f3bd1fd1781442fb14433504ff6fd648493c4d0c780514944',
                'Expected status code 200, but got {response.status_code}',
                'Response body is empty'
            ),
            (
                'invalid_token', 401,
                'Bearer invalid_token',
                'Expected status code 401, but got {response.status_code}',
                'Response body does not contain error message'
            ),
            (
                'no_token', 401,
                None,
                'Expected status code 401, but got {response.status_code}',
                'Response body does not contain error message'
            ),
            (
                'expired_token', 401,
                0,
                'Expected status code 401, but got {response.status_code}',
                'Response body does not contain error message'
            ),
            (
                'wrong_token_type', 401,
                'Token b8a58b7999ae944f3bd1fd1781442fb14433504ff6fd648493c4d0c780514944',
                'Expected status code 401, but got {response.status_code}',
                'Response body does not contain error message'
            )
        ]


class DictionaryPage:
    def __init__(self):
        self.base_url = 'https://genomepre.crie.ru/api/v1/import/dictionary'
        self.headers = {
            'accept': 'application/json'
        }
        self.auth = HTTPBasicAuth('crie_kurochkin', '2CZSudsG')

    @allure.step("Sending GET request with pathogen_type_id: {pathogen_type_id}")
    def send_request(self, pathogen_type_id):
        url = f"{self.base_url}?pathogen_type_id={pathogen_type_id}"
        logger.info(f"Sending GET request to {url}")
        response = requests.get(url, headers=self.headers, auth=self.auth)
        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response body: {response.text}")
        return response

    @staticmethod
    def get_test_data_dictionary():
        return [
            (1, 200, 'Expected status code 200, but got {response.status_code}'),
            (0, 500, 'Expected status code 400, but got {response.status_code}'),
            (54, 200, 'Expected status code 200, but got {response.status_code}'),
            (55, 500, 'Expected status code 400, but got {response.status_code}'),
            (27, 200, 'Expected status code 200, but got {response.status_code}')
        ]

class PackagePage:
    def __init__(self):
        self.base_url = 'https://genomepre.crie.ru/api/v1/import/package'
        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self.auth = HTTPBasicAuth('crie_kurochkin', '2CZSudsG')
        self.data = [
            {
                "sample_data": {
                    "sample_name": "sample_name",
                    "sequence_name": "sequence_name",
                    "sequencing_date": "2023-01-01",
                    "biomater": 0,
                    "sample_pick_place": "Россия, г Москва",
                    "sample_id": "123456-123-12",
                    "sample_pick_date": "2023-01-01",
                    "patient_gender": 0,
                    "patient_age": 23,
                    "patient_social_status": "Медицинский работник",
                    "pcr": 20,
                    "foreign": 1,
                    "foreign_income": "2023-01-01",
                    "foreign_place": "Турция",
                    "sick_date": "2023-01-01",
                    "sick_diagnosis": "B34.2",
                    "sick_form": 1,
                    "sick_symptoms": "Пневмония средней тяжести",
                    "issue": 1,
                    "hospitalization": 1,
                    "double_sick": 0,
                    "all_value": 20,
                    "pathogen_value": 10,
                    "pathogen_same_value": 5,
                    "pathogen_numbers_value": "5",
                    "infection_source": "Жена",
                    "test_system": "biocredit",
                    "tech": 0,
                    "method_ready_lib": "Artic",
                    "genom_pick_method": "SPAdes 3.14",
                    "average_cover": 50,
                    "sample_type": 0,
                    "seq_area": 0,
                    "author": "Ivanov Sidorov",
                    "gisaid_id": "EPI_ISL_1234567",
                    "comment": "comment test",
                    "vaccine": [
                        {
                            "vaccine_id": 1,
                            "date": "2022-01-01",
                            "order": 230
                        },
                        {
                            "vaccine_id": 1,
                            "date": "2022-04-02",
                            "order": 240
                        }
                    ]
                },
                "sequence": [
                    ">fasta-content-fasta-content-fasta-content-fasta-content-fasta-content-fasta-content-fasta-content-fasta-content"
                ]
            }
        ]

    @allure.step("Sending POST request with pathogen_type_id: {pathogen_type_id}")
    def send_request(self, pathogen_type_id):
        url = f"{self.base_url}?pathogen_type_id={pathogen_type_id}"
        logger.info(f"Sending POST request to {url}")
        response = requests.post(url, headers=self.headers, json=self.data, auth=self.auth)
        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response body: {response.text}")
        return response

    def set_invalid_seq_area(self):
        self.data[0]["sample_data"]["seq_area"] = 2

    def remove_required_field(self, field_name):
        del self.data[0]["sample_data"][field_name]

    def set_invalid_patient_gender(self):
        self.data[0]["sample_data"]["patient_gender"] = 2

    def remove_sample_pick_date(self):
        del self.data[0]["sample_data"]["sample_pick_date"]