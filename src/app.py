import config

from cs50 import SQL
from flask import Flask, render_template, redirect, request, Response
from utils.dashboards import top_ten_categories, this_month_receipts, this_month_spending
from utils.validators import to_currency, to_datedtime, to_utc, to_file, last_four_account, create_db

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
try:
    db = SQL(config.database_url)
except Exception:
    db = create_db(config.schema_path)

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
    if request.form.get("delete"):
        # Get the receipt ID to delete
        receipt_id = request.form.get("delete")
        print("Deleting receipt with ID:", receipt_id)
        db.execute("DELETE FROM receipts WHERE id = ?", receipt_id)
        return redirect("/receipts")
    
    if request.method == "POST":
        # Get the form data
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

        # Validate the data
        datetime = to_datedtime(unsafe_datetime)
        utc = to_utc(datetime, unsafe_timezone)
        tags = unsafe_tags
        items = unsafe_items
        amount = to_currency(unsafe_amount)
        # Get account ID from name
        account_id = db.execute("SELECT id FROM accounts WHERE NAME like ?", unsafe_account)
        account = account_id[0]['id'] if account_id else None
        # Get category ID from name
        category_id = db.execute("SELECT id FROM categories WHERE NAME like ?", unsafe_category)
        category = category_id[0]['id'] if category_id else None
        # Get merchant ID from name
        merchant_id = db.execute("SELECT id FROM merchants WHERE NAME like ?", unsafe_merchant)
        merchant = merchant_id[0]['id'] if merchant_id else None
        # Get location ID from name
        location_id = db.execute("SELECT id FROM addresses WHERE NAME like ?", unsafe_location)
        location = location_id[0]['id'] if location_id else None
        # Get account ID from name
        account_id = db.execute("SELECT id FROM accounts WHERE NAME like ?", unsafe_account)
        account = account_id[0]['id'] if account_id else None
        # Get category ID from name
        category_id = db.execute("SELECT id FROM categories WHERE NAME like ?", unsafe_category)
        category = category_id[0]['id'] if category_id else None
        # Set income flag
        incomeFlag = True if unsafe_incomeFlag == "1" else False
        # Read the file binary data
        file_data = to_file(unsafe_file) if unsafe_file else None

        if request.form.get("id"):
            # Editing an existing receipt
            receipt_id = request.form.get("id")
            print("Editing receipt with ID:", receipt_id)

            # Update the extisting entry in the database
            if utc and category and amount:
                print("Updating receipt in database", 
                      utc, category, tags, items, merchant, location, account, amount, incomeFlag)
                db.execute("UPDATE receipts SET date = ?, category = ?, tags = ?, items = ?, merchant = ?, location = ?, account = ?, amount = ?, income = ?, image = ? WHERE id = ?", 
                           utc, category, tags, items, merchant, location, account, amount, incomeFlag, file_data, receipt_id)
                return redirect("/receipts")
            else:
                return redirect("/receipts")
        
        else:
            # Update the database
            if utc and category and amount:
                print("Inserting receipt into database", 
                      utc, category, tags, items, merchant, location, account, amount, incomeFlag)
                db.execute("INSERT INTO receipts (date, category, tags, items, merchant, location, account, amount, image, income) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                           utc, category, tags, items, merchant, location, account, amount, file_data, incomeFlag)
                return redirect("/receipts")

            else:
                return redirect("/receipts")
    
    else:
        """ Otherwise show the list of receipts """
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
    if request.form.get("delete"):
        # Get the address ID to delete
        address_id = request.form.get("delete")
        print("Deleting address with ID:", address_id)
        db.execute("DELETE FROM addresses WHERE id = ?", address_id)
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
        name = unsafe_name
        street1 = unsafe_street1
        street2 = unsafe_street2
        city = unsafe_city
        state = unsafe_state
        postal = unsafe_postal
        country = unsafe_country
        
        # Check if editing an existing address
        if request.form.get("id"):
            # Editing an existing address
            address_id = request.form.get("id")
            print("Editing address with ID:", address_id)

            # Update the extisting entry in the database
            if name and city and country:
                print("Updating address in database", 
                      name, street1, street2, city, state, postal, country)
                db.execute("UPDATE addresses SET name = ?, street1 = ?, street2 = ?, city = ?, state = ?, postal = ?, country = ? WHERE id = ?", 
                           name, street1, street2, city, state, postal, country, address_id)
                return redirect("/addresses")
            else:
                return redirect("/addresses")
        
        else:
            # Create new entry in the database
            if name and city and country:
                print("Inserting address into database", 
                      name, street1, street2, city, state, postal, country)
                db.execute("INSERT INTO addresses (name, street1, street2, city, state, postal, country) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                           name, street1, street2, city, state, postal, country)
                return redirect("/addresses")
            else:
                return redirect("/addresses")
        
    else:
        """ Otherwise show the addresses page"""
        # check to see if there are any receipts to populate dashboard link
        receipts = db.execute("SELECT COUNT(*) as count FROM receipts")[0]['count'] > 0
        addresses = db.execute("SELECT * FROM addresses")
        print("Loaded addresses:", addresses)
        return render_template("addresses.html", addresses=addresses, receipts=receipts)

@app.route("/merchants", methods=["GET", "POST"])
def merchants():
    """ Load the merchants page """
    if request.form.get("delete"):
        # Get the merchant ID to delete
        merchant_id = request.form.get("delete")
        print("Deleting merchant with ID:", merchant_id)
        db.execute("DELETE FROM merchants WHERE id = ?", merchant_id)
        return redirect("/merchants")
    
    if request.method == "POST":
        # Get the form data
        unsafe_name = request.form.get("name")
        unsafe_location = request.form.get("location")

        # Validate the data
        name = unsafe_name
        location_id = db.execute("SELECT id FROM addresses WHERE NAME like ?", 
                                 unsafe_location)
        location = location_id[0]['id'] if location_id else None

        # Check if editing an existing merchant
        if request.form.get("id"):
            # Editing an existing merchant
            merchant_id = request.form.get("id")
            print("Editing merchant with ID:", merchant_id)

            # Update the extisting entry in the database
            if name:
                print("Updating merchant in database", name, location)
                db.execute("UPDATE merchants SET name = ?, location = ? WHERE id = ?", 
                           name, location, merchant_id)
                return redirect("/merchants")
            else:
                return redirect("/merchants")

        else:
        # Update the database
            if name:
                print("Inserting merchant into database", name, location)
                db.execute("INSERT INTO merchants (name, location) VALUES (?, ?)", 
                           name, location)
                return redirect("/merchants")
            else:
                return redirect("/merchants")
    
    else:
        """ Otherwise show the merchants page"""
        # check to see if there are any receipts to populate dashboard link
        receipts = db.execute("SELECT COUNT(*) as count FROM receipts")[0]['count'] > 0
        merchants = db.execute("SELECT * FROM merchants")
        addresses = db.execute("SELECT id, name FROM addresses")

        for merchant in merchants:
            location_id = merchant['location']
            if location_id:
                location_data = db.execute("SELECT name FROM addresses WHERE id = ?", location_id)
                merchant['location'] = location_data[0]['name'] if location_data else None

        print("Loaded merchants:", merchants)
        return render_template("merchants.html", merchants=merchants, addresses=addresses, receipts=receipts)

@app.route("/accounts", methods=["GET", "POST"])
def accounts():
    """ Load the accounts page """
    if request.form.get("delete"):
        # Get the account ID to delete
        account_id = request.form.get("delete")
        print("Deleting account with ID:", account_id)
        db.execute("DELETE FROM accounts WHERE id = ?", account_id)
        return redirect("/accounts")
    
    if request.method == "POST":
        # Get the form data
        unsafe_name = request.form.get("name")
        unsafe_merchant = request.form.get("merchant")
        unsafe_lastfour = request.form.get("lastfour")
        unsafe_balance = request.form.get("balance")

        # Validate the data
        name = unsafe_name
        merchant_id = db.execute("SELECT id FROM merchants WHERE NAME like ?", unsafe_merchant)
        merchant = merchant_id[0]['id'] if merchant_id else None
        lastfour = last_four_account(unsafe_lastfour)
        balance = to_currency(unsafe_balance)

        if request.form.get("id"):
            # Editing an existing account
            account_id = request.form.get("id")
            print("Editing account with ID:", account_id)

            # Update the extisting entry in the database
            if name and merchant and lastfour:
                print("Updating account in database", name, merchant, lastfour, balance)
                db.execute("UPDATE accounts SET name = ?, merchant = ?, lastfour = ?, balance = ? WHERE id = ?", 
                           name, merchant, lastfour, balance,  account_id)
                return redirect("/accounts")
            else:
                return redirect("/accounts")

        else:
            # Create new entry in the database
            if name and merchant and lastfour:
                print("Inserting account into database", name, merchant, lastfour, balance)
                db.execute("INSERT INTO accounts (name, merchant, lastfour, balance) VALUES (?, ?, ?, ?)", 
                           name, merchant, lastfour, balance)
                return redirect("/accounts")

            else:
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

        print("Loaded accounts:", accounts)
        return render_template("accounts.html", accounts=accounts, merchants=merchants, receipts=receipts)

@app.route("/categories", methods=["GET", "POST"])
def categories():
    """ Load the categories page """
    if request.form.get("delete"):
        # Get the category ID to delete
        category_id = request.form.get("delete")
        print("Deleting category with ID:", category_id)
        db.execute("DELETE FROM categories WHERE id = ?", category_id)
        return redirect("/categories")
    
    if request.method == "POST":
        # Get the form data
        unsafe_name = request.form.get("name")

        # Validate the data
        name = unsafe_name

        if request.form.get("id"):
            # Editing an existing category
            category_id = request.form.get("id")
            print("Editing category with ID:", category_id)
            # Update the extisting entry in the database
            if name:
                print("Updating category in database", name)
                db.execute("UPDATE categories SET name = ? WHERE id = ?", name, category_id)
                return redirect("/categories")
            else:
                return redirect("/categories")

        else:
            # Update the database
            if name:
                print("Inserting category into database", name)
                db.execute("INSERT INTO categories (name) VALUES (?)", name)
                return redirect("/categories")

            else:
                return redirect("/categories")
    
    else:
        """ Otherwise show the categories page"""
        # check to see if there are any receipts to populate dashboard link
        receipts = db.execute("SELECT COUNT(*) as count FROM receipts")[0]['count'] > 0
        Categories = db.execute("SELECT * FROM categories")
        print("Loaded categories:", Categories)
        return render_template("categories.html", Categories=Categories, receipts=receipts)

@app.route("/dashboard")
def dashboard():
    """ Load the dashboard page """
    # Check to make sure thee are receipts to show
    if db.execute("SELECT COUNT(*) as count FROM receipts")[0]['count'] <= 0:
        return redirect("/receipts")
    
    top_categories = top_ten_categories(db)
    print("Top categories:", top_categories)

    month_spending = this_month_spending(db)
    print("This month spending:", month_spending)

    month_receipts = this_month_receipts(db)
    print("This month's receipts:", month_receipts)

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