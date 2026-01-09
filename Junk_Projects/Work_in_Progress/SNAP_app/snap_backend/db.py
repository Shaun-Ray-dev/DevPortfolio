# DB connection helper

import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="snap_db",      # <--- correct database name
        user="postgres",      
        password="postgres",  
        host="localhost",
        port="5432"
    )

