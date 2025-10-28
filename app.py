# app.py — Full Version with Fixes
import os
import uuid
import streamlit as st
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# ---------- Streamlit Config ----------
st.set_page_config(page_title="🏦 Bank Management (Python + MySQL)", layout="wide")

# ---------- DB Config ----------
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "1234")
DB_NAME = os.getenv("DB_NAME", "mybank")

# ---------- DB Utility Functions ----------
def get_conn():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME
        )
        return conn
    except Error as e:
        st.error(f"❌ Database connection failed: {e}")
        return None

def fetch_one(query, params=None):
    conn = get_conn()
    if not conn: return None
    with conn.cursor(dictionary=True) as cur:
        cur.execute(query, params or ())
        row = cur.fetchone()
    conn.close()
    return row

def fetch_all(query, params=None):
    conn = get_conn()
    if not conn: return []
    with conn.cursor(dictionary=True) as cur:
        cur.execute(query, params or ())
        rows = cur.fetchall()
    conn.close()
    return rows

def exec_write(query, params=None):
    conn = get_conn()
    if not conn: return
    with conn.cursor() as cur:
        cur.execute(query, params or ())
        conn.commit()
    conn.close()

def call_proc(name, args):
    conn = get_conn()
    if not conn: return
    with conn.cursor() as cur:
        cur.callproc(name, args)
        conn.commit()
    conn.close()

def call_scalar_function(function_sql, params=None):
    conn = get_conn()
    if not conn: return None
    with conn.cursor() as cur:
        cur.execute(function_sql, params or ())
        row = cur.fetchone()
    conn.close()
    return row[0] if row else None

# ---------- Authentication ----------
def login(user_id, password):
    # Try Employee
    emp = fetch_one(
        "SELECT pfno AS id, empname AS name, designation, password_hash FROM EMPLOYEE WHERE pfno=%s",
        (user_id,)
    )
    if emp:
        if password == emp["password_hash"]:
            role = "admin" if emp["designation"].lower() == "manager" else "employee"
            return role, emp
        return None, None

    # Try Customer
    cust = fetch_one(
        "SELECT cif AS id, fname, lname, password_hash FROM CUSTOMER WHERE cif=%s",
        (user_id,)
    )
    if cust and password == cust["password_hash"]:
        return "customer", cust
    return None, None

# ---------- UI Components ----------
def show_login():
    st.title("🏦 Bank Management System")
    st.caption("Plain-text login (for demonstration).")

    with st.form("login_form"):
        user_id = st.text_input("User ID (e.g. E001 / C001)")
        pwd = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        role, profile = login(user_id.strip(), pwd)
        if role:
            st.session_state["role"] = role
            st.session_state["user"] = profile
            st.rerun()   # ✅ FIXED
        else:
            st.error("Invalid credentials.")

def nav_bar():
    role = st.session_state["role"]
    st.sidebar.title("Navigation")

    if role == "admin":
        return st.sidebar.radio("Go to", [
            "Dashboard", "Customers", "Employees", "Accounts", "Transactions",
            "Transfers", "Loans", "Audit Logs", "Reports"
        ])
    elif role == "employee":
        return st.sidebar.radio("Go to", [
            "Dashboard", "Accounts", "Transactions", "Transfers", "Loans", "Reports"
        ])
    else:
        return st.sidebar.radio("Go to", [
            "Dashboard", "My Accounts", "Reports"
        ])

# ---------- Dashboard ----------
def dashboard():
    st.header("📊 Dashboard")
    role = st.session_state["role"]
    user = st.session_state["user"]
    if role in ("admin", "employee"):
        st.write(f"Welcome, **{user.get('name','Employee')}** ({role})")
        accounts = fetch_all("SELECT accno, cif, accttype, balance FROM ACCOUNTS ORDER BY accno")
        st.subheader("All Accounts")
        st.dataframe(accounts, use_container_width=True)
    else:
        st.write(f"Welcome, **{user.get('fname','Customer')}** ({role})")
        accs = fetch_all("SELECT accno, accttype, balance FROM ACCOUNTS WHERE cif=%s", (user["id"],))
        st.subheader("My Accounts")
        st.dataframe(accs, use_container_width=True)

