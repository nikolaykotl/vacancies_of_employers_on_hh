import psycopg2

def connection(database, user_password):
  #  user_password = input('Пароль для подключения к базе данных: ')
    connection = psycopg2.connect(host='localhost', dbname=database, user='postgres',
                                  password=user_password)
    return connection
