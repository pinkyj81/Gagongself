from flask import Flask, render_template, request, abort
from datetime import datetime, timedelta
from db_pymssql import get_conn
import logging

app = Flask(__name__)

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_date(s: str):
    return datetime.strptime(s, "%Y-%m-%d")

@app.get("/")
def home():
    return render_template("list.html", data=[], page=1, total_count=0)

@app.get("/list")
def list_view():
    try:
        start = request.args.get("start")  # YYYY-MM-DD
        end = request.args.get("end")      # YYYY-MM-DD
        page = int(request.args.get("page", "1"))
        page_size = 30

        if not start or not end:
            abort(400, "start, end 날짜가 필요합니다. 예: ?start=2026-01-19&end=2026-01-19")

        logger.info(f"조회 요청: start={start}, end={end}, page={page}")

        start_dt = parse_date(start)
        end_dt_exclusive = parse_date(end) + timedelta(days=1)

        start_row = (page - 1) * page_size + 1
        end_row = page * page_size

        count_sql = """
        SELECT COUNT(*) AS cnt
        FROM dbo.GaGongSelfH
        WHERE EntryDate >= ? AND EntryDate < ?;
        """

        # SQL Server 2008 paging: ROW_NUMBER()
        sql = """
        ;WITH X AS (
            SELECT
                ROW_NUMBER() OVER (ORDER BY EntryDate DESC) AS rn,
                SaupCode, SelfNo, InDate, CodeNo, Worker, WDate, Shift, WTime, LotNo,
                Install, BiGo, EndGu, EntryID, EntryDate, OkDate, OkID, OkEntryDate
            FROM dbo.GaGongSelfH
            WHERE EntryDate >= ? AND EntryDate < ?
        )
        SELECT *
        FROM X
        WHERE rn BETWEEN ? AND ?
        ORDER BY rn;
        """

        logger.info("데이터베이스 연결 시도...")
        with get_conn() as conn:
            cur = conn.cursor()
            logger.info("COUNT 쿼리 실행 중...")
            cur.execute(count_sql, (start_dt, end_dt_exclusive))
            total = cur.fetchone()[0]
            logger.info(f"총 레코드 수: {total}")
            
            logger.info("데이터 조회 쿼리 실행 중...")
            cur.execute(sql, (start_dt, end_dt_exclusive, start_row, end_row))
            rows = cur.fetchall()
            logger.info(f"조회된 레코드 수: {len(rows)}")

        total_pages = (total + page_size - 1) // page_size

        return render_template(
            "list.html",
            rows=rows,
            start=start, end=end,
            page=page, total_pages=total_pages,
            total=total
        )
    except Exception as e:
        logger.error(f"오류 발생: {str(e)}", exc_info=True)
        return f"<h1>오류 발생</h1><pre>{str(e)}</pre>", 500

@app.get("/detail/<selfno>")
def detail_view(selfno: str):
    sql = """
    SELECT
        SaupCode, SelfNo, InDate, CodeNo, Worker, WDate, Shift, WTime, LotNo,
        Install, BiGo, EndGu, EntryID, EntryDate, OkDate, OkID, OkEntryDate
    FROM dbo.GaGongSelfH
    WHERE SelfNo = ?;
    """

    with get_conn() as conn:
        cur = conn.cursor()
        row = cur.execute(sql, (selfno,)).fetchone()

    if not row:
        abort(404, "데이터가 없습니다.")

    return render_template("detail.html", row=row)

if __name__ == "__main__":
    app.run(debug=True)
