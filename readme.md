В проекте реализовано получение данных о работодателях и вакансиях с сайте hh.ru:

1. Выбраны 10 компаний
2. Спроектированны таблицы в БД PostgreSQL для хранения полученных данных о работодателях и их вакансиях. 
3. Для работы с БД используется библиотека psycopg2.
4. Реализован код, который заполняет созданные в БД PostgreSQL таблицы данными о работодателях и их вакансиях.
5. Создан класс DBManager для работы с данными в БД, который будет подключается к БД PostgreSQL и иметь следующие методы:
 - get_companies_and_vacancies_count() — получает список всех компаний и количество вакансий у каждой компании.
 - get_all_vacancies() — получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
 - get_avg_salary() — получает среднюю зарплату по вакансиям.
 - get_vacancies_with_higher_salary() — получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
 - get_vacancies_with_keyword() — получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.