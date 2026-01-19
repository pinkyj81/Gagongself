from flask import Flask, render_template, request, abort
from datetime import datetime, timedelta
from db import get_conn

app = Flask(__name__)

def parse_date(s: str):
    return datetime.strptime(s, "%Y-%m-%d")

@app.get("/")
def home():
    return render_template("list.html", data=[], page=1, total_count=0)

@app.get("/list")
def list_view():
    start = request.args.get("start")  # YYYY-MM-DD
    end = request.args.get("end")      # YYYY-MM-DD
    page = int(request.args.get("page", "1"))
    page_size = 30

    if not start or not end:
        abort(400, "start, end 날짜가 필요합니다. 예: ?start=2026-01-19&end=2026-01-19")

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

    with get_conn() as conn:
        cur = conn.cursor()
        total = cur.execute(count_sql, (start_dt, end_dt_exclusive)).fetchone().cnt
        rows = cur.execute(sql, (start_dt, end_dt_exclusive, start_row, end_row)).fetchall()

    total_pages = (total + page_size - 1) // page_size

    return render_template(
        "list.html",
        rows=rows,
        start=start, end=end,
        page=page, total_pages=total_pages,
        total=total
    )

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
