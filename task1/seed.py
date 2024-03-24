import psycopg2
import faker
from random import randint, choice
from create import create_tables

NUMBER_OF_TASK_STSTUSES = 3
NUMBER_OF_USERS = 15
NUMBER_OF_TASKS = 60

def gen_fake_data(number_of_users, number_of_tasks) -> tuple:
    fake_users = []
    fake_tasks = []
    fake_data = faker.Faker("en_US")

    for i in range(number_of_users):
        fake_users.append([fake_data.unique.name(), fake_data.unique.email()])
    
    tasks_word_list_action = ["create", "update", "insert", "alter", "remove", "drop", "delete"]
    tasks_word_list_object = ["DB", "script", "triger", "function", "procedure", "index", "table", "schema", "dump"]

    for i in range(number_of_tasks):
        fake_tasks.append([f"{choice(tasks_word_list_action)} {choice(tasks_word_list_object)}", faker.Faker().sentence(ext_word_list = (tasks_word_list_action + tasks_word_list_object), nb_words = 8)]) 
        
    return fake_users, fake_tasks

def prep_data(users, tasks) -> tuple:
    user_insert = []
    for user in users:
        user_insert.append((user[0], user[1]))
    
    task_insert = []
    for task in tasks:
        task_insert.append((task[0], task[1], randint(1, NUMBER_OF_TASK_STSTUSES), randint(1, NUMBER_OF_USERS)))
    
    status_insert = []
    for status in ["new", "in progress", "completed"]:
        status_insert.append((status, ))

    return user_insert, task_insert, status_insert

def fill_db(users, statuses, tasks) -> None:

    connection = psycopg2.connect(
    database = "", user = "postgres",
    password = "postrgespassword", host = "localhost", port = 5432)

    cursor = connection.cursor()

    sql_insert_into_users = """insert into users(fullname, email) values(%s, %s)"""
    cursor.executemany(sql_insert_into_users, users)
    connection.commit()

    sql_insert_into_statuses = """insert into statuses(name) values(%s)"""
    cursor.executemany(sql_insert_into_statuses, statuses)
    connection.commit()

    sql_insert_into_tasks = """insert into tasks(title, description, status_id, user_id) values(%s, %s, %s, %s)"""
    cursor.executemany(sql_insert_into_tasks, tasks)
    connection.commit()

    cursor.close()
    connection.close()
   
if __name__ == "__main__":
    create_tables("create_tables.sql")
    users, tasks, statuses = prep_data(*gen_fake_data(NUMBER_OF_USERS, NUMBER_OF_TASKS))
    try:
        fill_db(users, statuses, tasks)
        print("DB filled successfully.")
    except Exception as e:
        print(f"Error: {e}")
