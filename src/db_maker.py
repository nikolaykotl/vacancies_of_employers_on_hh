from src.function import connection
import psycopg2


class Data_base_maker():
    def __init__(self, database, vac_table, emp_table, password):
        self.database = database
        self.vac_table = vac_table
        self.emp_table = emp_table
        self.password = password

    def db_create(self):
        conn = psycopg2.connect(dbname='postgres', user='postgres', password=self.password)
        cursor = conn.cursor()
        conn.autocommit = True

       # команда для удаления базы данных если она существует

        sql = f"DROP DATABASE IF EXISTS {self.database}"
        cursor.execute(sql)
        # команда для создания базы данных
        sql = f'CREATE DATABASE {self.database}'

        # выполняем код sql
        cursor.execute(sql)
        #return (f"База данных {self.database} успешно создана")

        cursor.close()
        conn.close()

    def create_tables(self):

        with connection(self.database, self.password) as conn:
            with conn.cursor() as cur:
        # создаем таблицу employers
                cur.execute(f"CREATE TABLE IF NOT EXISTS {self.emp_table}(employer_id SERIAL PRIMARY KEY,"
                            f"employer_name VARCHAR(50),"
                            f"site TEXT,"
                            f"city VARCHAR(50),"
                            f"industries_name TEXT)")
        # поддверждаем транзакцию
         #   print(f"Таблица {self.emp_table} успешно создана")


        with connection(self.database, self.password) as conn:
             with conn.cursor() as cur:
                    # создаем таблицу employers
                 cur.execute(
                        f"CREATE TABLE IF NOT EXISTS {self.vac_table}"
                        f"(vacancy_id SERIAL PRIMARY KEY,"
                        f"employer_id INT REFERENCES {self.emp_table}(employer_id),"
                        f"vacancy_name VARCHAR(100),"
                        f"salary_from INT,"
                        f"salary_to INT,"
                        f"currency VARCHAR(3),"
                        f"url TEXT)"
                    )
                # поддверждаем транзакцию
        #print(f"Таблица {self.vac_table} успешно создана")

    def insert_tables(self, employers, vacancies):
        with connection(self.database, self.password) as conn:
             with conn.cursor() as cur:

                for employer in employers:
                    cur.execute(f'INSERT INTO {self.emp_table} (employer_name, site, city, industries_name)'
                                f'VALUES (%s, %s, %s, %s) RETURNING employer_id', (employer['employer_name'], employer['employer_site_url'], employer['city'], employer['industries_name']))
                    employer_id = cur.fetchone()[0]

                    for vacancy in vacancies:
                        if vacancy['employer_id'] == employer['employer_id']:
                            cur.execute(f"INSERT INTO {self.vac_table}(employer_id, vacancy_name, salary_from, salary_to, currency, url)"
                                        f"VALUES (%s, %s, %s, %s, %s, %s)", (employer_id, vacancy['vacancy_name'], vacancy['salary_from'], vacancy['salary_to'], vacancy['currency'], vacancy['url']))