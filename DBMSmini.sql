CREATE DATABASE mybank;
USE mybank;


-- ======================================
-- STEP 2: Tables
-- ======================================

CREATE TABLE CUSTOMER (
  cif VARCHAR(20) PRIMARY KEY,
  fname VARCHAR(50) NOT NULL,
  lname VARCHAR(50),
  address TEXT,
  contact_no VARCHAR(15),
  identification_no VARCHAR(50) UNIQUE,
  birthdate DATE,
  gender CHAR(1),
  password_hash VARCHAR(255) NOT NULL,
  homebranch VARCHAR(50),
  opening_date DATE DEFAULT (CURRENT_DATE)
);

CREATE TABLE EMPLOYEE (
  pfno VARCHAR(20) PRIMARY KEY,
  empname VARCHAR(50) NOT NULL,
  designation VARCHAR(30),
  password_hash VARCHAR(255) NOT NULL,
  joining_date DATE DEFAULT (CURRENT_DATE),
  address TEXT
);

CREATE TABLE ACCOUNTS (
  accno VARCHAR(20) PRIMARY KEY,
  cif VARCHAR(20),
  accttype VARCHAR(20) NOT NULL,
  balance DECIMAL(12,2) DEFAULT 0,
  interest_rate DECIMAL(5,2),
  opening_date DATE DEFAULT (CURRENT_DATE),
  facility VARCHAR(50),
  FOREIGN KEY (cif) REFERENCES CUSTOMER(cif) ON DELETE CASCADE
);

CREATE TABLE `TRANSACTION` (
  transactionid VARCHAR(20) PRIMARY KEY,
  accno VARCHAR(20),
  transactiontype VARCHAR(20) NOT NULL,
  amount DECIMAL(12,2) NOT NULL,
  transactiondate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  makerid VARCHAR(20),
  checkerid VARCHAR(20),
  FOREIGN KEY (accno) REFERENCES ACCOUNTS(accno) ON DELETE CASCADE,
  FOREIGN KEY (makerid) REFERENCES EMPLOYEE(pfno),
  FOREIGN KEY (checkerid) REFERENCES EMPLOYEE(pfno)
);

CREATE TABLE TRANSFERS (
  transferid VARCHAR(20) PRIMARY KEY,
  from_accno VARCHAR(20),
  to_accno VARCHAR(20),
  amount DECIMAL(12,2) NOT NULL,
  transferdate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (from_accno) REFERENCES ACCOUNTS(accno) ON DELETE CASCADE,
  FOREIGN KEY (to_accno) REFERENCES ACCOUNTS(accno) ON DELETE CASCADE
);

CREATE TABLE LOANS (
  loan_id VARCHAR(20) PRIMARY KEY,
  cif VARCHAR(20),
  accno VARCHAR(20),
  loan_amount DECIMAL(12,2) NOT NULL,
  loan_type VARCHAR(30),
  interest_rate DECIMAL(5,2),
  tenure_months INT,
  approval_date DATE,
  status VARCHAR(20) DEFAULT 'PENDING',
  approved_by VARCHAR(20),
  FOREIGN KEY (cif) REFERENCES CUSTOMER(cif) ON DELETE CASCADE,
  FOREIGN KEY (accno) REFERENCES ACCOUNTS(accno) ON DELETE CASCADE,
  FOREIGN KEY (approved_by) REFERENCES EMPLOYEE(pfno)
);

CREATE TABLE AUDIT_LOGS (
  logid VARCHAR(20) PRIMARY KEY,
  user_id VARCHAR(20),
  user_type VARCHAR(20),
  action TEXT,
  ip_address VARCHAR(50),
  user_agent VARCHAR(100),
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  status_code VARCHAR(10)
);

-- ======================================
-- STEP 3: Insert sample data (5 each)
-- ======================================

