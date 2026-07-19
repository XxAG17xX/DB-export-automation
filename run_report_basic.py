import pyodbc, csv, datetime

# connection info
server = r"ABCDW\SQLEXPRESS"   # use exactly what SSMS shows as Server name
database = "DemoDB"

conn_str = (
    "Driver={ODBC Driver 18 for SQL Server};"
    f"Server={server};Database={database};"
    "Trusted_Connection=yes;Encrypt=yes;TrustServerCertificate=yes"
)

# read query from file
with open("query.sql", "r", encoding="utf-8") as f:
    sql = f.read()

# execute query
with pyodbc.connect(conn_str) as conn:
    cur = conn.cursor()
    cur.execute(sql)
    cols = [c[0] for c in cur.description]
    rows = cur.fetchall()

# write results to dated CSV
stamp = datetime.datetime.now().strftime("%Y-%m-%d")
out_file = f"report_{stamp}.csv"

with open(out_file, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(cols)
    writer.writerows(rows)

print("Saved:", out_file)
