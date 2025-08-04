import os
import psycopg2

def get_conn():
    conn = psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    return conn

