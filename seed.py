from sqlite3 import Error
from connect import create_connection, database
from faker import Faker
import random

fake = Faker()

def seed_users(conn, num_users) -> tuple:
    users = []
    emails = set()
    for _ in range(num_users):
        fullname = fake.name()
        email = fake.email()
        while email in emails:
            email = fake.email()
        users.append((fullname, email))
        emails.add(email)
    insert_query = "INSERT INTO users (fullname, email) VALUES (?, ?)"
    try:
        conn.executemany(insert_query, users)
    except Error as e:
        print(e)


def seed_status(conn):
    """ Seed status table with predefined values """
    status_values = [('new',), ('in progress',), ('completed',)]
    insert_query = "INSERT INTO status (name) VALUES (?)"
    try:
        conn.executemany(insert_query, status_values)
    except Error as e:
        print(e)

def seed_tasks(conn, num_tasks) -> tuple:
    """ Seed tasks table with random data """
    tasks = []
    for _ in range(num_tasks):
        title = fake.sentence()
        description = fake.paragraph()
        status_id = random.randint(1, 3)  
        user_id = random.randint(1, 10)    
        tasks.append((title, description, status_id, user_id))
    insert_query = "INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)"
    try:
        conn.executemany(insert_query, tasks)
    except Error as e:
        print(e)

if __name__ == '__main__':
    num_users = 10  
    num_tasks = 20  

    with create_connection(database) as conn:
        if conn is not None:
            seed_users(conn, num_users)
            seed_status(conn)
            seed_tasks(conn, num_tasks)
            conn.commit()
            print("Seed data successfully added.")
        else:
            print("Error! cannot create the database connection.")



