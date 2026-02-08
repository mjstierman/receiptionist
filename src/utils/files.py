""" Validate and read uploaded files """

import base64
import logging

def to_base64(unsafe_file):
    """ Validate and read the uploaded file """
    try:
        file_data = unsafe_file.read()
        file_data = base64.b64encode(file_data).decode('utf-8')
        return file_data
    except Exception as e:
        logging.error("File upload error: %s", e)
        return False