# -*- кодирование: utf-8 -*-
import psycopg2

# 1. Функция, создающая структуру БД (таблицы).
# 2. Функция, позволяющая добавить нового клиента.
# 3. Функция, позволяющая добавить телефон для существующего клиента.
# 4. Функция, позволяющая изменить данные о клиенте.
# 5. Функция, позволяющая удалить телефон для существующего клиента.
# 6. Функция, позволяющая удалить существующего клиента.
# 7. Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.


# 1. Функция, создающая структуру БД (таблицы).
def create_db(conn):
    with conn.cursor() as cur:
          # Создание таблицы клиентов
        cur.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                email VARCHAR(100) UNIQUE
            );
        ''')
     # Создание таблицы с телефонами
        cur.execute('''
            CREATE TABLE IF NOT EXISTS phones (
                id SERIAL PRIMARY KEY,
                client_id INTEGER REFERENCES clients(id) ON DELETE CASCADE,
                phone VARCHAR(20)
            );
        ''')
        conn.commit()


# 2. Функция, позволяющая добавить нового клиента.
def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        # указать инфо по клиенту
        cur.execute('''
            INSERT INTO clients (first_name, last_name, email) 
            VALUES (%s, %s, %s) RETURNING id;
        ''', (first_name, last_name, email))
        client_id = cur.fetchone()[0]
        # указать телефон
        if phones:
            for phone in phones:
                add_phone(conn, client_id, phone)
        conn.commit()


# 3.  Функция, позволяющая добавить телефон для существующего клиента.
def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute('''
            INSERT INTO phones (client_id, phone) 
            VALUES (%s, %s);
        ''', (client_id, phone))
        conn.commit()


# 4. Функция, позволяющая изменить данные о клиенте.
def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    with conn.cursor() as cur:
        # изменить информацию по клиенту
        if first_name:
            cur.execute('UPDATE clients SET first_name = %s WHERE id = %s;', (first_name, client_id))
        if last_name:
            cur.execute('UPDATE clients SET last_name = %s WHERE id = %s;', (last_name, client_id))
        if email:
            cur.execute('UPDATE clients SET email = %s WHERE id = %s;', (email, client_id))
        if phones is not None:
            # заменить телефон на другой
            cur.execute('DELETE FROM phones WHERE client_id = %s;', (client_id,))
            for phone in phones:
                add_phone(conn, client_id, phone)
        conn.commit()


# 5.  Функция, позволяющая удалить телефон для существующего клиента.
def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute('''
            DELETE FROM phones WHERE client_id = %s AND phone = %s;
        ''', (client_id, phone))
        conn.commit()


# 6. Функция, позволяющая удалить существующего клиента.

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute('DELETE FROM clients WHERE id = %s;', (client_id,))
        conn.commit()


# 7. Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        query = '''
            SELECT c.id, c.first_name, c.last_name, c.email, p.phone
            FROM clients c
            LEFT JOIN phones p ON c.id = p.client_id
            WHERE
        '''
        conditions = []
        params = []
        if first_name:
            conditions.append('c.first_name = %s')
            params.append(first_name)
        if last_name:
            conditions.append('c.last_name = %s')
            params.append(last_name)
        if email:
            conditions.append('c.email = %s')
            params.append(email)
        if phone:
            conditions.append('p.phone = %s')
            params.append(phone)

        if conditions:
            query += ' AND '.join(conditions)

        cur.execute(query, params)
        results = cur.fetchall()
        for row in results:
            print(row)


# пример использовнаи¤ функций
with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
    add_client(conn, "Иван", "Иванов", "ivanov@mail.ru", ["+123456789"])
    add_client(conn, "Степан", "Сидоров", "sidorov@mail.ru")
    add_phone(conn, 2, "+123123123")
    change_client(conn, 1, email="ivanov@gmail.com")
    delete_phone(conn, 1, "+123456789")
    delete_client(conn, 1)
    find_client(conn, first_name="Иван")

conn.close()
