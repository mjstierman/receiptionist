""" Main application file for Receiptionist """

import logging
import config

from cs50 import SQL
from flask import Flask, render_template, redirect, request, Response

from utils.dashboards import top_ten_categories, this_month_receipts, this_month_spending
from utils.currency import to_currency, to_cents
from utils.time import append_timezone, to_UTC
from utils.files import to_base64

import utils.schemas as schemas
import utils.crud as crud

app = Flask(__name__)

# Configure logging
logger = logging.getLogger(__name__)

# Configure CS50 Library to use SQLite database
try:
    logging.info("Connecting to database at %s", config.database_url)
    db = SQL(config.database_url)
except Exception:
    logging.error("Database connection failed, creating new database using schema at %s", config.schema_path)
    db = crud.create_db(config.schema_path)

@app.route("/")
def index():
    """ Redirect to dashboard """
    return redirect("/dashboard")

@app.route("/layout")
def layout():
    """ Load the layout page """
    if db.execute("SELECT COUNT(*) as count FROM receipts")[0]['count'] <= 0:
        receipts = True
    return render_template("layout.html", receipts=receipts)

@app.route("/receipts", methods=["GET", "POST"])
def receipts():
    """ Load the home page """
    # Handle receipt actions first
    if request.form.get("delete"):
        # Get the receipt ID to delete
        receipt_id = request.form.get("delete")
        logging.info("Deleting receipt with ID: %s", receipt_id)
        try:
            crud.delete_receipt(receipt_id)
        except Exception as e:
            logging.error("Error deleting receipt with ID %s: %s", receipt_id, e)
            return redirect("/receipts") 
        return redirect("/receipts")
    
    if request.method == "POST":
        # Get the form data
        logging.debug("Received form data: %s", request.form)
        unsafe_datetime = request.form.get("datetime")
        unsafe_timezone = request.form.get("timezone")
        unsafe_category = request.form.get("category")
        unsafe_tags = request.form.get("tags")
        unsafe_items = request.form.get("items")
        unsafe_merchant = request.form.get("merchant")
        unsafe_location = request.form.get("location")
        unsafe_account = request.form.get("account")
        unsafe_amount = request.form.get("amount")
        unsafe_incomeFlag = request.form.get("income")
        unsafe_file = request.files['file']

        str_date = append_timezone(unsafe_datetime, unsafe_timezone)
        new_date = to_UTC(str_date)

        # Create a new receipt object with the validated data
        new_receipt = schemas.receipt(
            id = -1, # placeholder, will be set by the database or specified later
            date = new_date,
            category = unsafe_category if crud.get_category(unsafe_category) else None,
            tags = unsafe_tags if unsafe_tags else None,
            items = unsafe_items if unsafe_items else None,
            merchant = unsafe_merchant if crud.get_merchant(unsafe_merchant) else None,
            location = unsafe_location if crud.get_address(unsafe_location) else None,
            account = unsafe_account if crud.get_account(unsafe_account) else None,
            amount = to_cents(unsafe_amount),
            income = True if unsafe_incomeFlag == "1" else False,
            image = to_base64(unsafe_file) if unsafe_file else None
        )

        if request.form.get("id"):
            # Editing an existing receipt
            receipt_id = request.form.get("id")
            # Update the new_receipt before insertion
            new_receipt.id = receipt_id
        
        # Insert or Update the new receipt into the database
        try:
            if request.form.get("id"):
                logging.info("Updating receipt with ID: %s", receipt_id)
                crud.update_receipt(receipt_id, new_receipt)
            else:
                logging.info("Inserting new receipt into database.")
                crud.insert_receipt(new_receipt)
        except Exception as e:
            logging.error("Error inserting/updating receipt: %s", e)
            return redirect("/receipts")
        return redirect("/receipts")
    
    # Otherwise show the list of receipts
    else:
        receipts = db.execute("SELECT * FROM receipts")
        addresses = db.execute("SELECT id, name FROM addresses")
        merchants = db.execute("SELECT id, name FROM merchants")
        accounts = db.execute("SELECT id, name FROM accounts")
        categories = db.execute("SELECT id, name FROM categories")

        for receipt in receipts:
            location_id = receipt['location']
            if location_id:
                location_data = db.execute("SELECT name FROM addresses WHERE id = ?", location_id)
                receipt['location'] = location_data[0]['name'] if location_data else None

        for receipt in receipts:
            merchant_id = receipt['merchant']
            if merchant_id:
                merchant_data = db.execute("SELECT name FROM merchants WHERE id = ?", merchant_id)
                receipt['merchant'] = merchant_data[0]['name'] if merchant_data else None

        for receipt in receipts:
            account_id = receipt['account']
            if account_id:
                account_data = db.execute("SELECT name FROM accounts WHERE id = ?", account_id)
                receipt['account'] = account_data[0]['name'] if account_data else None

        for receipt in receipts:
            category_id = receipt['category']
            if category_id:
                category_data = db.execute("SELECT name FROM categories WHERE id = ?", category_id)
                receipt['category'] = category_data[0]['name'] if category_data else None

        return render_template("receipts.html", 
                               accounts=accounts,
                               addresses=addresses, 
                               receipts=receipts, 
                               merchants=merchants, 
                               categories=categories,
                               currency_symbol=config.currency_symbol)

