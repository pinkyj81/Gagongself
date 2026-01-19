import os
import pymssql

def get_conn():
    server = os.getenv("DB_SERVER", "ms0501.gabiadb.com")
    db = os.getenv("DB_NAME", "yujin")
    user = os.getenv("DB_USER", "yujin")
    pw = os.getenv("DB_PASSWORD", "yj8630")
    port = int(os.getenv("DB_PORT", "1433"))
    
    # pymssql은 SQL Server 2008과 호환성이 좋고 Render에서 잘 작동합니다
    conn = pymssql.connect(
        server=server,
        user=user,
        password=pw,
        database=db,
        port=port,
        timeout=30,
        login_timeout=30
    )
    return conn
