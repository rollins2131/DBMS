# 🏦 Bank Management System — DBMS Project

This is a **Bank Management System** built using **MySQL (Database)** and **Streamlit (UI)**.  
It demonstrates **Triggers, Stored Procedures, Functions, CRUD operations**, and **role-based access control** through Admin, Employee, and Customer logins.

---

## 📂 Project Structure

.
├── .env # Environment variables (DB credentials)
├── app.py # Main Streamlit application
├── requirements.txt # Python dependencies
└── README.md # Project documentation

yaml
Copy code

---

## 🛢️ Database Schema

- **CUSTOMER** — Stores customer information (CIF, name, branch, etc.)  
- **EMPLOYEE** — Stores employee details (PF No, designation, etc.)  
- **ACCOUNTS** — Stores account details with balance  
- **TRANSACTION** — Records deposits/withdrawals  
- **TRANSFERS** — Records transfers between accounts  
- **LOANS** — Handles loan applications and approvals  
- **AUDIT_LOGS** — Logs every critical action for tracking

---

## 🧰 Key Features

- 👤 **Role-based login**: Admin, Employee, Customer  
- 🏦 **Account management**: Open accounts, view balances  
- 💰 **Transactions**: Deposit and withdraw  
- 🔄 **Transfers**: Between accounts  
- 📝 **Loans**: Apply and approve loans  
- 🧾 **Audit Logs**: All actions automatically logged

---

## 🧠 Database Logic

- **Trigger**:  
  - Automatically updates balance in ACCOUNTS and inserts into AUDIT_LOGS after every transaction.

- **Stored Procedure**:  
  - `sp_approve_loan` — Approves loans and records approval in AUDIT_LOGS.

- **Function**:  
  - `fn_calculate_interest` — Calculates interest for given inputs.

- **Queries**:
  - Join: Customer–Account mapping  
  - Nested: High-value customers (balance > 50,000)  
  - Aggregate: Total deposits per account

---

## 🔐 Roles and Privileges

- **Admin (Manager)**  
  - Full access (Customers, Employees, Accounts, Transactions, Transfers, Loans, Reports, Audit Logs)

- **Employee**  
  - Accounts, Transactions, Transfers, Loans, Reports

- **Customer**  
  - View only their own accounts and reports

---

## ⚡ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/DBMS.git
cd DBMS
2. Create and activate virtual environment
bash
Copy code
python -m venv venv
venv\Scripts\activate      # For Windows
source venv/bin/activate   # For Mac/Linux
3. Install dependencies
bash
Copy code
pip install -r requirements.txt
4. Set up .env file
ini
Copy code
DB_HOST=localhost
DB_USER=root
DB_PASS=1234
DB_NAME=mybank
5. Run the Streamlit app
bash
Copy code
streamlit run app.py
6. Access the UI
Visit http://localhost:8501 in your browser.

🧪 Test Users
Role	ID	Password	Description
Admin	E001	1234	Manager role
Employee	E002	abcd	Normal employee
Customer	C001	1234	Customer role

🏁 Example SQL Commands
Insert Employee
sql
Copy code
INSERT INTO EMPLOYEE VALUES
('E001','John Doe','Manager','1234','2022-01-10','Bangalore');
Insert Transaction (UI triggers this)
sql
Copy code
INSERT INTO TRANSACTION (transactionid, accno, transactiontype, amount, makerid)
VALUES ('UUID', 'A001', 'DEPOSIT', 5000, 'E001');
Trigger handles:
Balance update in ACCOUNTS

Log entry in AUDIT_LOGS

🏅 Project Demonstration
✅ CRUD Operations on all tables

✅ Triggers, Stored Procedures, Functions

✅ Reports: Join, Nested, Aggregate

✅ GUI Integration with Streamlit

✅ Role-based Access Control

