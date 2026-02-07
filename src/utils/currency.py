""" Utility functions for handling currency values in the application. """

import logging

def to_currency(value):
    """ Transform the value a two-decimal number """   
    try:
        number = float(value)
        if 0 <= number < 100_000_000_000:
            return round(number, 2)
    except ValueError:
        logging.error("Must be between 0 and 1 Billion: %s", value)

def to_cents(value):
    """ Convert the balance to cents for storage """
    try:
        number = float(value)
        if 0 <= number < 100_000_000_000:
            return int(round(number * 100))
    except ValueError:
        logging.error("Must be between 0 and 1 Billion: %s", value)