INSERT INTO CUSTOMER VALUES
('C001','Ajay','Venkatesh','Bangalore','9999000001','ID001','2002-05-10','M','1234','Indiranagar','2024-01-01'),
('C002','Megha','Rao','Mysore','9999000002','ID002','2000-02-18','F','1234','Jayanagar','2024-01-02'),
('C003','Rahul','Shetty','Mangalore','9999000003','ID003','1999-08-20','M','1234','HSR','2024-01-03'),
('C004','Sneha','Patil','Hubli','9999000004','ID004','1998-03-05','F','1234','Malleshwaram','2024-01-04'),
('C005','Kiran','Naik','Belgaum','9999000005','ID005','1997-09-12','M','1234','Koramangala','2024-01-05');

INSERT INTO EMPLOYEE VALUES
('E001','John Doe','Manager','1234','2022-01-10','Bangalore'),
('E002','Priya Sharma','Clerk','abcd','2022-03-05','Mysore'),
('E003','Vikram Singh','Loan Officer','abcd','2023-02-20','Delhi'),
('E004','Aman Gupta','Cashier','abcd','2023-07-15','Udupi'),
('E005','Nikita Menon','Auditor','abcd','2023-10-01','Bangalore');

INSERT INTO ACCOUNTS VALUES
('A001','C001','SAVINGS',10000.00,3.5,'2024-01-01','ATM'),
('A002','C002','SAVINGS',8500.00,3.5,'2024-01-02','ATM'),
('A003','C003','CURRENT',25000.00,2.5,'2024-01-03','NetBanking'),
('A004','C004','SAVINGS',12000.00,3.5,'2024-01-04','ATM'),
('A005','C005','CURRENT',40000.00,2.5,'2024-01-05','NetBanking');

INSERT INTO `TRANSACTION` VALUES
('T001','A001','DEPOSIT',5000.00,NOW(),'E004','E002'),
('T002','A002','WITHDRAWAL',2000.00,NOW(),'E004','E002'),
('T003','A003','DEPOSIT',10000.00,NOW(),'E004','E002'),
('T004','A004','WITHDRAWAL',3000.00,NOW(),'E004','E002'),
('T005','A005','DEPOSIT',15000.00,NOW(),'E004','E002');

INSERT INTO TRANSFERS VALUES
('TR001','A001','A002',500.00,NOW()),
('TR002','A003','A004',1000.00,NOW()),
('TR003','A005','A001',2000.00,NOW()),
('TR004','A002','A003',1500.00,NOW()),
('TR005','A004','A005',1200.00,NOW());

INSERT INTO LOANS VALUES
('L001','C001','A001',100000.00,'Personal',8.5,12,'2024-04-01','APPROVED','E003'),
('L002','C002','A002',200000.00,'Home',7.0,60,'2024-04-02','APPROVED','E003'),
('L003','C003','A003',150000.00,'Car',9.0,36,NULL,'PENDING',NULL),
('L004','C004','A004',80000.00,'Personal',8.5,24,NULL,'PENDING',NULL),
('L005','C005','A005',300000.00,'Home',7.0,120,'2024-04-10','APPROVED','E003');

INSERT INTO AUDIT_LOGS VALUES
('LG001','C001','Customer','Login Success','127.0.0.1','Chrome',NOW(),'200'),
('LG002','C002','Customer','Password Reset','127.0.0.2','Firefox',NOW(),'200'),
('LG003','E003','Employee','Loan Approval','127.0.0.10','Edge',NOW(),'200'),
('LG004','E004','Employee','Deposit Transaction','127.0.0.11','Chrome',NOW(),'200'),
('LG005','C003','Customer','Transfer Initiated','127.0.0.3','Chrome',NOW(),'200');

-- ======================================
-- STEP 4: Trigger (single final version)
-- ======================================

DROP TRIGGER IF EXISTS trg_after_transaction_insert;
DELIMITER $$
CREATE TRIGGER trg_after_transaction_insert
AFTER INSERT ON `TRANSACTION`
FOR EACH ROW
BEGIN
  INSERT INTO AUDIT_LOGS (
    logid,
    user_id,
    user_type,
    action,
    ip_address,
    user_agent,
    timestamp,
    status_code
  )
  VALUES (
    CONCAT('LG', LPAD(FLOOR(RAND()*999)+1, 3, '0')),
    NEW.accno,
    'Customer',
    CONCAT('Transaction ', NEW.transactiontype),
    '127.0.0.1',
    'System',
    NOW(),
    '200'
  );
