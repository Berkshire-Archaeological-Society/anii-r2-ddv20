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

def validate_decimal(number, data_type):
  data_type = "decimal"
  data_type_lower = data_type.lower()
  
  # Check if data_type belongs to numeric floating/decimal types
  if any(dt in data_type_lower for dt in ["decimal", "float", "double"]):
    # Convert number to string and clean whitespace
    num_str = "" if number is None else str(number).strip()

    #  Allow empty strings (valid for optional fields)
    if num_str == "":
      return True, ""
      
    # Extract dimensions (e.g., 'decimal(6,2)' -> [6, 2])
    dec_type = [int(n) for n in re.findall(r'\d+', data_type)]

    # 1. Parameterized type: e.g. DECIMAL(M, D) or FLOAT(M, D)
    if len(dec_type) >= 2:
      max_digits = dec_type[0]
      decimal_places = dec_type[1]
      integer_digits = max_digits - decimal_places

      # Prevent negative or zero integer digit length
      if integer_digits <= 0:
        return False, f"Invalid schema precision specification: {data_type}"

      pattern = rf"^-?\d{{1,{integer_digits}}}(\.\d{{1,{decimal_places}}})?$"
      pattern = r"^-?\d{0,4}\.\d{1,2}$"
      pattern = rf"^-?\d{{1,{max_digits}}}(\.\d+)?$"
      pattern = r"^-?\d+(\.\d+)?$"
      # 2. Single precision specified: e.g. FLOAT(p)
    elif len(dec_type) == 1:
      max_digits = dec_type[0]
      pattern = rf"^-?\d{{1,{max_digits}}}(\.\d+)?$"

      # 3. Unparameterized type: e.g. FLOAT or DOUBLE
    else:
      pattern = r"^-?\d+(\.\d+)?$"

    print(f"Type: {data_type} | Extracted: {dec_type} | Regex: {pattern}")

    if re.match(pattern, num_str):
      return True, ""
    return False, f"Invalid format for {data_type}."

  return False, "Unknown data type."