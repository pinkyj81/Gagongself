import os
import pytds

def get_conn():
    server = os.getenv("DB_SERVER", "ms0501.gabiadb.com")
    db = os.getenv("DB_NAME", "yujin")
    user = os.getenv("DB_USER", "yujin")
    pw = os.getenv("DB_PASSWORD", "yj8630")
    port = int(os.getenv("DB_PORT", "1433"))
    
    # python-tds는 순수 Python 구현으로 컴파일 불필요, SQL Server 2008 호환
    conn = pytds.connect(
        server=server,
        database=db,
        user=user,
        password=pw,
        port=port,
        timeout=30,
        login_timeout=30,
        tds_version=pytds.TDS70  # SQL Server 2008 호환
    )
    return conn