# ---------- Customers Page ----------
def customers_page():
    st.header("👤 Customers (Admin)")
    col = st.columns(2)
    with col[0]:
        st.subheader("Create / Update")
        with st.form("cust_form"):
            cif = st.text_input("CIF")
            fname = st.text_input("First Name")
            lname = st.text_input("Last Name")
            password_hash = st.text_input("Password (plain)")
            submitted = st.form_submit_button("Upsert")
        if submitted and cif and fname and password_hash:
            exists = fetch_one("SELECT cif FROM CUSTOMER WHERE cif=%s", (cif,))
            if exists:
                exec_write("UPDATE CUSTOMER SET fname=%s, lname=%s, password_hash=%s WHERE cif=%s",
                           (fname, lname, password_hash, cif))
                st.success("Customer updated.")
            else:
                exec_write("INSERT INTO CUSTOMER (cif,fname,lname,password_hash) VALUES (%s,%s,%s,%s)",
                           (cif, fname, lname, password_hash))
                st.success("Customer created.")

    with col[1]:
        st.subheader("Delete")
        cif_del = st.text_input("CIF to delete")
        if st.button("Delete Customer"):
            exec_write("DELETE FROM CUSTOMER WHERE cif=%s", (cif_del,))
            st.info("Deleted if existed.")

    st.subheader("All Customers")
    st.dataframe(fetch_all("SELECT cif, fname, lname, homebranch, opening_date FROM CUSTOMER"), use_container_width=True)

# ---------- Employees Page ----------
def employees_page():
    st.header("👔 Employees (Admin)")
    col = st.columns(2)
    with col[0]:
        with st.form("emp_form"):
            pfno = st.text_input("PF No")
            name = st.text_input("Name")
            desig = st.selectbox("Designation", ["Manager","Teller","Clerk","Officer"])
            pwd = st.text_input("Password (plain)")
            submitted = st.form_submit_button("Upsert")
        if submitted and pfno and name and pwd:
            exists = fetch_one("SELECT pfno FROM EMPLOYEE WHERE pfno=%s", (pfno,))
            if exists:
                exec_write("UPDATE EMPLOYEE SET empname=%s, designation=%s, password_hash=%s WHERE pfno=%s",
                           (name, desig, pwd, pfno))
                st.success("Employee updated.")
            else:
                exec_write("INSERT INTO EMPLOYEE (pfno, empname, designation, password_hash) VALUES (%s,%s,%s,%s)",
                           (pfno, name, desig, pwd))
                st.success("Employee created.")

    with col[1]:
        pf_del = st.text_input("PF No to delete")
        if st.button("Delete Employee"):
            exec_write("DELETE FROM EMPLOYEE WHERE pfno=%s", (pf_del,))
            st.info("Deleted if existed.")

    st.subheader("All Employees")
    st.dataframe(fetch_all("SELECT pfno, empname, designation, joining_date FROM EMPLOYEE"), use_container_width=True)

# ---------- Accounts Page ----------
def accounts_page(employee_mode=True):
    if employee_mode:
        st.header("🏦 Accounts")
    else:
        st.header("💳 My Accounts")

    role = st.session_state["role"]
    user = st.session_state["user"]

    if role == "customer":
        rows = fetch_all("SELECT accno, accttype, balance, interest_rate FROM ACCOUNTS WHERE cif=%s", (user["id"],))
        st.dataframe(rows, use_container_width=True)
        return

    # Admin/Employee can view all and create
    st.subheader("Open Account")
    with st.form("acct_open"):
        accno = st.text_input("Account No")
        cif = st.text_input("CIF")
        accttype = st.selectbox("Type", ["SAVINGS","CURRENT","RECURRING"])
        ir = st.number_input("Interest Rate (%)", value=3.50, step=0.25)
        opening = st.form_submit_button("Create")
    if opening and accno and cif:
        exec_write("INSERT INTO ACCOUNTS (accno,cif,accttype,interest_rate) VALUES (%s,%s,%s,%s)",
                   (accno, cif, accttype, ir))
        st.success("Account created.")

    st.subheader("All Accounts")
    st.dataframe(fetch_all("SELECT accno, cif, accttype, balance, interest_rate FROM ACCOUNTS"), use_container_width=True)

