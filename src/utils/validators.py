
import pytz
import sqlite3

from datetime import datetime as dt

""" Validate Inputs Server-Side """

def createDB(schema_file):
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

def lastFour(card_number):
    """ Ensure only last four chars of card number are stored """
    if len(card_number) <= 4:
        return card_number
    elif len(card_number) > 4:
        return card_number[-4:]
    print("Invalid card number")
    return False

def toCurrency(number):
    """ Transform the value a two-decimal number """   
    # Format the number between 0 and 1 billion
    if number.replace('.', '', 1).isdigit():
        number = float(number)
        if 0 <= number < 100_000_000_000:
            return f"{number:.2f}"
    print("Not a number")
    return False

def toDatetime(datetime):
    """ Transform the value to a datetime object """
    try:
        print("Parsing datetime:", datetime)
        # Format the datetime string to a datetime object
        datestr = datetime.replace("T"," ")
        z = dt.strptime(datestr, '%Y-%m-%d %H:%M')
        return datetime
    except ValueError:
        print("Invalid date format")
        return False

def toUTC(datestr, timezone):
    """ Transform the datetime to UTC """
    try:
        print("Converting to UTC:", datestr, timezone)

        # Get the timezone object
        tz = pytz.timezone(timezone)

        # Create a datetime object from the string
        datestr = datestr.replace("T"," ")
        dt_obj = dt.strptime(datestr, '%Y-%m-%d %H:%M')

        # Convert the datetime to UTC
        local = tz.localize(dt_obj)
        utc_dt = local.astimezone(pytz.utc)

        # Return the ISO 8601 format
        iso_utc = utc_dt.isoformat()
        return iso_utc
    
    except Exception as e:
        print("Error converting to UTC:", e)
        return False

