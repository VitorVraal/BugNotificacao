from db_mysql import MySqlConnector
from db_model import DBModel
from mysql.connector import Error

def main():
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()

    if conn:
        print(msg)
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * from estoque")
            result = cursor.fetchall()
            print("Resultado:", result)
            cursor.close()
            db.disconnect()
        finally:
            db.disconect()

if __name__ == "__main__":
    main()
