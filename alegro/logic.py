import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


class ProductManagement:
    def add_item(self, name, retail, wholesale, stock, distant):
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute('''CREATE TABLE IF NOT EXISTS goods(
                id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                name varchar(25),
                wholesale_cost integer,
                retail_cost integer);''')
                cur.execute('''INSERT INTO goods (name, wholesale_cost, retail_cost) 
                VALUES (%s, %s, %s)''', (name, retail, wholesale))

                cur.execute('''CREATE TABLE IF NOT EXISTS stocks(
                                id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                                goods_id bigint REFERENCES goods (id),
                                stock varchar(20),
                                distant_stock varchar(20));''')

                goods_id = self.search_item(name)[0]
                cur.execute('''INSERT INTO stocks (goods_id, stock, distant_stock) 
                                VALUES (%s, %s, %s)''', (goods_id, stock, distant))

                conn.commit()

    @staticmethod
    def search_item(name):
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM goods WHERE name = %s', (name,))
                result = cur.fetchone()
            return result

    @staticmethod
    def find_locate(good_id):
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT stock, distant_stock FROM stocks WHERE goods_id = %s', (good_id,))
                result = cur.fetchone()
        return result

