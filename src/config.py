""" Configuration for Finfo application """

import logging

### USER PREFERENCES ###
# SQL database configuration
database_url = "sqlite:///app.db"
schema_path = "static/schema.sql"
# Default currency symbol
currency_symbol = "$"

### Debugging and Development ###
TEMPLATES_AUTO_RELOAD = True # Reload templates when html changed
LOG_LEVEL = logging.INFO # NOTSET DEBUG INFO WARNING ERROR CRITICAL

# Logging Config
logging.basicConfig(
    level=LOG_LEVEL,  # Default level
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S %z",
    handlers=[
        logging.FileHandler('app.log'),  # Log to file
        logging.StreamHandler()  # Also print to console
    ]
)