END$$
DELIMITER ;

-- ======================================
-- STEP 5: Test Query (optional)
-- ======================================
SELECT * FROM CUSTOMER;
SELECT * FROM ACCOUNTS;
SELECT * FROM EMPLOYEE;
SELECT * FROM `TRANSACTION`;
SELECT * FROM TRANSFERS;
SELECT * FROM LOANS;
SELECT * FROM AUDIT_LOGS;

-- stored procedure

DROP PROCEDURE IF EXISTS sp_transfer_amount;
DELIMITER $$
CREATE PROCEDURE sp_transfer_amount(
    IN p_from_acc VARCHAR(20),
    IN p_to_acc VARCHAR(20),
    IN p_amount DECIMAL(12,2),
    IN p_emp_id VARCHAR(20)
)
BEGIN
    START TRANSACTION;

    -- Deduct from source account
    UPDATE ACCOUNTS
    SET balance = balance - p_amount
    WHERE accno = p_from_acc;

    -- Add to destination account
    UPDATE ACCOUNTS
    SET balance = balance + p_amount
    WHERE accno = p_to_acc;

    -- Insert transfer record
    INSERT INTO TRANSFERS (transferid, from_accno, to_accno, amount)
    VALUES (CONCAT('TR', LPAD(FLOOR(RAND()*99999), 5, '0')), p_from_acc, p_to_acc, p_amount);

    -- Log action
    INSERT INTO AUDIT_LOGS (logid, user_id, user_type, action, ip_address, user_agent, status_code)
    VALUES (
        CONCAT('LG', LPAD(FLOOR(RAND()*999)+1, 3, '0')),
        p_emp_id,
        'Employee',
        CONCAT('Transferred ', p_amount, ' from ', p_from_acc, ' to ', p_to_acc),
        '127.0.0.1',
        'System',
        '200'
    );

    COMMIT;
END$$
DELIMITER ;



INSERT INTO `transaction` (transactionid, accno, transactiontype, amount, makerid, checkerid)
VALUES ('T1006', 'A001', 'DEPOSIT', 5000.00, 'E004', 'E002');


CALL sp_transfer_amount('A001', 'A002', 500.00, 'E004');
SELECT balance FROM ACCOUNTS WHERE accno IN ('A001','A002');
SELECT * FROM TRANSFERS ORDER BY transferdate DESC;
SELECT * FROM AUDIT_LOGS ORDER BY timestamp DESC;

-- functions
DROP FUNCTION IF EXISTS fn_get_balance;
DELIMITER $$
CREATE FUNCTION fn_get_balance(p_accno VARCHAR(20))
RETURNS DECIMAL(12,2)
DETERMINISTIC
BEGIN
    DECLARE total_in DECIMAL(12,2);
    DECLARE total_out DECIMAL(12,2);

    SELECT IFNULL(SUM(amount),0) INTO total_in 
    FROM `TRANSACTION` 
    WHERE accno = p_accno AND transactiontype = 'DEPOSIT';

    SELECT IFNULL(SUM(amount),0) INTO total_out 
    FROM `TRANSACTION` 
    WHERE accno = p_accno AND transactiontype = 'WITHDRAWAL';

    RETURN total_in - total_out;
END$$
DELIMITER ;

SELECT fn_get_balance('A001') AS CurrentBalance;

-- join
SELECT 
    l.loan_id,
    c.fname AS customer_firstname,
    c.lname AS customer_lastname,
    e.empname AS approved_by,
    l.loan_amount,
    l.loan_type,
    l.status
FROM LOANS l
JOIN CUSTOMER c ON l.cif = c.cif
LEFT JOIN EMPLOYEE e ON l.approved_by = e.pfno;


-- nested query

