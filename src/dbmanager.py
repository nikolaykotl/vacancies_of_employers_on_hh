#import psycopg2
from src.function import connection
class DBManager():
    def __init__(self, database, password):
        self.database = database
        self.password = password

    def convert_to_str(self, value, return_value):
        """Конвертация вывода при значении в базе данных None(Null)"""
        if value is None:
            return f'{return_value}'
        else:
            return value

    def get_companies_and_vacancies(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        result = []
        with connection(self.database, self.password) as conn:
             with conn.cursor() as cur:
                cur.execute('select employer_name, count(vacancies.vacancy_name) from employers '
                            'full join vacancies using(employer_id) '
                            'group by employer_name')
                rows = cur.fetchall()

                for row in rows:
                    company_name, vacancies_count = row
                    result.append({'Компания': company_name, 'Количество вакансий': vacancies_count})
        return result

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию"""
        result = []
        with connection(self.database, self.password) as conn:
            with conn.cursor() as cur:
                cur.execute('select employers.employer_name, vacancy_name, salary_from, salary_to, currency, url '
                            'from vacancies '
                            'full join employers using(employer_id)')
                rows = cur.fetchall()

                for row in rows:
                    company_name = row[0]
                    vac = self.convert_to_str(row[1], 'Нет вакансий')
                    salary_from = self.convert_to_str(row[2], 'н/д')
                    salary_to = self.convert_to_str(row[3], 'н/д')
                    currency = self.convert_to_str(row[4], '')
                    site = self.convert_to_str(row[5], '-')
                    result.append({'Компания': company_name, 'Вакансия': vac, 'Зарплата от': salary_from, 'Зарплата до': salary_to, 'Валюта': currency, 'Ссылка на вакансию': site})
        return result

    def get_avg_salary(self):
        """ Получает среднюю зарплату по вакансиям"""

        with connection(self.database, self.password) as conn:
            with conn.cursor() as cur:
                cur.execute(f"select avg((salary_from+salary_to) / 2) from vacancies where currency = 'RUR'")
                row = cur.fetchone()
                avg_salary = round(row[0],2)
        return f'{avg_salary} RUR'

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        result = []
        with connection(self.database, self.password) as conn:
            with conn.cursor() as cur:
                cur.execute(f"select vacancy_name, salary_from, salary_to, currency, url  from vacancies where ((salary_from+salary_to) / 2) > (select avg((salary_from+salary_to) / 2) from vacancies where currency = 'RUR')")
                rows = cur.fetchall()

                for row in rows:
                    vac = self.convert_to_str(row[0], 'Нет вакансий')
                    salary_from = self.convert_to_str(row[1], 'н/д')
                    salary_to = self.convert_to_str(row[2], 'н/д')
                    currency = self.convert_to_str(row[3], '')
                    site = self.convert_to_str(row[4], '-')
                    result.append({'Вакансия': vac, 'Зарплата от': salary_from,
                                   'Зарплата до': salary_to, 'Валюта': currency, 'Ссылка на вакансию': site})
        return result

    def get_vacancies_with_keyword(self):
        """Получает список всех вакансий, в названии которых есть переданные в метод слова"""
        result = []
        user_input = input('Введите ключевое слово, для поиска в названии вакансии: ')
        title_input = user_input.title()
        lower_input = user_input.lower()
        with connection(self.database, self.password) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"select vacancy_name, salary_from, salary_to, currency, url"
                    f" from vacancies where vacancy_name like '%{title_input}%' or vacancy_name like '%{lower_input}%'")
                rows = cur.fetchall()

                for row in rows:
                    vac = self.convert_to_str(row[0], 'Нет вакансий')
                    salary_from = self.convert_to_str(row[1], 'н/д')
                    salary_to = self.convert_to_str(row[2], 'н/д')
                    currency = self.convert_to_str(row[3], '')
                    site = self.convert_to_str(row[4], '-')
                    result.append({'Вакансия': vac, 'Зарплата от': salary_from,
                                   'Зарплата до': salary_to, 'Валюта': currency, 'Ссылка на вакансию': site})
        return result
