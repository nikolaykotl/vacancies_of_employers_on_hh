from src.api_hh import Api_hh
from src.db_maker import Data_base_maker
from src.dbmanager import DBManager

if __name__ == '__main__':
    employers = []
    employers_dict = {
                 'Сбер': '3529',
                 'Яндекс': '1740',
                 'АльфаБанк': '80',
                 'VK': '15478',
                 'Тинькофф': '78638',
                 'Газпром нефть': '39305',
                 'ВТБ': '4181',
                 'СИБУР': '3809',
                 'ТЕЛЕ2': '4219',
                 'МТС': '3776'
                 }
    for employer in employers_dict.values():
        employers.append(employer)
    #emp = Api_hh(employers)
    emp = Api_hh(employers).get_employers()
    vac = Api_hh(employers).get_vacancies()
    password = input('Пароль для подключения к базе данных: ')
    db = Data_base_maker('vac_employers', 'vacancies', 'employers', password)
    db.db_create()
    db.create_tables()
    db.insert_tables(emp, vac)
    manager = DBManager('vac_employers', password)
    print('Список компаний и количества вакансий у них имеющихся.')
    print(f'{manager.get_companies_and_vacancies()}\n')
    print('Список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.')
    print(f'{manager.get_all_vacancies()}\n')
    print('Средняя зарплата по вакансиям.')
    print(f'{manager.get_avg_salary()}\n')
    print('Cписок всех вакансий, у которых зарплата выше средней по всем вакансиям.')
    print(f'{manager.get_vacancies_with_higher_salary()}\n')
    print('Список всех вакансий, в названии которых есть переданные в метод слова.')
    print(manager.get_vacancies_with_keyword())