SELECT c.cif, c.fname, c.lname
FROM CUSTOMER c
WHERE c.cif IN (
    SELECT a.cif
    FROM ACCOUNTS a
    JOIN `TRANSACTION` t ON a.accno = t.accno
    GROUP BY a.cif
    HAVING SUM(
        CASE 
            WHEN t.transactiontype = 'DEPOSIT' THEN t.amount
            WHEN t.transactiontype = 'WITHDRAWAL' THEN -t.amount
            ELSE 0
        END
    ) > 10000
);

-- aggreagate function

SELECT 
    accno,
    SUM(CASE WHEN transactiontype = 'DEPOSIT' THEN amount ELSE 0 END) AS total_deposit,
    SUM(CASE WHEN transactiontype = 'WITHDRAWAL' THEN amount ELSE 0 END) AS total_withdrawal,
    SUM(
        CASE 
            WHEN transactiontype = 'DEPOSIT' THEN amount
            WHEN transactiontype = 'WITHDRAWAL' THEN -amount
            ELSE 0
        END
    ) AS net_balance
FROM `TRANSACTION`
GROUP BY accno
ORDER BY net_balance DESC;

ALTER TABLE TRANSACTION
MODIFY COLUMN transactionid VARCHAR(50);

SELECT TRIGGER_NAME, EVENT_OBJECT_TABLE, DEFINER
FROM INFORMATION_SCHEMA.TRIGGERS
WHERE TRIGGER_SCHEMA = 'mybank';

DROP TRIGGER IF EXISTS `mybank`.`tr_after_transaction_insert`;

DROP TRIGGER IF EXISTS `mybank`.`trg_after_transaction_insert`;
SHOW TRIGGERS;

DELIMITER $$

CREATE TRIGGER trg_after_transaction_insert
AFTER INSERT ON `TRANSACTION`
FOR EACH ROW
BEGIN
  DECLARE current_balance DECIMAL(15,2);

  -- 1️⃣ Get current balance of the account
  SELECT balance INTO current_balance
  FROM ACCOUNTS
  WHERE accno = NEW.accno
  FOR UPDATE;

  -- 2️⃣ Update balance based on transaction type
  IF NEW.transactiontype = 'DEPOSIT' THEN
    UPDATE ACCOUNTS
    SET balance = current_balance + NEW.amount
    WHERE accno = NEW.accno;

  ELSEIF NEW.transactiontype = 'WITHDRAW' THEN
    -- Optional: Prevent overdraft
    IF current_balance >= NEW.amount THEN
      UPDATE ACCOUNTS
      SET balance = current_balance - NEW.amount
      WHERE accno = NEW.accno;
    ELSE
      SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Insufficient funds for withdrawal';
    END IF;
  END IF;

  -- 3️⃣ If the account exists in other related tables (e.g., linked accounts)
  -- Example: If you have another table that mirrors balance
  -- UPDATE JOINT_ACCOUNTS SET balance = (SELECT balance FROM ACCOUNTS WHERE accno = NEW.accno)
  -- WHERE accno = NEW.accno;

  -- 4️⃣ Insert into audit logs
  INSERT INTO AUDIT_LOGS (
    logid,
    user_id,
    user_type,
    action,
    ip_address,
    user_agent,
    timestamp,
    status_code
  )
  VALUES (
    CONCAT('LG', LPAD(FLOOR(RAND() * 999) + 1, 3, '0')),
    NEW.accno,
    'Customer',
    CONCAT('Transaction ', NEW.transactiontype, ' of amount ', NEW.amount),
    '127.0.0.1',
    'System',
    NOW(),
    '200'
  );
END$$

DELIMITER ;

ALTER TABLE TRANSFERS 
MODIFY transferid VARCHAR(50);

SHOW CREATE TABLE TRANSFERS;

DELIMITER $$

