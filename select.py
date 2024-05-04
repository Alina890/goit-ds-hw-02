import sqlite3 
from connect import create_connection, database

def execute_query(conn, query, *args):
    try:
        cursor = conn.cursor()
        cursor.execute(query, args)
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print(e)
        
# Отримати всі завдання певного користувача. 
def select_tasks_by_user(conn, user_id):
    query = """
    SELECT * FROM tasks WHERE user_id = ?;
    """
    return execute_query(conn, query, user_id)
        
# Вибрати завдання за певним статусом.  
def select_task_by_status(conn, status):
    query = """
    SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = ?);
    """
    return execute_query(conn, query, status)

# Оновити статус конкретного завдання.
def update_task_by_status(conn, task_id, new_status):
    query = """
    UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = ?) WHERE id = ?;
    """
    execute_query(conn, query, new_status,task_id)

# Отримати список користувачів, які не мають жодного завдання
def get_users_without_tasks(conn):
    query = """
    SELECT * FROM users WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks);
    """
    return execute_query(conn, query)

# Додати нове завдання для конкретного користувача. 
def add_task(conn, title, description, status_id, user_id):
    query = f"""
    INSERT INTO tasks (title, description, status_id, user_id)
    VALUES ('{title}', '{description}', {status_id}, {user_id});
    """
    execute_query(conn, query)

# Отримати всі завдання, які ще не завершено. 
def get_incomplete_tasks(conn):
    query = """
    SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = 'completed');
    """
    return execute_query(conn, query)

# Видалити конкретне завдання.
def delete_task(conn, task_id):
    query = f"""
    DELETE FROM tasks WHERE id = {task_id};
    """
    execute_query(conn, query)

# Знайти користувачів з певною електронною поштою. 
def get_users_by_email(conn, domain):
    query = f"""
    SELECT * FROM users WHERE email LIKE '%{domain}@%';
    """
    return execute_query(conn, query)

# Оновити ім'я користувача.
def update_username(conn, user_id, new_name):
    query = f"""
    UPDATE users SET fullname = '{new_name}' WHERE id = {user_id};
    """
    execute_query(conn, query)

# Отримати кількість завдань для кожного статусу.
def get_task_count_by_status(conn):
    query = """
    SELECT status.name, COUNT(tasks.id) AS task_count 
    FROM status LEFT JOIN tasks ON status.id = tasks.status_id 
    GROUP BY status.name;
    """
    return execute_query(conn, query)

# Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти.
def get_tasks_by_email_domain(conn, domain):
    query = f"""
    SELECT tasks.* 
    FROM tasks 
    JOIN users ON tasks.user_id = users.id 
    WHERE users.email LIKE '%{domain}@%';
    """
    return execute_query(conn, query)

# Отримати список завдань, що не мають опису.
def get_tasks_without_description(conn):
    query = """
    SELECT * FROM tasks WHERE description IS NULL OR description = '';
    """
    return execute_query(conn, query)

# Вибрати користувачів та їхні завдання, які є у статусі 'in progress'. 
def get_users_and_tasks_in_progress(conn):
    query = """
    SELECT users.*, tasks.* 
    FROM users 
    JOIN tasks ON users.id = tasks.user_id 
    JOIN status ON tasks.status_id = status.id 
    WHERE status.name = 'in progress';
    """
    return execute_query(conn, query)

# Отримати користувачів та кількість їхніх завдань.
def get_users_with_task_count(conn):
    query = """
    SELECT users.id, users.fullname, COUNT(tasks.id) AS task_count 
    FROM users 
    LEFT JOIN tasks ON users.id = tasks.user_id 
    GROUP BY users.id, users.fullname;
    """
    return execute_query(conn, query)


def main():
    with create_connection(database) as conn:
        if conn is not None:
        # Виконати запити
            print("All tasks user:")
            print(select_tasks_by_user(conn, 1))
            print("Tasks with 'new' status:")
            print(select_task_by_status(conn, "new"))
            print("Tasks with 'in progress' status:")
            print(select_task_by_status(conn, "in progress"))
            print("Tasks with 'completed' status:")
            print(select_task_by_status(conn, "completed"))
            update_task_by_status(conn, 1, "New status")
            print("Users without tasks:")
            print(get_users_without_tasks(conn))
            add_task(conn, "New Task", "Description", 1, 1)
            print("Incomplete tasks:")
            print(get_incomplete_tasks(conn))
            delete_task(conn, 1)
            print("Users with 'example.com' email:")
            print(get_users_by_email(conn, 'example.com'))
            update_username(conn, 1, "New Name")
            print("Task count by status:")
            print(get_task_count_by_status(conn))
            print("Tasks for users with 'example.com' email domain:")
            print(get_tasks_by_email_domain(conn, 'example.com'))
            print("Tasks without description:")
            print(get_tasks_without_description(conn))
            print("Users and their tasks in progress:")
            print(get_users_and_tasks_in_progress(conn))
            print("Users with task count:")
            print(get_users_with_task_count(conn))
        else:
            print("Error! Cannot create the database connection.")

if __name__ == '__main__':  
    main()
 # type: ignore