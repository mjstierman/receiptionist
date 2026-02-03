import logging

import pytz
import sqlite3

from datetime import datetime as dt

""" Validate Inputs Server-Side """

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

def last_four_account(card_number):
    """ Ensure only last four chars of card number are stored """
    if len(card_number) <= 4:
        return card_number
    elif len(card_number) > 4:
        return card_number[-4:]
    logging.error("Invalid card number")
    return False

def to_currency(number):
    """ Transform the value a two-decimal number """   
    # Format the number between 0 and 1 billion
    if number.replace('.', '', 1).isdigit():
        number = float(number)
        if 0 <= number < 100_000_000_000:
            return f"{number:.2f}"
    logging.error("Not a number")
    return False

def to_file(unsafe_file):
    """ Validate and read the uploaded file """
    try:
        file_data = unsafe_file.read()
        return file_data
    except Exception as e:
        logging.error("File upload error: %s", e)
        return False

def to_datedtime(datetime):
    """ Transform the value to a datetime object """
    try:
        logging.info("Parsing datetime: %s", datetime)
        # Format the datetime string to a datetime object
        datestr = datetime.replace("T"," ")
        z = dt.strptime(datestr, '%Y-%m-%d %H:%M')
        return datetime
    except ValueError:
        logging.ERROR("Invalid date format")
        return False
  
def to_utc(datestr, timezone):
    """ Transform the datetime to UTC """
    try:
        logging.info("Converting to UTC:", datestr, timezone)

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
        logging.error("Error converting to UTC: %s", e)
        return False