@app.route("/receipt_image/<int:receipt_id>")
def receipt_image(receipt_id):
    """ Serve the receipt image file """
    receipt = db.execute("SELECT image FROM receipts WHERE id = ?", receipt_id)
    if receipt and receipt[0]['image']:
        return Response(receipt[0]['image'], mimetype='application/octet-stream')
    else:
        return "No image found", 404

@app.route("/addresses", methods=["GET", "POST"])
def addresses():
    """ Load the addresses page """
    # Handle address actions first
    if request.form.get("delete"):
        # Get the address ID to delete
        address_id = request.form.get("delete")
        logging.info("Deleting address with ID: %s", address_id)
        try:
            crud.delete_address(address_id)
        except Exception as e:
            logging.error("Error deleting address with ID %s: %s", address_id, e)
            return redirect("/addresses")
        return redirect("/addresses")
    
    if request.method == "POST":
        # Get the form data
        unsafe_name = request.form.get("name")
        unsafe_street1 = request.form.get("street1")
        unsafe_street2 = request.form.get("street2")
        unsafe_city = request.form.get("city")
        unsafe_state = request.form.get("state")
        unsafe_postal = request.form.get("postal")
        unsafe_country = request.form.get("country")

        # Validate the data
        new_address = schemas.address(
            id = -1, # placeholder, will be set by the database or specified later
            name = unsafe_name,
            street1 = unsafe_street1 if unsafe_street1 else None,
            street2 = unsafe_street2 if unsafe_street2 else None,
            city = unsafe_city if unsafe_city else None,
            state = unsafe_state if unsafe_state else None,
            postal = unsafe_postal if unsafe_postal else None,
            country = unsafe_country
        )
        
        # Check if editing an existing address
        if request.form.get("id"):
            # Editing an existing address
            address_id = request.form.get("id")
            logging.info("Editing address with ID: %s", address_id)

        # Insert or Update the extisting entry in the database
        try:
            if request.form.get("id"):
                logging.info("Updating address with ID: %s", address_id)
                crud.update_address(address_id, new_address)
            else:
                logging.info("Inserting new address '%s' into database.", new_address.name)
                crud.insert_address(new_address)
        except Exception as e:
            logging.error("Error inserting/updating receipt: %s", e)
            return redirect("/addresses")
        return redirect("/addresses")
    
    # Otherwise show the addresses page
    else:
        # check to see if there are any receipts to populate dashboard link
        receipts = db.execute("SELECT COUNT(*) as count FROM receipts")[0]['count'] > 0
        addresses = db.execute("SELECT * FROM addresses")
        logging.debug("Loaded addresses: %s", addresses)
        return render_template("addresses.html", addresses=addresses, receipts=receipts)

