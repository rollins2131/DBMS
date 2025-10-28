# 🏦 Bank Management System — DBMSmini

A **Database Management Mini Project** simulating a **banking system**, built using:
- 🧰 **MySQL** — Database
- 🐍 **Python** — Backend
- 🖥️ **Streamlit** — User Interface

This project covers real banking operations like account creation, transactions, transfers, loans, audit logging, and role-based access.

---

## 📁 Project Structure

DBMSmini/
├── app.py # Streamlit application
├── .env # Environment variables (DB credentials)
├── requirements.txt # Python dependencies
├── DBMSmini.sql # ✅ Database schema and data dump
└── README.md # Project documentation

markdown
Copy code

---

## 🧱 Database (DBMSmini.sql)

The `.sql` file includes:
- **Tables**
  - `CUSTOMER` — customer details  
  - `EMPLOYEE` — employee info and roles  
  - `ACCOUNTS` — account details with balance  
  - `TRANSACTION` — deposit and withdrawal logs  
  - `TRANSFERS` — account-to-account transfers  
  - `LOANS` — loan applications  
  - `AUDIT_LOGS` — transaction & approval logs

- **Triggers**
  - Automatically update account balance after a transaction.
  - Insert log entry into `AUDIT_LOGS`.

- **Stored Procedure**
  - `sp_approve_loan` — approves pending loans and logs the action.

- **Function**
  - `fn_calculate_interest` — calculates interest based on input.

- **Queries**
  - Joins, nested queries, and aggregate queries implemented for reporting.

---

## ⚙️ Setting Up the Database

### 1. Open MySQL and create database
```sql
CREATE DATABASE mybank;
USE mybank;
2. Import the SQL file
Option 1 — Terminal:
bash
Copy code
mysql -u root -p mybank < DBMSmini.sql
Option 2 — MySQL Workbench:
Server → Data Import

Select Import from Self-Contained File

Choose DBMSmini.sql

Start Import

✅ This will create all tables, triggers, stored procedures, and functions.

🧪 Test Login Credentials
Role	ID	Password	Description
Admin	E001	1234	Manager role
Employee	E002	abcd	Employee role
Customer	C001	1234	Customer account

🚀 Running the Streamlit App
1. Create Virtual Environment
bash
Copy code
python -m venv venv
venv\Scripts\activate       # Windows
# or
source venv/bin/activate    # Mac/Linux
2. Install Dependencies
bash
Copy code
pip install -r requirements.txt
3. Set up .env
env
Copy code
DB_HOST=localhost
DB_USER=root
DB_PASS=yourpassword
DB_NAME=mybank
4. Run the App
bash
Copy code
streamlit run app.py
Then open http://localhost:8501 in your browser.

🧠 SQL Concepts Demonstrated
✅ Triggers — Auto update balance and insert into audit logs

✅ Stored Procedure — Loan approval process

✅ Functions — Interest calculation

✅ Joins — Customer–Account relations

✅ Nested Queries — Filtering high-value customers

✅ Aggregate Queries — Summarizing deposits

✅ Role-based Access Control

📝 User Roles
Role	Privileges
Admin	Full CRUD on customers, employees, accounts, loans, audit
Employee	Accounts, transactions, transfers, loans
Customer	View own accounts, check balance, reports

🧾 Example SQL Commands
Deposit Transaction

sql
Copy code
INSERT INTO TRANSACTION (transactionid, accno, transactiontype, amount, makerid)
VALUES ('UUID', 'A001', 'DEPOSIT', 5000, 'E001');
Trigger updates balance + adds to audit log automatically.

Approve Loan

sql
Copy code
CALL sp_approve_loan('L001', 'E001');
🛡️ Security Notes
Do not commit .env with real passwords.

.env should be listed in .gitignore.

The SQL file can be kept for easy setup — but remove sensitive data if pushing to public repo.
