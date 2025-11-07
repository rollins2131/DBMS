# app.py — Enhanced UI with AI Chatbot (Complete Version)
import os
import uuid
import streamlit as st
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import requests

# ---------- Streamlit Config ----------
st.set_page_config(
    page_title="🏦 Bank Management System", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for attractive UI
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid #3d3d5c;
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        color: #e0e0e0;
        font-weight: 500;
        font-size: 1.05rem;
    }
    
    h1, h2, h3 {
        color: #e8e8f0 !important;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stDataFrame"] {
        background: rgba(45, 45, 68, 0.6);
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #3d3d5c;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        background-color: #2d2d44;
        color: #e0e0e0;
        border: 1px solid #4a4a6a;
        border-radius: 8px;
        padding: 0.6rem;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #5865F2 0%, #4752C4 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(88, 101, 242, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(88, 101, 242, 0.4);
    }
    
    [data-testid="stMetricValue"] {
        color: #5865F2;
        font-size: 2rem;
        font-weight: 700;
    }
    
    .chat-container {
        background: linear-gradient(135deg, #2d2d44 0%, #3d3d5c 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #4a4a6a;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
    }
    
    .chat-message {
        padding: 0.8rem 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        max-width: 80%;
        word-wrap: break-word;
    }
    
    .user-message {
        background: linear-gradient(135deg, #5865F2 0%, #4752C4 100%);
        color: white;
        margin-left: auto;
        text-align: right;
    }
    
    .bot-message {
        background: rgba(45, 45, 68, 0.8);
        color: #e0e0e0;
        border: 1px solid #4a4a6a;
    }
    
    .login-container {
        background: rgba(45, 45, 68, 0.6);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid #4a4a6a;
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.5);
        max-width: 500px;
        margin: 2rem auto;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #2d2d44;
        border-radius: 8px 8px 0 0;
        color: #a0a0b0;
        padding: 0.8rem 1.5rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #5865F2 0%, #4752C4 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

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

# ---------- AI Chatbot Function ----------
def get_chatbot_response(user_message, context=""):
    """Simulate AI chatbot responses - Replace with actual API when deploying"""
    # In production, you would need to add your Anthropic API key here
    # For now, this provides rule-based responses
    
    user_message_lower = user_message.lower()
    
    # Account-related queries
    if any(word in user_message_lower for word in ['account', 'balance', 'open account', 'account type']):
        return """I can help you with account-related questions! Here's what you need to know:

**Account Types:**
- Savings Account: For regular savings with interest
- Current Account: For business transactions
- Recurring Account: For regular monthly deposits

**To check your balance:** Go to the 'My Accounts' section in the dashboard.
**To open a new account:** Please visit your branch or contact a bank representative."""

    # Transaction queries
    elif any(word in user_message_lower for word in ['transaction', 'deposit', 'withdraw', 'transfer']):
        return """For transactions, here's what you can do:

**Deposits & Withdrawals:** Visit the 'Transactions' page to deposit or withdraw money from your accounts.

**Transfers:** Use the 'Transfers' page to move money between accounts. You'll need the recipient's account number.

All transactions are processed securely and appear in your transaction history immediately."""

    # Loan queries
    elif any(word in user_message_lower for word in ['loan', 'borrow', 'credit', 'emi']):
        return """I can help you with loan information:

**Loan Types Available:**
- Home Loan: For purchasing property
- Auto Loan: For vehicle purchases
- Personal Loan: For personal needs

**To apply:** Go to the 'Loans' section and fill out the application form. You'll need to link it to one of your accounts. Your application will be reviewed by our team.

**Interest rates** vary by loan type and tenure. Typical rates range from 8-12% annually."""

    # Interest rate queries
    elif any(word in user_message_lower for word in ['interest', 'rate', 'calculate']):
        return """Interest rates vary by account type:

**Savings Account:** Typically 3.5% - 4% per annum
**Fixed Deposits:** 5% - 7% per annum
**Loan Interest:** 8% - 12% depending on loan type

You can use the interest calculator in the 'Reports' section to estimate interest for different amounts and tenures."""

    # Greeting
    elif any(word in user_message_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
        user = st.session_state.get("user", {})
        name = user.get('fname', 'Customer')
        return f"""Hello {name}! 👋 Welcome to our banking assistant.

I can help you with:
- Account information and services
- Transaction guidance
- Loan applications and information
- Interest rate calculations
- General banking queries

What would you like to know about today?"""

    # Help/what can you do
    elif any(word in user_message_lower for word in ['help', 'what can you', 'how can you', 'assist']):
        return """I'm here to help you with:

✅ **Accounts** - Information about account types, opening accounts, checking balances
✅ **Transactions** - How to deposit, withdraw, and transfer money
✅ **Loans** - Loan types, application process, interest rates
✅ **Interest Rates** - Current rates and calculations
✅ **Security** - Account security and best practices
✅ **Services** - Available banking services and features

Just ask me any question about banking!"""

    # Security/safety
    elif any(word in user_message_lower for word in ['security', 'safe', 'secure', 'password', 'protect']):
        return """Your account security is our top priority:

🔒 **Security Tips:**
- Never share your password or CIF with anyone
- Log out after each session
- Regularly check your transaction history
- Report any suspicious activity immediately
- Use strong, unique passwords

**All transactions** are encrypted and monitored for fraud. If you notice any unauthorized activity, please contact us immediately."""

    # Name query
    elif any(word in user_message_lower for word in ['name', 'who are you', 'what are you']):
        return """I'm your banking assistant! I'm here to help you navigate our bank management system and answer any questions you have about:

- Your accounts and balances
- Making transactions
- Applying for loans
- Understanding our services
- Banking best practices

Feel free to ask me anything about banking!"""

    # Default response
    else:
        return f"""Thanks for your question! While I can provide general banking information, for specific details about "{user_message}", I recommend:

1. Checking the relevant section in your dashboard
2. Contacting a bank representative
3. Visiting your nearest branch

I can help with:
- Account information
- Transaction guidance
- Loan applications
- Interest calculations
- General banking queries

Is there anything else I can help you with?"""

# ---------- Authentication ----------
def login(user_id, password):
    emp = fetch_one(
        "SELECT pfno AS id, empname AS name, designation, password_hash FROM EMPLOYEE WHERE pfno=%s",
        (user_id,)
    )
    if emp:
        if password == emp["password_hash"]:
            role = "admin" if emp["designation"].lower() == "manager" else "employee"
            return role, emp
        return None, None

    cust = fetch_one(
        "SELECT cif AS id, fname, lname, password_hash FROM CUSTOMER WHERE cif=%s",
        (user_id,)
    )
    if cust and password == cust["password_hash"]:
        return "customer", cust
    return None, None

# ---------- UI Components ----------
def show_login():
    st.markdown("<div style='text-align: center; padding: 2rem 0;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 3rem;'>🏦 Bank Management System</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.2rem; color: #a0a0b0;'>Secure Banking Portal</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        with st.form("login_form"):
            st.markdown("### 🔐 Login")
            user_id = st.text_input("User ID", placeholder="e.g. E001 / C001")
            pwd = st.text_input("Password", type="password", placeholder="Enter password")
            submitted = st.form_submit_button("Sign In", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        role, profile = login(user_id.strip(), pwd)
        if role:
            st.session_state["role"] = role
            st.session_state["user"] = profile
            st.session_state["chat_history"] = []
            st.rerun()
        else:
            st.error("❌ Invalid credentials.")

def nav_bar():
    role = st.session_state["role"]
    user = st.session_state["user"]
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### 👤 {user.get('name', user.get('fname', 'User'))}")
    st.sidebar.markdown(f"**Role:** {role.title()}")
    st.sidebar.markdown(f"**ID:** {user.get('id', 'N/A')}")
    st.sidebar.markdown("---")
    
    st.sidebar.title("📋 Navigation")

    if role == "admin":
        return st.sidebar.radio("", [
            "📊 Dashboard", "👤 Customers", "👔 Employees", "🏦 Accounts", 
            "💰 Transactions", "🔄 Transfers", "🏡 Loans", "🧾 Audit Logs", "📈 Reports"
        ], label_visibility="collapsed")
    elif role == "employee":
        return st.sidebar.radio("", [
            "📊 Dashboard", "🏦 Accounts", "💰 Transactions", 
            "🔄 Transfers", "🏡 Loans", "📈 Reports"
        ], label_visibility="collapsed")
    else:
        return st.sidebar.radio("", [
            "📊 Dashboard", "💳 My Accounts", "💰 Transactions", 
            "🔄 Transfers", "🏡 Loans", "📈 Reports", "🤖 Banking Assistant"
        ], label_visibility="collapsed")

# ---------- Chatbot Page ----------
def chatbot_page():
    st.header("🤖 Banking Assistant")
    st.markdown("*Ask me anything about banking services*")
    
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    
    user = st.session_state["user"]
    accounts = fetch_all("SELECT accno, accttype, balance FROM ACCOUNTS WHERE cif=%s", (user["id"],))
    context = f"Customer: {user.get('fname', '')} {user.get('lname', '')} (CIF: {user['id']}), Accounts: {len(accounts)}"
    
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    
    for chat in st.session_state["chat_history"]:
        if chat["role"] == "user":
            st.markdown(f"<div class='chat-message user-message'><b>You:</b> {chat['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-message bot-message'><b>🤖:</b> {chat['content']}</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("", key="chat_input", label_visibility="collapsed", placeholder="Type your message...")
    with col2:
        send_button = st.button("Send", use_container_width=True)
    
    if send_button and user_input:
        st.session_state["chat_history"].append({"role": "user", "content": user_input})
        
        with st.spinner("🤔 Thinking..."):
            bot_response = get_chatbot_response(user_input, context)
        
        st.session_state["chat_history"].append({"role": "assistant", "content": bot_response})
        st.rerun()
    
    if st.button("🗑️ Clear Chat"):
        st.session_state["chat_history"] = []
        st.rerun()

# ---------- Dashboard ----------
def dashboard():
    st.header("📊 Dashboard")
    role = st.session_state["role"]
    user = st.session_state["user"]
    
    if role in ("admin", "employee"):
        st.markdown(f"### Welcome, **{user.get('name','Employee')}** 👋")
        
        total_customers = fetch_one("SELECT COUNT(*) as count FROM CUSTOMER")
        total_accounts = fetch_one("SELECT COUNT(*) as count FROM ACCOUNTS")
        total_balance = fetch_one("SELECT SUM(balance) as total FROM ACCOUNTS")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("👥 Customers", total_customers["count"] if total_customers else 0)
        with col2:
            st.metric("🏦 Accounts", total_accounts["count"] if total_accounts else 0)
        with col3:
            st.metric("💰 Total Balance", f"₹{total_balance['total']:,.2f}" if total_balance and total_balance['total'] else "₹0.00")
        
        st.markdown("---")
        st.subheader("📋 All Accounts")
        accounts = fetch_all("SELECT accno, cif, accttype, balance FROM ACCOUNTS ORDER BY accno")
        st.dataframe(accounts, use_container_width=True)
    else:
        st.markdown(f"### Welcome, **{user.get('fname','')} {user.get('lname','')}** 👋")
        
        accs = fetch_all("SELECT accno, accttype, balance FROM ACCOUNTS WHERE cif=%s", (user["id"],))
        total_balance = sum([acc["balance"] for acc in accs])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("💳 My Accounts", len(accs))
        with col2:
            st.metric("💰 Total Balance", f"₹{total_balance:,.2f}")
        
        st.markdown("---")
        st.subheader("💳 My Accounts")
        if accs:
            st.dataframe(accs, use_container_width=True)
        else:
            st.info("ℹ️ No accounts yet.")

# ---------- Customers Page ----------
def customers_page():
    st.header("👤 Customers Management")
    
    tab1, tab2 = st.tabs(["📝 Create/Update", "📊 View All"])
    
    with tab1:
        col = st.columns(2)
        with col[0]:
            with st.form("cust_form"):
                cif = st.text_input("CIF")
                fname = st.text_input("First Name")
                lname = st.text_input("Last Name")
                password_hash = st.text_input("Password")
                submitted = st.form_submit_button("💾 Save")
            if submitted and cif and fname and password_hash:
                exists = fetch_one("SELECT cif FROM CUSTOMER WHERE cif=%s", (cif,))
                if exists:
                    exec_write("UPDATE CUSTOMER SET fname=%s, lname=%s, password_hash=%s WHERE cif=%s",
                               (fname, lname, password_hash, cif))
                    st.success("✅ Updated.")
                else:
                    exec_write("INSERT INTO CUSTOMER (cif,fname,lname,password_hash) VALUES (%s,%s,%s,%s)",
                               (cif, fname, lname, password_hash))
                    st.success("✅ Created.")

        with col[1]:
            cif_del = st.text_input("CIF to delete")
            if st.button("🗑️ Delete"):
                exec_write("DELETE FROM CUSTOMER WHERE cif=%s", (cif_del,))
                st.info("ℹ️ Deleted.")
    
    with tab2:
        customers = fetch_all("SELECT cif, fname, lname, homebranch, opening_date FROM CUSTOMER")
        st.dataframe(customers, use_container_width=True)

# ---------- Employees Page ----------
def employees_page():
    st.header("👔 Employees Management")
    
    tab1, tab2 = st.tabs(["📝 Create/Update", "📊 View All"])
    
    with tab1:
        col = st.columns(2)
        with col[0]:
            with st.form("emp_form"):
                pfno = st.text_input("PF No")
                name = st.text_input("Name")
                desig = st.selectbox("Designation", ["Manager","Teller","Clerk","Officer"])
                pwd = st.text_input("Password")
                submitted = st.form_submit_button("💾 Save")
            if submitted and pfno and name and pwd:
                exists = fetch_one("SELECT pfno FROM EMPLOYEE WHERE pfno=%s", (pfno,))
                if exists:
                    exec_write("UPDATE EMPLOYEE SET empname=%s, designation=%s, password_hash=%s WHERE pfno=%s",
                               (name, desig, pwd, pfno))
                    st.success("✅ Updated.")
                else:
                    exec_write("INSERT INTO EMPLOYEE (pfno, empname, designation, password_hash) VALUES (%s,%s,%s,%s)",
                               (pfno, name, desig, pwd))
                    st.success("✅ Created.")

        with col[1]:
            pf_del = st.text_input("PF No to delete")
            if st.button("🗑️ Delete"):
                exec_write("DELETE FROM EMPLOYEE WHERE pfno=%s", (pf_del,))
                st.info("ℹ️ Deleted.")
    
    with tab2:
        employees = fetch_all("SELECT pfno, empname, designation, joining_date FROM EMPLOYEE")
        st.dataframe(employees, use_container_width=True)

# ---------- Accounts Page ----------
def accounts_page(employee_mode=True):
    if employee_mode:
        st.header("🏦 Accounts Management")
    else:
        st.header("💳 My Accounts")

    role = st.session_state["role"]
    user = st.session_state["user"]

    if role == "customer":
        rows = fetch_all("SELECT accno, accttype, balance, interest_rate FROM ACCOUNTS WHERE cif=%s", (user["id"],))
        if rows:
            st.dataframe(rows, use_container_width=True)
        else:
            st.info("ℹ️ No accounts.")
        return

    tab1, tab2 = st.tabs(["➕ Open Account", "📊 View All"])
    
    with tab1:
        with st.form("acct_open"):
            accno = st.text_input("Account No")
            cif = st.text_input("CIF")
            accttype = st.selectbox("Type", ["SAVINGS","CURRENT","RECURRING"])
            ir = st.number_input("Interest Rate (%)", value=3.50, step=0.25)
            opening = st.form_submit_button("🏦 Create")
        if opening and accno and cif:
            exec_write("INSERT INTO ACCOUNTS (accno,cif,accttype,interest_rate) VALUES (%s,%s,%s,%s)",
                       (accno, cif, accttype, ir))
            st.success("✅ Created.")

    with tab2:
        accounts = fetch_all("SELECT accno, cif, accttype, balance, interest_rate FROM ACCOUNTS")
        st.dataframe(accounts, use_container_width=True)

# ---------- Transactions ----------
def transactions_page():
    st.header("💰 Transactions")
    role = st.session_state["role"]
    user = st.session_state["user"]

    if role == "customer":
        customer_accounts = fetch_all("SELECT accno, balance FROM ACCOUNTS WHERE cif=%s", (user["id"],))
        if not customer_accounts:
            st.warning("⚠️ No accounts.")
            return
        
        acc_list = [f"{acc['accno']} (₹{acc['balance']:,.2f})" for acc in customer_accounts]
        acc_numbers = [acc["accno"] for acc in customer_accounts]
        
        with st.form("txn_form_customer"):
            accno_display = st.selectbox("Account", acc_list)
            accno = acc_numbers[acc_list.index(accno_display)]
            ttype = st.selectbox("Type", ["DEPOSIT","WITHDRAW"])
            amount = st.number_input("Amount (₹)", min_value=0.01, step=100.00)
            submitted = st.form_submit_button("✓ Process")
        
        if submitted and accno and amount > 0:
            txn_id = str(uuid.uuid4())
            try:
                exec_write(
                    "INSERT INTO `TRANSACTION` (transactionid, accno, transactiontype, amount, makerid, checkerid) VALUES (%s,%s,%s,%s,NULL,NULL)",
                    (txn_id, accno, ttype, amount)
                )
                st.success(f"✅ Success! ID: {txn_id[:8]}...")
            except Error as e:
                st.error(f"❌ Failed: {e}")

        st.markdown("---")
        st.subheader("📜 Recent Transactions")
        my_txns = fetch_all(
            "SELECT t.transactionid, t.accno, t.transactiontype, t.amount, t.transactiondate FROM `TRANSACTION` t WHERE t.accno IN (SELECT accno FROM ACCOUNTS WHERE cif=%s) ORDER BY t.transactiondate DESC LIMIT 50",
            (user["id"],)
        )
        if my_txns:
            st.dataframe(my_txns, use_container_width=True)
        else:
            st.info("ℹ️ No transactions.")
    else:
        with st.form("txn_form"):
            accno = st.text_input("Account No")
            ttype = st.selectbox("Type", ["DEPOSIT","WITHDRAW"])
            amount = st.number_input("Amount (₹)", min_value=0.01, step=100.00)
            checker = st.text_input("Checker PF No (optional)")
            submitted = st.form_submit_button("✓ Process")
        
        if submitted and accno and amount > 0:
            txn_id = str(uuid.uuid4())
            try:
                exec_write(
                    "INSERT INTO `TRANSACTION` (transactionid, accno, transactiontype, amount, makerid, checkerid) VALUES (%s,%s,%s,%s,%s,%s)",
                    (txn_id, accno, ttype, amount, user["id"], checker if checker else None)
                )
                st.success(f"✅ Success! ID: {txn_id[:8]}...")
            except Error as e:
                st.error(f"❌ Failed: {e}")

        st.markdown("---")
        st.subheader("📜 Recent Transactions")
        txns = fetch_all("SELECT transactionid, accno, transactiontype, amount, transactiondate, makerid FROM `TRANSACTION` ORDER BY transactiondate DESC LIMIT 50")
        st.dataframe(txns, use_container_width=True)

# ---------- Transfers ----------
def transfers_page():
    st.header("🔄 Fund Transfers")
    role = st.session_state["role"]
    user = st.session_state["user"]

    if role == "customer":
        customer_accounts = fetch_all("SELECT accno, balance FROM ACCOUNTS WHERE cif=%s", (user["id"],))
        if not customer_accounts:
            st.warning("⚠️ No accounts.")
            return
        
        acc_list = [f"{acc['accno']} (₹{acc['balance']:,.2f})" for acc in customer_accounts]
        acc_numbers = [acc["accno"] for acc in customer_accounts]
        
        with st.form("tr_form_customer"):
            from_acc_display = st.selectbox("From Account", acc_list)
            from_acc = acc_numbers[acc_list.index(from_acc_display)]
            to_acc = st.text_input("To Account")
            amount = st.number_input("Amount (₹)", min_value=0.01, step=100.00)
            submitted = st.form_submit_button("✓ Transfer")
        
        if submitted and from_acc and to_acc and amount > 0:
            tr_id = str(uuid.uuid4())
            try:
                exec_write("INSERT INTO TRANSFERS (transferid, from_accno, to_accno, amount) VALUES (%s,%s,%s,%s)",
                           (tr_id, from_acc, to_acc, amount))
                st.success(f"✅ Success! ID: {tr_id[:8]}...")
            except Error as e:
                st.error(f"❌ Failed: {e}")

        st.markdown("---")
        st.subheader("📜 Recent Transfers")
        my_transfers = fetch_all(
            "SELECT * FROM TRANSFERS WHERE from_accno IN (SELECT accno FROM ACCOUNTS WHERE cif=%s) OR to_accno IN (SELECT accno FROM ACCOUNTS WHERE cif=%s) ORDER BY transferdate DESC LIMIT 50",
            (user["id"], user["id"])
        )
        if my_transfers:
            st.dataframe(my_transfers, use_container_width=True)
        else:
            st.info("ℹ️ No transfers.")
    else:
        with st.form("tr_form"):
            from_acc = st.text_input("From Account")
            to_acc = st.text_input("To Account")
            amount = st.number_input("Amount (₹)", min_value=0.01, step=100.00)
            submitted = st.form_submit_button("✓ Transfer")
        
        if submitted and from_acc and to_acc and amount > 0:
            tr_id = str(uuid.uuid4())
            try:
                exec_write("INSERT INTO TRANSFERS (transferid, from_accno, to_accno, amount) VALUES (%s,%s,%s,%s)",
                           (tr_id, from_acc, to_acc, amount))
                st.success(f"✅ Success! ID: {tr_id[:8]}...")
            except Error as e:
                st.error(f"❌ Failed: {e}")

        st.markdown("---")
        st.subheader("📜 Recent Transfers")
        st.dataframe(fetch_all("SELECT * FROM TRANSFERS ORDER BY transferdate DESC LIMIT 50"), use_container_width=True)

# ---------- Loans ----------
def loans_page():
    st.header("🏡 Loans")
    role = st.session_state["role"]
    user = st.session_state["user"]

    if role == "customer":
        customer_accounts = fetch_all("SELECT accno FROM ACCOUNTS WHERE cif=%s", (user["id"],))
        if not customer_accounts:
            st.warning("⚠️ No accounts to link loan.")
            return
        
        acc_list = [acc["accno"] for acc in customer_accounts]
        
        with st.form("loan_apply_customer"):
            loan_id = st.text_input("Loan ID")
            accno = st.selectbox("Account", acc_list)
            loan_amt = st.number_input("Amount (₹)", min_value=0.01, step=1000.00)
            loan_type = st.selectbox("Type", ["HOME","AUTO","PERSONAL"])
            rate = st.number_input("Interest Rate (%)", min_value=0.00, value=9.50, step=0.25)
            tenure = st.number_input("Tenure (months)", min_value=1, step=1)
            submitted = st.form_submit_button("Apply")
        
        if submitted and loan_id and accno and loan_amt > 0:
            try:
                exec_write(
                    "INSERT INTO LOANS (loan_id,cif,accno,loan_amount,loan_type,interest_rate,tenure_months,status) VALUES (%s,%s,%s,%s,%s,%s,%s,'PENDING')",
                    (loan_id, user["id"], accno, loan_amt, loan_type, rate, tenure)
                )
                st.success("✅ Application submitted.")
            except Error as e:
                st.error(f"❌ Failed: {e}")

        st.markdown("---")
        st.subheader("My Loans")
        my_loans = fetch_all(
            "SELECT loan_id, accno, loan_amount, loan_type, interest_rate, tenure_months, status, approval_date FROM LOANS WHERE cif=%s ORDER BY loan_id",
            (user["id"],)
        )
        if my_loans:
            st.dataframe(my_loans, use_container_width=True)
        else:
            st.info("ℹ️ No loans yet.")
    else:
        # Employee/Admin flow
        with st.form("loan_apply"):
            st.subheader("Apply for Loan")
            loan_id = st.text_input("Loan ID")
            cif = st.text_input("CIF")
            accno = st.text_input("Linked Account No")
            loan_amt = st.number_input("Loan Amount (₹)", min_value=0.01, step=1000.00)
            loan_type = st.selectbox("Type", ["HOME","AUTO","PERSONAL"])
            rate = st.number_input("Interest Rate (%)", min_value=0.00, value=9.50, step=0.25)
            tenure = st.number_input("Tenure (months)", min_value=1, step=1)
            submitted = st.form_submit_button("Apply")
        
        if submitted and loan_id and cif and accno and loan_amt > 0:
            try:
                exec_write(
                    "INSERT INTO LOANS (loan_id,cif,accno,loan_amount,loan_type,interest_rate,tenure_months,status) VALUES (%s,%s,%s,%s,%s,%s,%s,'PENDING')",
                    (loan_id, cif, accno, loan_amt, loan_type, rate, tenure)
                )
                st.success("✅ Loan application submitted.")
            except Error as e:
                st.error(f"❌ Failed: {e}")

        st.markdown("---")
        st.subheader("All Loans")
        st.dataframe(fetch_all("SELECT loan_id,cif,accno,loan_amount,loan_type,interest_rate,tenure_months,status,approval_date,approved_by FROM LOANS ORDER BY loan_id"), use_container_width=True)

        if role == "admin":
            st.markdown("---")
            st.subheader("Approve Loan")
            target = st.text_input("Loan ID to approve")
            if st.button("✓ Approve Loan"):
                try:
                    call_proc("sp_approve_loan", (target, st.session_state["user"]["id"]))
                    st.success("✅ Loan approved.")
                except Error as e:
                    st.error(f"❌ Approval failed: {e}")

# ---------- Audit Logs ----------
def audit_logs_page():
    st.header("🧾 Audit Logs")
    st.dataframe(fetch_all("SELECT * FROM AUDIT_LOGS ORDER BY timestamp DESC LIMIT 200"), use_container_width=True)

# ---------- Reports ----------
def reports_page():
    st.header("📈 Reports")
    role = st.session_state["role"]
    
    if role == "customer":
        st.subheader("Calculate Interest")
        col1, col2, col3 = st.columns(3)
        with col1:
            principal = st.number_input("Principal (₹)", min_value=0.00, value=100000.00, step=1000.00)
        with col2:
            rate = st.number_input("Rate (%)", min_value=0.00, value=8.50, step=0.25)
        with col3:
            months = st.number_input("Months", min_value=1, value=12, step=1)

        if st.button("Calculate"):
            val = call_scalar_function("SELECT fn_calculate_interest(%s,%s,%s)", (principal, rate, months))
            st.info(f"Calculated Interest: ₹ {val:.2f}" if val is not None else "No value returned.")
    else:
        st.subheader("Customer + Account Details (JOIN)")
        join_rows = fetch_all("""
            SELECT c.cif, c.fname, a.accno, a.balance
            FROM CUSTOMER c
            JOIN ACCOUNTS a ON c.cif = a.cif
            ORDER BY c.cif
        """)
        st.dataframe(join_rows, use_container_width=True)

        st.markdown("---")
        st.subheader("High Value Customers (Nested Query)")
        hv_rows = fetch_all("""
            SELECT * FROM CUSTOMER
            WHERE cif IN (SELECT cif FROM ACCOUNTS WHERE balance > 50000)
        """)
        st.dataframe(hv_rows, use_container_width=True)

        st.markdown("---")
        st.subheader("Total Deposits per Account (Aggregate)")
        agg_rows = fetch_all("""
            SELECT accno, SUM(amount) AS total_deposits
            FROM `TRANSACTION`
            WHERE transactiontype = 'DEPOSIT'
            GROUP BY accno
            ORDER BY accno
        """)
        st.dataframe(agg_rows, use_container_width=True)

        st.markdown("---")
        st.subheader("Interest Calculator")
        col1, col2, col3 = st.columns(3)
        with col1:
            principal = st.number_input("Principal (₹)", min_value=0.00, value=100000.00, step=1000.00)
        with col2:
            rate = st.number_input("Rate (%)", min_value=0.00, value=8.50, step=0.25)
        with col3:
            months = st.number_input("Months", min_value=1, value=12, step=1)

        if st.button("Calculate"):
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

    if page == "📊 Dashboard":
        dashboard()
    elif page == "👤 Customers":
        if role == "admin": customers_page()
        else: st.error("Unauthorized")
    elif page == "👔 Employees":
        if role == "admin": employees_page()
        else: st.error("Unauthorized")
    elif page == "🏦 Accounts":
        accounts_page(employee_mode=True)
    elif page == "💳 My Accounts":
        accounts_page(employee_mode=False)
    elif page == "💰 Transactions":
        transactions_page()
    elif page == "🔄 Transfers":
        transfers_page()
    elif page == "🏡 Loans":
        loans_page()
    elif page == "🧾 Audit Logs":
        if role == "admin": audit_logs_page()
        else: st.error("Unauthorized")
    elif page == "📈 Reports":
        reports_page()
    elif page == "🤖 Banking Assistant":
        if role == "customer": chatbot_page()
        else: st.error("Unauthorized")

if __name__ == "__main__":
    main()
