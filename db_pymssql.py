import os
import pytds
import logging

logger = logging.getLogger(__name__)

def get_conn():
    try:
        server = os.getenv("DB_SERVER", "ms0501.gabiadb.com")
        db = os.getenv("DB_NAME", "yujin")
        user = os.getenv("DB_USER", "yujin")
        pw = os.getenv("DB_PASSWORD", "yj8630")
        port = int(os.getenv("DB_PORT", "1433"))
        
        logger.info(f"DB 연결 시도: {server}:{port}/{db}")
        
        # python-tds는 순수 Python 구현으로 컴파일 불필요, SQL Server 2008 호환
        conn = pytds.connect(
            server=server,
            database=db,
            user=user,
            password=pw,
            port=port,
            timeout=30,
            login_timeout=30
        )
        
        logger.info("DB 연결 성공!")
        return conn
    except Exception as e:
        logger.error(f"DB 연결 실패: {str(e)}", exc_info=True)
        raise
