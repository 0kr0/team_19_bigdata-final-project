import psycopg2
import os

with open(os.path.join("secrets", "psql.pass"), "r") as f:
    password = f.read().strip()

conn_string = "host=hadoop-04.uni.innopolis.ru port=5432 user=team19 dbname=team19_projectdb password=" + password

try:
    conn = psycopg2.connect(conn_string)
    print("Successfully connected to PostgreSQL!")
    conn.close()
except Exception as e:
    print("Connection failed:", e)
