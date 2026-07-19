import pyodbc, csv, datetime, sys
from pathlib import Path
from shutil import copyfile

# --- config you will change on your friend's machine ---
server   = r"YoursSERVERname"   # or "host,1433"
database = "YourDatabase"
driver   = "ODBC Driver 18 for SQL Server"  # change to 17 if that's installed

# --- paths (robust for Task Scheduler) ---
BASE = Path(__file__).resolve().parent
QUERY_FILE = BASE / "query.sql"
OUT_FILE   = BASE / f"report_{datetime.datetime.now():%Y-%m-%d}.csv"
LATEST     = BASE / "latest.csv"
LOG_FILE   = BASE / "logs.txt"

def log(msg: str):
    LOG_FILE.write_text("" if not LOG_FILE.exists() else LOG_FILE.read_text(encoding="utf-8"), encoding="utf-8")
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] {msg}\n")

def main():
    conn_str = (
    f"Driver={{{driver}}};"
    f"Server={server};Database={database};"
    "Trusted_Connection=yes;Encrypt=yes;TrustServerCertificate=yes"
)
    # read SQL
    sql = QUERY_FILE.read_text(encoding="utf-8")

    # run query
    with pyodbc.connect(conn_str) as conn:
        cur = conn.cursor()
        cur.execute(sql)
        cols = [c[0] for c in cur.description]
        rows = cur.fetchall()

    # write CSV (UTF-8 BOM so Excel opens cleanly)
    with OUT_FILE.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(cols)
        w.writerows(rows)

    # stable pointer + light rotation
    try:
        copyfile(OUT_FILE, LATEST)
    except Exception:
        pass

    # delete CSVs older than 60 days
    cutoff = datetime.datetime.now().timestamp() - 60*24*3600
    for p in BASE.glob("report_*.csv"):
        try:
            if p.stat().st_mtime < cutoff:
                p.unlink()
        except Exception:
            pass

    log(f"SUCCESS: wrote {OUT_FILE.name}")
    print("Saved:", OUT_FILE)

if __name__ == "__main__":
    try:
        log("START export")
        main()
        sys.exit(0)
    except Exception as e:
        log(f"ERROR: {e}")
        print("ERROR:", e, file=sys.stderr)
        sys.exit(1)
