# 가공자주검사 조회 시스템

Flask 기반의 가공자주검사 데이터 조회 웹 애플리케이션입니다.

## 기능
- 날짜 범위별 가공자주검사 데이터 조회
- 페이징 처리
- SQL Server 데이터베이스 연동

## 환경 변수 설정

Render 또는 로컬 환경에서 다음 환경 변수를 설정하세요:

```
DB_SERVER=your_server.com
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password
DB_DRIVER=ODBC Driver 18 for SQL Server
```

## 로컬 실행

```bash
pip install -r requirements.txt
python app.py
```

## Render 배포

1. GitHub에 코드 푸시
2. Render에서 새 Web Service 생성
3. 환경 변수 설정
4. 배포 시작

## 필요 사항
- Python 3.8+
- SQL Server ODBC Driver 18 (로컬 개발용)
- SQL Server 2008 이상

## ⚠️ SQL Server 2008 구버전 주의사항

### Render 배포 시 문제 발생 시:

**Option 1: pyodbc 사용 (권장)**
- Render의 환경 변수에 `DB_DRIVER=FreeTDS` 설정
- 또는 `DB_DRIVER=ODBC Driver 17 for SQL Server` 시도

**Option 2: pymssql 사용 (대안)**
1. `requirements.txt`에서 `pymssql==2.2.8` 주석 해제
2. `app.py` 첫 줄 변경: `from db_pymssql import get_conn`
3. Render 재배포

### 연결 오류 해결:
- `Encrypt=no` 설정이 적용되어 구버전 SQL Server와 호환됩니다
- 방화벽에서 Render IP 허용 필요
- SQL Server에서 원격 연결 허용 확인

### 테스트 방법:
```python
from db import get_conn
conn = get_conn()
print("연결 성공!")
conn.close()
```