CREATE TRIGGER trg_after_transfer_insert
AFTER INSERT ON TRANSFERS
FOR EACH ROW
BEGIN
    DECLARE from_balance DECIMAL(15,2);
    DECLARE to_balance DECIMAL(15,2);

    -- Get current balances
    SELECT balance INTO from_balance FROM ACCOUNTS WHERE accno = NEW.from_accno;
    SELECT balance INTO to_balance FROM ACCOUNTS WHERE accno = NEW.to_accno;

    -- Deduct from source account
    IF from_balance >= NEW.amount THEN
        UPDATE ACCOUNTS
        SET balance = from_balance - NEW.amount
        WHERE accno = NEW.from_accno;

        -- Credit to destination account
        UPDATE ACCOUNTS
        SET balance = to_balance + NEW.amount
        WHERE accno = NEW.to_accno;

        -- Add entry to audit logs
        INSERT INTO AUDIT_LOGS (
            logid,
            user_id,
            user_type,
            action,
            ip_address,
            user_agent,
            timestamp,
            status_code
        )
        VALUES (
            CONCAT('LG', LPAD(FLOOR(RAND()*999)+1, 3, '0')),
            NEW.from_accno,
            'Customer',
            CONCAT('Transferred ₹', NEW.amount, ' from ', NEW.from_accno, ' to ', NEW.to_accno),
            '127.0.0.1',
            'System',
            NOW(),
            '200'
        );
    ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Insufficient funds for transfer';
    END IF;
END$$

DELIMITER ;


DELIMITER $$

CREATE PROCEDURE sp_approve_loan(IN p_loan_id VARCHAR(20), IN p_emp_id VARCHAR(20))
BEGIN
    DECLARE v_accno VARCHAR(20);
    DECLARE v_amount DECIMAL(15,2);

    -- Get the account number and amount linked to the loan
    SELECT accno, loan_amount INTO v_accno, v_amount
    FROM LOANS
    WHERE loan_id = p_loan_id;

    -- Approve the loan
    UPDATE LOANS
    SET status = 'APPROVED',
        approval_date = CURRENT_DATE,
        approved_by = p_emp_id
    WHERE loan_id = p_loan_id;

    -- Credit the loan amount to the linked account
    UPDATE ACCOUNTS
    SET balance = balance + v_amount
    WHERE accno = v_accno;

    -- Add an audit log entry
    INSERT INTO AUDIT_LOGS (logid, user_id, user_type, action, ip_address, user_agent, timestamp, status_code)
    VALUES (
        CONCAT('LOG', UUID()),
        p_emp_id,
        'admin',
        CONCAT('Approved loan ID ', p_loan_id, ' and credited ₹', v_amount, ' to account ', v_accno),
        '127.0.0.1',
        'System',
        NOW(),
        '200'
    );
END$$

DELIMITER ;

SHOW PROCEDURE STATUS
WHERE Db = 'mybank';

DROP PROCEDURE IF EXISTS sp_approve_loan;

DELIMITER $$

CREATE PROCEDURE sp_approve_loan(
    IN p_loan_id VARCHAR(50),
    IN p_admin_id VARCHAR(50)
)
BEGIN
    DECLARE v_accno VARCHAR(50);
    DECLARE v_amount DECIMAL(15,2);

    -- 1. Get the linked account and loan amount
    SELECT accno, loan_amount
    INTO v_accno, v_amount
    FROM LOANS
    WHERE loan_id = p_loan_id;

    -- 2. Update loan status to APPROVED
    UPDATE LOANS
    SET status = 'APPROVED',
        approval_date = NOW(),
        approved_by = p_admin_id
    WHERE loan_id = p_loan_id;

    -- 3. Update account balance
    UPDATE ACCOUNTS
    SET balance = balance + v_amount
    WHERE accno = v_accno;

    -- 4. Add to AUDIT_LOGS
    INSERT INTO AUDIT_LOGS (
        logid,
        user_id,
        user_type,
        action,
        ip_address,
        user_agent,
        timestamp,
        status_code
    )
    VALUES (
        CONCAT('LG', LPAD(FLOOR(RAND()*999)+1, 3, '0')),
        v_accno,
        'Customer',
        CONCAT('Loan Approved for ', v_accno, ' Amount: ', v_amount),
        '127.0.0.1',
        'System',
        NOW(),
        '200'
    );
END$$

DELIMITER ;


