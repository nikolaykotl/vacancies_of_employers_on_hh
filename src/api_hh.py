import requests
class Api_hh():
    base_url = f"https://api.hh.ru/"
    def __init__(self, employers_id):
        self.employers_id = employers_id
        self.params = {
        "page": 1,
        "per_page": 20,
        "archived": False
        }

    def get_vacancies(self):
        """Получаем вакансии"""
        vacancies = []
        for employer_id in self.employers_id:
            url_vac_emp = self.base_url+f'vacancies?employer_id={employer_id}'
            response = requests.get(url_vac_emp, self.params)
            if response.status_code != 200:
                raise print(f"Ошибка! Статус {response.status_code}")
            else:
                vacancies_emp = response.json()
                for i in range(len(vacancies_emp['items'])):
                     vacancies_data = {'employer_id': employer_id,
                                       'vacancy_name': vacancies_emp['items'][i]['name'],
                                       'salary_from': vacancies_emp['items'][i]['salary']['from'] if vacancies_emp['items'][i]['salary'] and vacancies_emp['items'][i]['salary']['from'] != 0 else None,
                                       'salary_to': vacancies_emp['items'][i]['salary']['to'] if vacancies_emp['items'][i]['salary'] and vacancies_emp['items'][i]['salary']['to'] != 0 else None,
                                       'currency': vacancies_emp['items'][i]['salary']['currency'] if vacancies_emp['items'][i]['salary'] and vacancies_emp['items'][i]['salary']['currency'] != 0 else None,
                                       'url': vacancies_emp['items'][i]['alternate_url']
                                       }
                     vacancies.append(vacancies_data)
        return vacancies

    def get_employers(self):
        employers = []
        for employer_id in self.employers_id:
            url_emp = self.base_url + f'employers/{employer_id}'
            response = requests.get(url_emp)
            if response.status_code != 200:
                raise print(f"Ошибка! Статус {response.status_code}")
            else:
                employer = response.json()
                employer_data = {'employer_id' : employer_id,
                                 'employer_name' : employer['name'],
                                 'employer_site_url':employer['site_url'] if employer['site_url'] != '' else None,
                                 'city': employer['area']['name'],
                                 'industries_name': employer['industries'][0]['name'] if employer['industries'] != [] else None
                                 }
            employers.append(employer_data)
        return employers