import mariadb, pandas as pd, sys

#Данные для подключения к БД
config = {
    'user': 'corp_reader',
    'password': 'corp_reader',
    'host': '149.154.71.99',
    'port': 3306,
    'database': 'corp'
}

#Отрабатываем возможную ошибку
try:
    conn = mariadb.connect(**config)
except mariadb.Error as e:
    print(f"Ошибка подключения к MariaDB: {e}")
    sys.exit(1)

#SQL-запросы к БД
query1 = "SELECT * FROM locations"
query1 = "SELECT * FROM locations"
query2 = "SELECT * FROM managers"
query3 = "SELECT * FROM branches"
query4 = "SELECT * FROM reports"

#Извлекаем данные из БД
loc = pd.read_sql(query1, conn)
man = pd.read_sql(query2, conn)
branch = pd.read_sql(query3, conn)
rep = pd.read_sql(query4, conn)
conn.close()

#Импортируем извлеченные таблицы в локальную среду SQLite
import sqlalchemy as sql
connect = sql.create_engine('sqlite:///D:\\Практика_Pandas\\DB.db')
loc.to_sql('locations', connect, index=False)
man.to_sql('managers', connect, index=False)
branch.to_sql('branches', connect, index=False)
rep.to_sql('reports', connect, index=False)
connect.dispose()

