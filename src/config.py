""" Configuration for Finfo application """

from cs50 import SQL

# SQL database configuration
db = SQL("sqlite:///app.db")

# Default currency symbol
currency_symbol = "$"