# ---------- Transactions ----------
def transactions_page():
    st.header("💰 Transactions (fires trigger)")
    user = st.session_state["user"]

    with st.form("txn_form"):
        accno = st.text_input("Account No")
        ttype = st.selectbox("Type", ["DEPOSIT","WITHDRAWAL"])
        amount = st.number_input("Amount", min_value=0.01, step=0.01)
        checker = st.text_input("Checker PF No (optional)")
        submitted = st.form_submit_button("Post Transaction")
    if submitted and accno and amount > 0:
        txn_id = str(uuid.uuid4())
        exec_write(
            "INSERT INTO `TRANSACTION` (transactionid, accno, transactiontype, amount, makerid, checkerid) VALUES (%s,%s,%s,%s,%s,%s)",
            (txn_id, accno, ttype, amount, user["id"], checker if checker else None)
        )
        st.success(f"Transaction posted: {txn_id}. Trigger executed.")

    st.subheader("Recent Transactions")
    st.dataframe(fetch_all("SELECT transactionid, accno, transactiontype, amount, transactiondate, makerid FROM `TRANSACTION` ORDER BY transactiondate DESC LIMIT 50"), use_container_width=True)

# ---------- Transfers ----------
def transfers_page():
    st.header("🔄 Transfers (between accounts)")
    with st.form("tr_form"):
        from_acc = st.text_input("From Account")
        to_acc = st.text_input("To Account")
        amount = st.number_input("Amount", min_value=0.01, step=0.01)
        submitted = st.form_submit_button("Transfer")
    if submitted and from_acc and to_acc and amount > 0:
        tr_id = str(uuid.uuid4())
        user = st.session_state["user"]
        try:
            exec_write("INSERT INTO TRANSFERS (transferid, from_accno, to_accno, amount) VALUES (%s,%s,%s,%s)",
                       (tr_id, from_acc, to_acc, amount))
            exec_write("INSERT INTO `TRANSACTION` (transactionid, accno, transactiontype, amount, makerid) VALUES (%s,%s,'WITHDRAWAL',%s,%s)",
                       (str(uuid.uuid4()), from_acc, amount, user["id"]))
            exec_write("INSERT INTO `TRANSACTION` (transactionid, accno, transactiontype, amount, makerid) VALUES (%s,%s,'DEPOSIT',%s,%s)",
                       (str(uuid.uuid4()), to_acc, amount, user["id"]))
            st.success(f"Transfer successful: {tr_id}")
        except Error as e:
            st.error(f"Transfer failed: {e}")

    st.subheader("Recent Transfers")
    st.dataframe(fetch_all("SELECT * FROM TRANSFERS ORDER BY transferdate DESC LIMIT 50"), use_container_width=True)

# ---------- Loans ----------
def loans_page():
    st.header("🏡 Loans")
    role = st.session_state["role"]
    user = st.session_state["user"]

    with st.form("loan_apply"):
        st.subheader("Apply for Loan")
        loan_id = st.text_input("Loan ID")
        cif = st.text_input("CIF")
        accno = st.text_input("Linked Account No")
        loan_amt = st.number_input("Loan Amount", min_value=0.01, step=0.01)
        loan_type = st.selectbox("Type", ["HOME","AUTO","PERSONAL"])
        rate = st.number_input("Interest Rate (%)", min_value=0.00, value=9.50, step=0.25)
        tenure = st.number_input("Tenure (months)", min_value=1, step=1)
        submitted = st.form_submit_button("Apply")
    if submitted and loan_id and cif and accno and loan_amt > 0:
        exec_write(
            "INSERT INTO LOANS (loan_id,cif,accno,loan_amount,loan_type,interest_rate,tenure_months,status) VALUES (%s,%s,%s,%s,%s,%s,%s,'PENDING')",
            (loan_id, cif, accno, loan_amt, loan_type, rate, tenure)
        )
        st.success("Loan application submitted.")

    st.subheader("All Loans")
    st.dataframe(fetch_all("SELECT loan_id,cif,accno,loan_amount,loan_type,interest_rate,tenure_months,status,approval_date,approved_by FROM LOANS ORDER BY loan_id"), use_container_width=True)

    if role == "admin":
        st.subheader("Approve Loan (Stored Procedure)")
        target = st.text_input("Loan ID to approve")
        if st.button("Approve"):
            try:
                call_proc("sp_approve_loan", (target, st.session_state["user"]["id"]))
                st.success("Loan approved via stored procedure.")
            except Error as e:
                st.error(f"Approval failed: {e}")

