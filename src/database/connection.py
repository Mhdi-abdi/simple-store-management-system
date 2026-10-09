import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():

    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT", default=3306)
    name = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    connection = mysql.connector.connect(
    host = host,
    port = port,
    user = user,
    password = password,
    database = name
    )

    return connection
    
        