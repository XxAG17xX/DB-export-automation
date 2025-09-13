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
```

---

## 📥 Installation
Clone the repo and install requirements:
```bash
git clone https://github.com/YOUR-USERNAME/sqlserver-weekly-export.git
cd sqlserver-weekly-export
pip install -r requirements.txt
```

---

## 🛠️ Configuration
Open `run_report.py` and set:
```python
server   = r"whatevr your smss shows"   # or "host,1433"
database = "YourDBname"
driver   = "ODBC Driver 18 for SQL Server"  # or "ODBC Driver 17 for SQL Server"
```

### Authentication
- **Windows Auth (default)** → works if the Windows account running the task has DB read access.  
- **SQL Auth** → swap connection string to include:
  ```
  UID=readonly_user;PWD=secret;
  ```
  and remove `Trusted_Connection=yes`.

---

## ▶️ Run Locally
Put your SQL in `query.sql`, e.g.:
```sql
SELECT id, name, subject
FROM Students;
```

Run:
```bash
python run_report.py
```

Expected output:
- ✅ `report_YYYY-MM-DD.csv`  
- ✅ `latest.csv`  
- ✅ `logs.txt` with START / SUCCESS entries  

---

## 📅 Automate with Task Scheduler (Windows)
1. Open **Task Scheduler** → **Create Task…**
2. **General**
   - Name: `Weekly DB Export`
   - Run whether user is logged on or not
   - Run with highest privileges
3. **Triggers**
   - Weekly → pick day/time (e.g. Mondays 08:00, Europe/Dublin time)
4. **Actions**
   - **Program/script**: full path to your `python.exe` (conda env or system)
   - **Arguments**: full path to `run_report.py`
   - **Start in**: folder containing the script
5. **Settings**
   - Restart on failure (every 5 min, up to 3 times)
   - Stop task if running longer than 30 min
6. Test by right-clicking the task → **Run** → check for new CSV + logs.

---

## 📂 Repo Contents
```
├─ run_report.py   # initial version (minimal working script)
├─ run_report_1.py         # improved version (logs, latest.csv, cleanup)
├─ query.sql             # your SQL query
├─ sample_output.csv     # example output (5 rows, 3 cols)
├─ requirements.txt      # Python dependencies
├─ .gitignore
└─ README.md
```

## 🧰 Troubleshooting
- **IM002 / “Data source name not found / no default driver”**  
  → The `Driver={...}` must match exactly one from `pyodbc.drivers()` (e.g., `ODBC Driver 18 for SQL Server` or `ODBC Driver 17 for SQL Server`).

- **Login failed**  
  → The Windows account running the task needs DB read permissions (Windows Auth), or use SQL Auth with a read-only SQL user.

- **Works manually, fails in Task Scheduler**  
  - Use absolute paths.  
  - Set **Start in** to the repo folder.  
  - Ensure the correct `python.exe` (conda env vs system) in **Program/script**.  
  - Check `logs.txt` and Task Scheduler **History** for details.

---

## 🚀 Roadmap / Nice-to-haves
- Email/Slack/Teams alert on failure
- Parameterized date windows (e.g. “last full week”)
- Export directly to cloud storage (S3, SharePoint, etc.)
- Dashboard in Power BI / Excel connected to `latest.csv`

---

