import json
import os
import csv

INVENTORY_PATH = "./database/inventory.json"
TRANSACTION_PATH = "./database/transactions.csv"

def read_json(file_path):
  if not os.path.exists(file_path):
    return {}
  
  try:
    with open(file_path, 'r', encoding='utf-8') as file:
      return json.load(file)
  except (json.JSONDecodeError, IOError):
    return {}


def write_json(file_path, data):
  try:
    # Ensure parent directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as file:
      json.dump(data, file, indent=4, ensure_ascii=False)
    return True
  except (TypeError, IOError):
    return False



def read_inventory():
  return read_json(INVENTORY_PATH)

def write_inventory(data):
  return write_json(INVENTORY_PATH, data)

def add_order_record(name, products, price, payment_method):
    file_exists = os.path.exists(TRANSACTION_PATH)

    # Open the file in append mode
    with open(TRANSACTION_PATH, mode='a', newline='', encoding='utf-8') as file:
      writer = csv.DictWriter(file, fieldnames=["Name", "Products", "Price", "Payment Method"])
      
      # If file doesn't exist, write header first
      if not file_exists:
        writer.writeheader()
      
      # Write the new row
      writer.writerow({
        "Name": name,
        "Products": products,
        "Price": price,
        "Payment Method": payment_method
      })
    
    return True
