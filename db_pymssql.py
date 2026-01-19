"""
SQL Server 2008 구버전 호환 - pymssql 버전
pyodbc가 Render에서 작동하지 않을 경우 이 파일을 사용하세요.

사용 방법:
1. requirements.txt에서 pymssql==2.2.8 주석 해제
2. app.py 첫 줄을 다음과 같이 변경:
   from db_pymssql import get_conn
"""
import os
import pymssql

def get_conn():
    server = os.getenv("DB_SERVER", "ms0501.gabiadb.com")
    db = os.getenv("DB_NAME", "yujin")
    user = os.getenv("DB_USER", "yujin")
    pw = os.getenv("DB_PASSWORD", "yj8630")
    port = int(os.getenv("DB_PORT", "1433"))
    
    # pymssql은 SQL Server 2008과 호환성이 좋습니다
    conn = pymssql.connect(
        server=server,
        user=user,
        password=pw,
        database=db,
        port=port,
        timeout=30,
        login_timeout=30,
        as_dict=False  # pyodbc와 동일한 튜플 형식 반환
    )
    return conn
