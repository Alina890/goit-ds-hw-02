from sqlite3 import Error
from connect import create_connection, database

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    except Error as e:
        print(e)

if __name__ == '__main__':
    sql_create_users_table = """
    CREATE TABLE users (
    id SERIAL primary key,
    fullname VARCHAR(100),
    email VARCHAR(100) UNIQUE
    );
    """

    sql_create_status_table = """
    CREATE TABLE status (
    id SERIAL primary key,
    name VARCHAR(50) UNIQUE
    );

    INSERT INTO status (name) VALUES
    ('new'),
    ('in progress'),
    ('completed');
    """
    sql_create_tasks_table = """
    CREATE TABLE tasks (
    id SERIAL primary key,
    title VARCHAR(100),
    description text,
    status_id INT,
    user_id INT,
    foreign key (status_id) references status (id) ON DELETE SET null ON UPDATE CASCADE,
    foreign key (user_id) references users (id) ON DELETE SET null ON UPDATE CASCADE
    );
    """
    with create_connection(database) as conn:
        if conn is not None:
            create_table(conn, sql_create_users_table)
            create_table(conn, sql_create_status_table)
            create_table(conn, sql_create_tasks_table)
        else:
            print("Error! cannot create the database connection.")