@app.route("/merchants", methods=["GET", "POST"])
def merchants():
    """ Load the merchants page """
    if request.form.get("delete"):
        # Get the merchant ID to delete
        merchant_id = request.form.get("delete")
        logging.info("Deleting merchant with ID: %s", merchant_id)
        try:
            crud.delete_merchant(merchant_id)
        except Exception as e:
            logging.error("Error deleting merchant with ID %s: %s", merchant_id, e)
            return redirect("/merchants") 
        return redirect("/merchants")
    
    if request.method == "POST":
        # Get the form data
        unsafe_name = request.form.get("name")
        unsafe_location = request.form.get("location")

        # Validate the data
        new_merchant = schemas.merchant(
            id = -1, # placeholder, will be set by the database or specified later
            name = unsafe_name,
            location = unsafe_location if unsafe_location else None
        )

        # Check if editing an existing merchant
        if request.form.get("id"):
            # Editing an existing merchant
            merchant_id = request.form.get("id")
            new_merchant.id = merchant_id
            logging.info("Editing merchant with ID: %s", merchant_id)

        # Insert or Update the extisting entry in the database
        try:
            if request.form.get("id"):
                logging.info("Updating merchant with ID: %s", merchant_id)
                crud.update_merchant(merchant_id, new_merchant)
            else:
                logging.info("Inserting new merchant '%s' into database.", new_merchant.name)
                crud.insert_merchant(new_merchant)
        except Exception as e:
            logging.error("Error inserting/updating merchant: %s", e)
            return redirect("/merchants")
        return redirect("/merchants")    
    
    # Otherwise show the merchants page
    else:
        # check to see if there are any receipts to populate dashboard link
        receipts = db.execute("SELECT COUNT(*) as count FROM receipts")[0]['count'] > 0
        merchants = db.execute("SELECT * FROM merchants")
        addresses = db.execute("SELECT id, name FROM addresses")

        for merchant in merchants:
            location_id = merchant['location']
            if location_id:
                location_data = db.execute("SELECT name FROM addresses WHERE id = ?", location_id)
                merchant['location'] = location_data[0]['name'] if location_data else None

        logging.debug("Loaded merchants: %s", merchants)
        return render_template("merchants.html", merchants=merchants, addresses=addresses, receipts=receipts)

@app.route("/accounts", methods=["GET", "POST"])
def accounts():
    """ Load the accounts page """
    if request.form.get("delete"):
        # Get the account ID to delete
        account_id = request.form.get("delete")
        logging.info("Deleting account with ID: %s", account_id)
        try: 
            crud.delete_account(account_id)
        except Exception as e:            
            logging.error("Error deleting account with ID %s: %s", account_id, e)
            return redirect("/accounts")
        return redirect("/accounts")
    
    if request.method == "POST":
        # Get the form data
        unsafe_name = request.form.get("name")
        unsafe_merchant = request.form.get("merchant")
        unsafe_lastfour = request.form.get("lastfour")
        unsafe_balance = request.form.get("balance")

        # Validate the data
        new_account = schemas.account(
            id = -1, # placeholder, will be set by the database or specified later
            name = unsafe_name,
            merchant = unsafe_merchant if unsafe_merchant else None,
            lastfour = unsafe_lastfour,
            balance = to_cents(unsafe_balance)
        )

        # Check if editing an existing account
        if request.form.get("id"):
            # Editing an existing account
            account_id = request.form.get("id")
            new_account.id = account_id
            logging.info("Editing account with ID: %s", account_id)
        
        # Insert or Update the extisting entry in the database
        try:
            if request.form.get("id"):
                logging.info("Updating account with ID: %s", account_id)
                crud.update_account(account_id, new_account)
            else:
                logging.info("Inserting new account '%s' into database.", new_account.name)
                crud.insert_account(new_account)
        except Exception as e:
            logging.error("Error inserting/updating account: %s", e)
            return redirect("/accounts")
        return redirect("/accounts")
    
    else:
        """ Otherwise show the accounts page"""
        # check to see if there are any receipts to populate dashboard link
        receipts = db.execute("SELECT COUNT(*) as count FROM receipts")[0]['count'] > 0
        accounts = db.execute("SELECT * FROM accounts")
        merchants = db.execute("SELECT id, name FROM merchants")
        accounts = db.execute("SELECT * FROM accounts")

        for account in accounts:
            merchant_id = account['merchant']
            if merchant_id:
                merchant_data = db.execute("SELECT name FROM merchants WHERE id = ?", merchant_id)
                account['merchant'] = merchant_data[0]['name'] if merchant_data else None
        logger.debug("Loaded accounts:", accounts)
        return render_template("accounts.html", accounts=accounts, merchants=merchants, receipts=receipts)

