# 🏦 FinanceHub - Banking Management Platform

A comprehensive banking management system built with Python, Streamlit, and MySQL featuring role-based access control, real-time transactions, loan management, and AI-powered customer assistance.


## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Docker Deployment](#docker-deployment)
- [Database Setup](#database-setup)
- [Usage](#usage)
- [User Roles](#user-roles)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### 🔐 Role-Based Access Control
- **Admin (Manager)**: Full system access including employee management, loan approvals, and audit logs
- **Employee**: Account management, transaction processing, and customer service
- **Customer**: Self-service banking including transactions, transfers, and loan applications

### 💰 Core Banking Operations
- **Account Management**: Create and manage savings, current, and recurring accounts
- **Transactions**: Deposit and withdrawal with real-time balance updates
- **Fund Transfers**: Secure inter-account transfers with instant processing
- **Loan Management**: Apply for home, auto, and personal loans with approval workflow

### 🤖 AI-Powered Features
- **Banking Assistant Chatbot**: 24/7 customer support for common queries
- **Balance Inquiries**: Real-time account balance checking
- **Interest Calculator**: Calculate loan and deposit interest
- **Quick Actions**: Pre-configured responses for common banking questions

### 📊 Advanced Database Features
- **Triggers**: Automatic balance updates and audit logging
- **Stored Procedures**: Loan approval and transfer processing
- **Functions**: Interest calculation and balance computation
- **Complex Queries**: JOIN, nested queries, and aggregate functions

### 🎨 Modern UI/UX
- Elegant dark theme with gradient accents
- Responsive design for all screen sizes
- Real-time data updates
- Interactive dashboards with metrics
- Smooth animations and transitions

### 🔒 Security Features
- Password-based authentication
- Role-based authorization
- Audit logging for all transactions
- Maker-Checker workflow for critical operations

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Python web framework)
- **Backend**: Python 3.9+
- **Database**: MySQL 8.0+
- **Connector**: mysql-connector-python
- **Containerization**: Docker & Docker Compose

## 📦 Prerequisites

### Option 1: Local Installation
- Python 3.9 or higher
- MySQL 8.0 or higher
- pip (Python package manager)

### Option 2: Docker Installation
- Docker Desktop 20.10+
- Docker Compose 2.0+

## 🚀 Installation

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/financehub.git
cd financehub
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure database**
```bash
# Edit the database configuration in app.py or set environment variables
export DB_HOST=localhost
export DB_USER=root
export DB_PASS=your_password
export DB_NAME=mybank
```

5. **Initialize database**
```bash
mysql -u root -p < DBMSmini.sql
```

6. **Run the application**
```bash
streamlit run app.py
```

7. **Access the application**
```
Open browser at: http://localhost:8501
```

## 🐳 Docker Deployment

### Quick Start with Docker Compose

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/financehub.git
cd financehub
```

2. **Start the application**
```bash
docker-compose up -d
```

3. **Access the application**
```
Application: http://localhost:8501
MySQL: localhost:3306
```

4. **View logs**
```bash
docker-compose logs -f
```

5. **Stop the application**
```bash
docker-compose down
```

### Manual Docker Build

```bash
# Build the image
docker build -t financehub:latest .

# Run MySQL container
docker run -d \
  --name financehub-mysql \
  -e MYSQL_ROOT_PASSWORD=1234 \
  -e MYSQL_DATABASE=mybank \
  -p 3306:3306 \
  mysql:8.0

# Initialize database
docker exec -i financehub-mysql mysql -uroot -p1234 mybank < DBMSmini.sql

# Run application container
docker run -d \
  --name financehub-app \
  --link financehub-mysql:mysql \
  -e DB_HOST=mysql \
  -e DB_USER=root \
  -e DB_PASS=1234 \
  -e DB_NAME=mybank \
  -p 8501:8501 \
  financehub:latest
```

## 💾 Database Setup

The database schema includes:

### Tables
- **CUSTOMER**: Customer information and credentials
- **EMPLOYEE**: Employee details with role assignments
- **ACCOUNTS**: Bank accounts with balance tracking
- **TRANSACTION**: All deposit/withdrawal transactions
- **TRANSFERS**: Inter-account transfer records
- **LOANS**: Loan applications and approvals
- **AUDIT_LOGS**: System activity and transaction logs

### Triggers
- `trg_after_transaction_insert`: Auto-update account balance
- `trg_after_transfer_insert`: Process transfer and update balances

### Stored Procedures
- `sp_approve_loan`: Approve loan and credit amount
- `sp_transfer_amount`: Process fund transfers

### Functions
- `fn_calculate_interest`: Calculate interest for loans/deposits
- `fn_get_balance`: Get current account balance

## 📖 Usage

### Default Login Credentials

**Admin Access:**
- User ID: `E001`
- Password: `1234`
- Role: Manager (Full Access)

**Employee Access:**
- User ID: `E002`, `E003`, `E004`, `E005`
- Password: `abcd`
- Role: Employee (Limited Access)

**Customer Access:**
- User ID: `C001`, `C002`, `C003`, `C004`, `C005`
- Password: `1234`
- Role: Customer (Self-Service)

### Common Operations

#### For Customers:
1. **Check Balance**: Dashboard → View account balances
2. **Make Deposit**: Transactions → Select account → Choose DEPOSIT → Enter amount
3. **Withdraw Funds**: Transactions → Select account → Choose WITHDRAW → Enter amount
4. **Transfer Money**: Transfers → Select from account → Enter to account → Amount
5. **Apply for Loan**: Loans → Fill loan details → Submit application
6. **Ask Assistant**: AI Assistant → Type question or use quick actions

#### For Employees:
1. **Open Account**: Accounts → Enter customer details → Create account
2. **Process Transaction**: Transactions → Enter account number → Process
3. **View Reports**: Reports → Access various analytics

#### For Admins:
1. **Manage Users**: Customers/Employees → Create/Update/Delete
2. **Approve Loans**: Loans → Enter loan ID → Approve
3. **View Audit Logs**: Audit Logs → Monitor all activities

## 👥 User Roles

| Role | Permissions |
|------|-------------|
| **Admin (Manager)** | Full access: Customer management, Employee management, Account operations, Loan approvals, Audit logs, Reports |
| **Employee** | Limited access: Account operations, Transaction processing, Customer service, Reports |
| **Customer** | Self-service: View accounts, Make transactions, Transfer funds, Apply for loans, Use AI assistant |

## 📁 Project Structure

```
financehub/
│
├── app.py                  # Main application file
├── DBMSmini.sql           # Database schema and sample data
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker image configuration
├── docker-compose.yml    # Docker Compose configuration
├── .dockerignore        # Docker ignore file
├── README.md            # Project documentation
│
└── docs/                # Additional documentation (optional)
    ├── API.md
    ├── DEPLOYMENT.md
    └── SCREENSHOTS.md
```

## 🖼️ Screenshots

### Login Page
Professional login interface with secure authentication

### Dashboard
Role-specific dashboard with key metrics and account overview

### Transactions
Intuitive transaction interface with real-time balance updates

### AI Assistant
Intelligent chatbot for customer support and quick actions

### Reports
Comprehensive analytics with JOIN, nested, and aggregate queries

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Streamlit for the amazing web framework
- MySQL for robust database management
- Docker for containerization support

## 📧 Contact

Project Link: [https://github.com/yourusername/financehub](https://github.com/yourusername/financehub)

## 🐛 Known Issues

- None reported yet

## 🔮 Future Enhancements

- [ ] Two-factor authentication
- [ ] Email notifications for transactions
- [ ] Mobile app integration
- [ ] Advanced analytics dashboard
- [ ] Real-time chat support
- [ ] Biometric authentication
- [ ] Multi-currency support
- [ ] API for third-party integrations

## 📊 Database Statistics

- **8 Tables**: Comprehensive banking data model
- **2 Triggers**: Automated balance management
- **2 Stored Procedures**: Complex transaction processing
- **2 Functions**: Reusable calculations
- **3 User Roles**: Granular access control

---

**Made with ❤️ for modern banking solutions**
