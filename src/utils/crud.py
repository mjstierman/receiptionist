import config
import sqlite3

from cs50 import SQL
from utils.schemas import receipt, account, address, category, merchant

db = SQL(config.database_url)

### CRATE NEW DATABASE ###
def create_db(schema_file):
    """ Create a new database file from schema """
    # Read the schema file
    schema = open(schema_file, "r").read()
    # Create the database
    db = open("app.db", "w")
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    # Execute the schema statements
    for statement in schema.split(';'):
        statement = statement.strip()
        if statement:  # Check if the statement is not empty
            cursor.execute(statement)
    conn.commit()
    conn.close()
    db.close()

### CRUD OPERATIONS FOR RECEIPTS ###
# insert
# update
# delete
# get by id
def insert_receipt(receipt: receipt):
    """ Insert a new receipt into the database """
    query = """
        INSERT INTO receipts (date, category, tags, items, merchant, location, account, amount, income, image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    db.execute(query, receipt.date, receipt.category, str(receipt.tags), str(receipt.items), receipt.merchant, receipt.location, receipt.account, receipt.amount, receipt.income, receipt.image)

def update_receipt(receipt_id: int, receipt: receipt):
    """ Update an existing receipt in the database """
    query = """
        UPDATE receipts
        SET date = ?, category = ?, tags = ?, items = ?, merchant = ?, location = ?, account = ?, amount = ?, income = ?, image = ?
        WHERE id = ?
    """
    db.execute(query, receipt.date, receipt.category, str(receipt.tags), str(receipt.items), receipt.merchant, receipt.location, receipt.account, receipt.amount, receipt.income, receipt.image, receipt_id)

def delete_receipt(receipt_id: int):
    """ Delete a receipt from the database """
    query = "DELETE FROM receipts WHERE id = ?"
    db.execute(query, receipt_id)

def get_receipt(receipt_id: int) -> receipt:
    """ Get a receipt from the database by ID """
    query = "SELECT * FROM receipts WHERE id = ?"
    result = db.execute(query, receipt_id)
    if result:
        return receipt(**result[0])  # Convert dict to receipt object
    return None

### CRUD OPERATIONS FOR ACCOUNTS ###
# insert
# update
# delete
# get by id
def insert_account(account: account):
    """ Insert a new account into the database """
    query = """
        INSERT INTO accounts (name, merchant, lastfour, balance)
        VALUES (?, ?, ?, ?)
    """
    db.execute(query, account.name, account.merchant, account.lastfour, account.balance)

def update_account(account_id: int, account: account):
    """ Update an existing account in the database """
    query = """
        UPDATE accounts
        SET name = ?, merchant = ?, lastfour = ?, balance = ?
        WHERE id = ?
    """
    db.execute(query, account.name, account.merchant, account.lastfour, account.balance, account_id)

def delete_account(account_id: int):
    """ Delete an account from the database """
    query = "DELETE FROM accounts WHERE id = ?"
    db.execute(query, account_id)

def get_account(account_id: int) -> account:
    """ Get an account from the database by ID """
    query = "SELECT * FROM accounts WHERE id = ?"
    result = db.execute(query, account_id)
    if result:
        return account(**result[0])  # Convert dict to account object
    return None

### CRUD OPERATIONS FOR ADDRESS ###
# insert
# update
# delete
# get by id

def insert_address(address: address):
    """ Insert a new address into the database """
    query = """
        INSERT INTO addresses (name, street1, street2, city, state, postal, country)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    db.execute(query, address.name, address.street1, address.street2, address.city, address.state, address.postal, address.country)

def update_address(address_id: int, address: address):
    """ Update an existing address in the database """
    query = """
        UPDATE addresses
        SET name = ?, street1 = ?, street2 = ?, city = ?, state = ?, postal = ?, country = ?
        WHERE id = ?
    """
    db.execute(query, address.name, address.street1, address.street2, address.city, address.state, address.postal, address.country, address_id)

def delete_address(address_id: int):
    """ Delete an address from the database """
    query = "DELETE FROM addresses WHERE id = ?"
    db.execute(query, address_id)

def get_address(address_id: int) -> address:
    """ Get an address from the database by ID """
    query = "SELECT * FROM addresses WHERE id = ?"
    result = db.execute(query, address_id)
    if result:
        return address(**result[0])  # Convert dict to address object
    return None

### CRUD OPERATIONS FOR CATEGORIES ###
# insert
# update
# delete
# get by id
def insert_category(category: category):
    """ Insert a new category into the database """
    query = "INSERT INTO categories (name) VALUES (?)"
    db.execute(query, category.name)

def update_category(category_id: int, category: category):
    """ Update an existing category in the database """
    query = "UPDATE categories SET name = ? WHERE id = ?"
    db.execute(query, category.name, category_id)

def delete_category(category_id: int):
    """ Delete a category from the database """
    query = "DELETE FROM categories WHERE id = ?"
    db.execute(query, category_id)

def get_category(category_id: int) -> category:
    """ Get a category from the database by ID """
    query = "SELECT * FROM categories WHERE id = ?"
    result = db.execute(query, category_id)
    if result:
        return category(**result[0])  # Convert dict to category object
    return None

### CRUD OPERATIONS FOR MERCHANTS ###
# insert
# update
# delete
# get by id

def insert_merchant(merchant: merchant):
    """ Insert a new merchant into the database """
    query = "INSERT INTO merchants (name, location) VALUES (?, ?)"
    db.execute(query, merchant.name, merchant.location)

def update_merchant(merchant_id: int, merchant: merchant):
    """ Update an existing merchant in the database """
    query = "UPDATE merchants SET name = ?, location = ? WHERE id = ?"
    db.execute(query, merchant.name, merchant.location, merchant_id)

def delete_merchant(merchant_id: int):
    """ Delete a merchant from the database """
    query = "DELETE FROM merchants WHERE id = ?"
    db.execute(query, merchant_id)

def get_merchant(merchant_id: int) -> merchant:
    """ Get a merchant from the database by ID """
    query = "SELECT * FROM merchants WHERE id = ?"
    result = db.execute(query, merchant_id)
    if result:
        return merchant(**result[0])  # Convert dict to merchant object
    return None

