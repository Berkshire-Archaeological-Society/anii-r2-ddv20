import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import re

# This is the DataValidation module.

def validate_email(email):
  pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
  if not email or not re.match(pattern, str(email).strip()):
    return False, "Invalid email address format."
  return True, ""

def validate_integer(number):
  pattern = r"^$|^\d*$"
  if not number or not re.match(pattern, str(number).strip()):
    return False, "Invalid whole number format."
  return True, ""

def validate_year(number):
  pattern = r"^$|^(-?[0-9]{1,10}|)$"
  if not number or not re.match(pattern, str(number).strip()):
    return False, "Invalid year format."
  return True, ""

def validate_percentage(number):
  pattern = r"^(100(\.0+)?|[1-9]?\d(\.\d+)?)$"
  if not number or not re.match(pattern, str(number).strip()):
    return False, "Invalid percentage format."
  return True, ""