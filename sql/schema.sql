CREATE TABLE users(
    user_ID VARCHAR(10) PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    date_joined DATE DEFAULT CURRENT_DATE
);

CREATE TABLE wallets(
    wallet_ID VARCHAR(10) PRIMARY KEY, 
    user_ID VARCHAR(10) NOT NULL,
    FOREIGN KEY(user_ID) REFERENCES users(user_ID),
    balance NUMERIC DEFAULT 0.00 CHECK(balance >= 0.00),
    status VARCHAR(6) DEFAULT 'active' CHECK(status = 'active' OR status = 'closed'), 
    date_created DATE DEFAULT CURRENT_DATE
);

CREATE TABLE transactions(
    transaction_ID VARCHAR(10) PRIMARY KEY, 
    wallet_ID VARCHAR(10) NOT NULL,
    FOREIGN KEY(wallet_ID) REFERENCES wallets(wallet_ID),
    type VARCHAR(10) NOT NULL CHECK(type = 'withdraw' OR type = 'deposit'), 
    amount NUMERIC NOT NULL CHECK(amount > 0.00),
    time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);