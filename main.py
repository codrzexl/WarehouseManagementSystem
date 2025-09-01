import numpy as np
import matplotlib.pyplot as plt
import json

class Product:
    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price

class Warehouse:
    def __init__(self):
        self.inventory = {}

    def add_product(self, product, quantity):
        if product.product_id in self.inventory:
            self.inventory[product.product_id]['quantity'] += quantity
        else:
            self.inventory[product.product_id] = {'product': product, 'quantity': quantity}

    def remove_product(self, product_id, quantity):
        if product_id in self.inventory and self.inventory[product_id]['quantity'] >= quantity:
            self.inventory[product_id]['quantity'] -= quantity
            if self.inventory[product_id]['quantity'] == 0:
                del self.inventory[product_id]
            print(f"Removed {quantity} of product ID {product_id}.")
        else:
            print(f"Error: Insufficient quantity or product ID {product_id} not found.")

    def update_product(self, product_id, name=None, price=None):
        if product_id in self.inventory:
            if name:
                self.inventory[product_id]['product'].name = name
            if price:
                self.inventory[product_id]['product'].price = price
            print(f"Product {product_id} updated.")
        else:
            print(f"Error: Product ID {product_id} not found.")

    def search_product(self, product_id):
        if product_id in self.inventory:
            return self.inventory[product_id]['product']
        else:
            print(f"Error: Product ID {product_id} not found.")
            return None

    def view_product_details(self, product_id):
        if product_id in self.inventory:
            product = self.inventory[product_id]['product']
            quantity = self.inventory[product_id]['quantity']
            print(f"Product ID: {product.product_id}, Name: {product.name}, Price: {product.price}, Quantity: {quantity}")
        else:
            print(f"Error: Product ID {product_id} not found.")

    def get_inventory_levels(self):
        return {product_id: info['quantity'] for product_id, info in self.inventory.items()}

    def visualize_inventory(self):
        product_ids = list(self.inventory.keys())
        quantities = [info['quantity'] for info in self.inventory.values()]
        
        plt.bar(product_ids, quantities)
        plt.xlabel('Product ID')
        plt.ylabel('Quantity')
        plt.title('Inventory Levels')
        plt.show()

    def save_inventory(self, filename):
        with open(filename, 'w') as file:
            json.dump({product_id: {'product': {'product_id': info['product'].product_id, 'name': info['product'].name, 'price': info['product'].price}, 'quantity': info['quantity']} for product_id, info in self.inventory.items()}, file)
        print("Inventory saved.")

    def load_inventory(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.inventory = {int(product_id): {'product': Product(info['product']['product_id'], info['product']['name'], info['product']['price']), 'quantity': info['quantity']} for product_id, info in data.items()}
            print("Inventory loaded.")
        except FileNotFoundError:
            print("Error: File not found. Starting with an empty inventory.")

class Order:
    def __init__(self, order_id, products):
        self.order_id = order_id
        self.products = products

    def process_order(self, warehouse):
        for product_id, quantity in self.products:
            if product_id not in warehouse.inventory:
                print(f"Error: Invalid product ID {product_id}. Skipping this product.")
                continue  
            if warehouse.inventory[product_id]['quantity'] < quantity:
                print(f"Error: Insufficient quantity for product ID {product_id}. Available: {warehouse.inventory[product_id]['quantity']}, Requested: {quantity}")
                continue
            warehouse.remove_product(product_id, quantity)
            print(f"Processed {quantity} of product ID {product_id} for order {self.order_id}.")

def main():
    warehouse = Warehouse()

    while True:
        print("\nWarehouse Management System")
        print("1. Add Product")
        print("2. Create Order")
        print("3. View Inventory Levels")
        print("4. Visualize Inventory")
        print("5. Update Product")
        print("6. Search Product")
        print("7. View Product Details")
        print("8. Save Inventory")
        print("9. Load Inventory")
        print("10. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            try:
                product_id = int(input("Enter product ID: "))
                name = input("Enter product name: ")
                price = float(input("Enter product price: "))
                quantity = int(input("Enter quantity: "))
                product = Product(product_id, name, price)
                warehouse.add_product(product, quantity)
                print(f"Added {quantity} of {name} to the warehouse.")
            except ValueError:
                print("Error: Invalid input. Please enter numeric values for ID, price, and quantity.")

        elif choice == '2':
            try:
                order_id = int(input("Enter order ID: "))
                num_products = int(input("Enter number of products in the order: "))
                products = []
                for _ in range(num_products):
                    product_id = int(input("Enter product ID: "))
                    quantity = int(input("Enter quantity: "))
                    products.append((product_id, quantity))
                order = Order(order_id, products)
                order.process_order(warehouse)
                print(f"Processed order {order_id}.")
            except ValueError:
                print("Error: Invalid input. Please enter numeric values for order ID, product ID, and quantity.")

        elif choice == '3':
            inventory_levels = warehouse.get_inventory_levels()
            print("Current Inventory Levels:", inventory_levels)

        elif choice == '4':
            warehouse.visualize_inventory()

        elif choice == '5':
            try:
                product_id = int(input("Enter product ID to update: "))
                name = input("Enter new product name (leave blank to keep current): ")
                price = input("Enter new product price (leave blank to keep current): ")
                price = float(price) if price else None
                warehouse.update_product(product_id, name, price)
            except ValueError:
                print("Error: Invalid input. Please enter numeric values for product ID and price.")

        elif choice == '6':
            try:
                product_id = int(input("Enter product ID to search: "))
                product = warehouse.search_product(product_id)
                if product:
                    print(f"Product found: ID={product.product_id}, Name={product.name}, Price={product.price}")
            except ValueError:
                print("Error: Invalid input. Please enter a numeric value for product ID.")

        elif choice == '7':
            try:
                product_id = int(input("Enter product ID to view details: "))
                warehouse.view_product_details(product_id)
            except ValueError:
                print("Error: Invalid input. Please enter a numeric value for product ID.")

        elif choice == '8':
            filename = input("Enter filename to save inventory: ")
            warehouse.save_inventory(filename)

        elif choice == '9':
            filename = input("Enter filename to load inventory: ")
            warehouse.load_inventory(filename)

        elif choice == '10':
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Error: Invalid choice. Please try again.")

if __name__ == "__main__":
    main()