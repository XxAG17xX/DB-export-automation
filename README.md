# 🗄️ SQL Server → CSV (Weekly Export, Python)

A small automation project: run a SQL query against **Microsoft SQL Server** and export the results to **CSV**.  
Designed for Windows with **Task Scheduler**, using **Windows Authentication** by default (no passwords in code).

---

## ✨ Features
- Runs SQL from `query.sql`
- Exports **dated CSV**: `report_YYYY-MM-DD.csv`
- Maintains a stable **`latest.csv`** (always the newest file)
- Simple **logging** to `logs.txt`
- Cleans up old reports automatically (default: 60 days)

---

## ⚙️ Prerequisites
- **Python 3.10+** (Anaconda or system Python)  
- **Microsoft ODBC Driver for SQL Server**  
  - Use **18** if available; **17** also works.  
- **SQL Server** reachable (local `SQLEXPRESS` or remote host)

Check installed drivers inside Python:
```python
import pyodbc
print(pyodbc.drivers())
