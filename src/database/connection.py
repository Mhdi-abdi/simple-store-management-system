import mysql.connector
from dotenv import load_dotenv
import os

def get_connection():
    load_dotenv()

    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    name = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    try:
        connection = mysql.connector.connect(
        host = host,
        port = port,
        user = user,
        password = password,
        database = name
        )

        return connection
    
    except mysql.connector.Error as error:
        print(f"Database connection failed: {error}")
        return None