# ---------- Audit Logs ----------
def audit_logs_page():
    st.header("🧾 Audit Logs (Admin)")
    st.dataframe(fetch_all("SELECT * FROM AUDIT_LOGS ORDER BY timestamp DESC LIMIT 200"), use_container_width=True)

# ---------- Reports ----------
def reports_page():
    st.header("📈 Reports")
    st.subheader("Join: Customer + Account details")
    join_rows = fetch_all("""
        SELECT c.cif, c.fname, a.accno, a.balance
        FROM CUSTOMER c
        JOIN ACCOUNTS a ON c.cif = a.cif
        ORDER BY c.cif
    """)
    st.dataframe(join_rows, use_container_width=True)

    st.subheader("Nested: High Value Customers (balance > 50,000)")
    hv_rows = fetch_all("""
        SELECT * FROM CUSTOMER
        WHERE cif IN (SELECT cif FROM ACCOUNTS WHERE balance > 50000)
    """)
    st.dataframe(hv_rows, use_container_width=True)

    st.subheader("Aggregate: Total Deposits per Account")
    agg_rows = fetch_all("""
        SELECT accno, SUM(amount) AS total_deposits
        FROM `TRANSACTION`
        WHERE transactiontype = 'DEPOSIT'
        GROUP BY accno
        ORDER BY accno
    """)
    st.dataframe(agg_rows, use_container_width=True)

    st.subheader("Function demo: Interest for custom inputs")
    col1, col2, col3 = st.columns(3)
    with col1:
        principal = st.number_input("Principal", min_value=0.00, value=100000.00, step=1000.00)
    with col2:
        rate = st.number_input("Rate (%)", min_value=0.00, value=8.50, step=0.25)
    with col3:
        months = st.number_input("Months", min_value=1, value=12, step=1)

    if st.button("Calculate (fn_calculate_interest)"):
        val = call_scalar_function("SELECT fn_calculate_interest(%s,%s,%s)", (principal, rate, months))
        st.info(f"Calculated Interest: ₹ {val:.2f}" if val is not None else "No value returned.")

# ---------- Main ----------
def main():
    if "role" not in st.session_state:
        st.session_state["role"] = None
    if "user" not in st.session_state:
        st.session_state["user"] = None

    if get_conn() is None:
        st.error("⚠️ Could not connect to database. Please check MySQL is running.")
        return

    if not st.session_state["role"]:
        show_login()
        return

    with st.sidebar:
        st.write(f"Logged in as: **{st.session_state['user'].get('id','')}** ({st.session_state['role']})")
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()

    page = nav_bar()
    role = st.session_state["role"]

    if page == "Dashboard":
        dashboard()
    elif page == "Customers":
        if role == "admin": customers_page()
        else: st.error("Unauthorized")
    elif page == "Employees":
        if role == "admin": employees_page()
        else: st.error("Unauthorized")
    elif page == "Accounts":
        accounts_page(employee_mode=True)
    elif page == "My Accounts":
        accounts_page(employee_mode=False)
    elif page == "Transactions":
        if role in ("admin","employee"): transactions_page()
        else: st.error("Unauthorized")
    elif page == "Transfers":
        if role in ("admin","employee"): transfers_page()
        else: st.error("Unauthorized")
    elif page == "Loans":
        if role in ("admin","employee"): loans_page()
        else: st.error("Unauthorized")
    elif page == "Audit Logs":
        if role == "admin": audit_logs_page()
        else: st.error("Unauthorized")
    elif page == "Reports":
        reports_page()

if __name__ == "__main__":
    main()
