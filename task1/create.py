import psycopg2
from pathlib import Path

def create_tables(sql_script: str):
    '''Arg. -> "<script_name>.sql"'''
    try:
        script_file = Path(sql_script).absolute()
        script = ''
        with open(script_file, "r") as f:
            script = f.read()

        connection = psycopg2.connect(
            database = "", user = "postgres",
            password = "postrgespassword", host = "localhost", port = 5432)

        cursor = connection.cursor()
        cursor.execute(script)
        connection.commit()
        cursor.close()
        connection.close()
        print("Script executed successfully (tables created).")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_tables("create_tables.sql")