CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    merchant INTEGER,
    lastfour INTEGER,
    balance DECIMAL(30, 2) DEFAULT 0.00 NOT NULL,
    FOREIGN KEY (merchant) REFERENCES merchants(id)
);

CREATE TABLE addresses (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    street1 TEXT,
    street2 TEXT,
    city TEXT NOT NULL,
    state TEXT,
    postal TEXT,
    country TEXT NOT NULL
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL
);

CREATE TABLE merchants (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    location INTEGER,
    FOREIGN KEY (location) REFERENCES addresses(id)
);

CREATE TABLE receipts (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    date DEFAULT CURRENT_TIMESTAMP NOT NULL,
    category INTEGER,
    tags TEXT,
    items TEXT,
    merchant INTEGER,
    location INTEGER,
    account INTEGER,
    amount DECIMAL(30, 2) NOT NULL,
    income BOOLEAN DEFAULT 0 NOT NULL,
    image BLOB,
    FOREIGN KEY (account) REFERENCES accounts(id),
    FOREIGN KEY (category) REFERENCES categories(id),
    FOREIGN KEY (location) REFERENCES addresses(id),
    FOREIGN KEY (merchant) REFERENCES merchants(id)
);

CREATE INDEX date ON receipts (date);