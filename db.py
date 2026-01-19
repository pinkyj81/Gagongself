import os
import pyodbc

def get_conn():
    server = os.getenv("DB_SERVER", "ms0501.gabiadb.com")
    db = os.getenv("DB_NAME", "yujin")
    user = os.getenv("DB_USER", "yujin")
    pw = os.getenv("DB_PASSWORD", "yj8630")
    driver = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")

    conn_str = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={db};"
        f"UID={user};"
        f"PWD={pw};"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str)
