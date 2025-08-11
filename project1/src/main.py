import json
from helpers import read_inventory, write_inventory, add_order_record

def main():
  inventory = read_inventory()
  transaction = []

  while True:
    print("Enter one of following genres: ")
    print(*inventory.keys(), sep='\n -> ')
    genre = input()
    if genre not in inventory:
      print("Please enter the available genere")
      continue

    print("Enter one of the products: ")
    print(*[f" -> {product} ({inventory[genre][product]["availableStock"]})" for product in inventory[genre].keys()], sep='\n')
    product = input()

    if product not in inventory[genre]:
      print("Please enter available product")
    
    qty = int(input("Enter number of " + product + ": "))
    if qty <= inventory[genre][product]["availableStock"]:
      inventory[genre][product]["availableStock"] -= qty
      name = input("Enter your name: ")
      price = inventory[genre][product]["price"] * qty
      paymentMethod = input("Enter payment method: ")

      write_inventory(inventory)
      add_order_record(name, product, price, paymentMethod)
    else:
      print("Please enter valid quantity")
      continue

    continueFlag = input("Do you want to continue? (Y/N)")
    if continueFlag.lower() == 'n': break
    print()


if __name__=='__main__':
  main()