@app.route("/categories", methods=["GET", "POST"])
def categories():
    """ Load the categories page """
    if request.form.get("delete"):
        # Get the category ID to delete
        category_id = request.form.get("delete")
        logging.info("Deleting category with ID: %s", category_id)
        try:
            crud.delete_category(category_id)
        except Exception as e:
            logging.error("Error deleting category with ID %s: %s", category_id, e)
            return redirect("/categories")
        return redirect("/categories")
    
    if request.method == "POST":
        # Get the form data
        unsafe_name = request.form.get("name")

        # Validate the data
        new_category = schemas.category(
            id = -1, # placeholder, will be set by the database or specified later
            name = unsafe_name
        )

        if request.form.get("id"):
            # Editing an existing category
            category_id = request.form.get("id")
            logging.info("Editing category with ID: %s", category_id)
            new_category.id = category_id
        
        # Insert or Update the extisting entry in the database
        try:
            if request.form.get("id"):
                logging.info("Updating category with ID: %s", category_id)
                crud.update_category(category_id, new_category)
            else:
                logging.info("Inserting new category '%s' into database.", new_category.name)
                crud.insert_category(new_category)
        except Exception as e:
            logging.error("Error inserting/updating category: %s", e)
            return redirect("/categories")
        return redirect("/categories")
    
    else:
        """ Otherwise show the categories page"""
        # check to see if there are any receipts to populate dashboard link
        receipts = db.execute("SELECT COUNT(*) as count FROM receipts")[0]['count'] > 0
        Categories = db.execute("SELECT * FROM categories")
        logging.debug("Loaded categories: %s", Categories)
        return render_template("categories.html", Categories=Categories, receipts=receipts)

@app.route("/dashboard")
def dashboard():
    """ Load the dashboard page """
    # Check to make sure thee are receipts to show
    if db.execute("SELECT COUNT(*) as count FROM receipts")[0]['count'] <= 0:
        return redirect("/receipts")
    
    try:
        top_categories = top_ten_categories(db)
        logger.debug("Top categories:", top_categories)
    except Exception as e:
        logging.error("Error loading top categories or no results: %s", e)
        top_categories = []

    try:
        month_spending = this_month_spending(db)
        logger.debug("This month spending:", month_spending)
    except Exception as e:
        logging.error("Error loading this month spending or no results: %s", e)
        month_spending = []

    try:
        month_receipts = this_month_receipts(db)
        logger.debug("This month's receipts:", month_receipts)
    except Exception as e:
        logging.error("Error loading this month receipts or no results: %s", e)
        month_receipts = []

    if month_receipts:
        for receipt in month_receipts:
            location_id = receipt['location']
            if location_id:
                location_data = db.execute("SELECT name FROM addresses WHERE id = ?", location_id)
                receipt['location'] = location_data[0]['name'] if location_data else None
        for receipt in month_receipts:
            merchant_id = receipt['merchant']
            if merchant_id:
                merchant_data = db.execute("SELECT name FROM merchants WHERE id = ?", merchant_id)
                receipt['merchant'] = merchant_data[0]['name'] if merchant_data else None
        for receipt in month_receipts:
            account_id = receipt['account']
            if account_id:
                account_data = db.execute("SELECT name FROM accounts WHERE id = ?", account_id)
                receipt['account'] = account_data[0]['name'] if account_data else None
        for receipt in month_receipts:
            category_id = receipt['category']
            if category_id:
                category_data = db.execute("SELECT name FROM categories WHERE id = ?", category_id)
                receipt['category'] = category_data[0]['name'] if category_data else None
        month_receipts.sort(key=lambda x: x['date'])

    return render_template("dashboard.html", 
                           top_categories=top_categories, 
                           month_spending=month_spending, 
                           currency_symbol=config.currency_symbol,
                           receipts=month_receipts)