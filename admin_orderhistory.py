import os
import csv
import platform
from datetime import datetime
import hashlib

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')
def manage_order():
    clear_screen()
    try:
        with open("orderhistory.txt") as file:
            lines = file.readlines()
            orders = []
            order_id_counter = 1
            for line in lines:
                parsed = parse_order_line(line, order_id_counter)
                if parsed:
                    orders.append(parsed)
                    order_id_counter += 1
    except FileNotFoundError:
        print("No orders found (orderhistory.txt is missing).")
        input("Press Enter to return...")
        return

    if not orders:
        print("No valid orders found.")
        input("Press Enter to return...")
        return

    while True:
        clear_screen()
        print("--- Order Management ---")
        print("1. View all orders")
        print("2. Filter by payment method")
        print("3. Filter by Customer ID")
        print("4. Filter by Delivery Status")
        print("5. Update Delivery Status")
        print("0. Return to main menu")
        choice = input("\nSelect an option: ")

        if choice == "1":
            clear_screen()
            display_orders(orders, "ALL ORDERS")

        elif choice == "2":
            clear_screen()
            display_orders(orders, "All Orders", show_footer=False, pause=False)
            print("\nPayment Filter Options:")
            print("1. Visa")
            print("2. Cash on Delivery")
            print("Enter to show all\n")
            method_choice = input("Select payment filter: ").strip()

            method = ""
            if method_choice == "1":
                method = "Visa"
            elif method_choice == "2":
                method = "Cash on Delivery"

            if method:
                filtered = [order for order in orders if order['PaymentMethod'].lower() == method.lower()]
                title = f"Orders Paid by {method}"
            else:
                filtered = orders
                title = "All Orders (No Payment Filter)"

            clear_screen()
            if filtered:
                display_orders(filtered, title)
            else:
                print(f"No orders found with payment method '{method}'.")
                input("\nPress Enter to return...")

        elif choice == "3":
            clear_screen()
            display_orders(orders, "All Orders", show_footer=False, pause=False)
            cid = input("Enter Customer ID to filter: ")
            filtered = [order for order in orders if order['CustomerID'] == cid]
            clear_screen()
            title = f"Orders for Customer ID {cid}"
            if filtered:
                display_orders(filtered, title)
            else:
                print(f"No orders found for Customer ID '{cid}'.")
                input("\nPress Enter to return...")

        elif choice == "4":
            clear_screen()
            display_orders(orders, "All Orders", show_footer=False, pause=False)
            print("\nDelivery Status Filter Options:")
            print("1. Pending")
            print("2. Delivered")
            print("Enter to show all\n")
            status_choice = input("Select delivery status filter: ").strip()

            status = ""
            if status_choice == "1":
                status = "Pending"
            elif status_choice == "2":
                status = "Delivered"

            if status:
                filtered = [order for order in orders if order['DeliveryStatus'] == status]
                title = f"Orders with Delivery Status: {status}"
            else:
                filtered = orders
                title = "All Orders (No Delivery Status Filter)"

            clear_screen()
            if filtered:
                display_orders(filtered, title)
            else:
                print(f"No orders found with Delivery Status '{status}'.")
                input("\nPress Enter to return...")

        elif choice == "5":
            clear_screen()
            display_orders(orders, "All Orders", show_footer=False, pause=False)
            order_id = input("Enter Order ID to mark as Delivered: ")
            matching = [order for order in orders if order['OrderID'] == order_id]
            if not matching:
                print(f"No order found with Order ID '{order_id}'.")
            else:
                matching[0]['DeliveryStatus'] = "Delivered"
                print(f"Order {order_id} marked as Delivered.")

                try:
                    with open("orderhistory.txt", "w") as file:
                        for order in orders:
                            line = "|".join([
                                order['OrderID'],
                                order['CustomerID'],
                                order['Product'],
                                str(order['Quantity']),
                                f"{order['Price']:.2f}",
                                f"{order['Total']:.2f}",
                                order['DateTime'],
                                order['PaymentMethod'],
                                order['PaymentDetails'],
                                order['DeliveryStatus']
                            ])
                            file.write(line + "\n")
                except Exception as e:
                    print(f"Failed to save updated orders: {e}")

            input("Press Enter to return...")

        elif choice == "0":
            break

        else:
            print("Invalid option. Try again.")
            input("Press Enter to continue...")

def parse_order_line(line, order_id):
    parts = line.strip().split('|')
    try:
        if len(parts) == 8:  # 8-column format
            return {
                'OrderID': str(order_id),
                'CustomerID': parts[0],
                'Product': parts[1],
                'Quantity': int(parts[2]),
                'Price': float(parts[3]),
                'Total': float(parts[4]),
                'DateTime': parts[5],
                'PaymentMethod': parts[6],
                'PaymentDetails': parts[7],
                'DeliveryStatus': 'Pending'
            }
        elif len(parts) == 10:
            return {
                'OrderID': str(order_id),
                'CustomerID': parts[1],
                'Product': parts[2],
                'Quantity': int(parts[3]),
                'Price': float(parts[4]),
                'Total': float(parts[5]),
                'DateTime': parts[6],
                'PaymentMethod': parts[7],
                'PaymentDetails': parts[8],
                'DeliveryStatus': parts[9]
            }
    except ValueError as e:
        print(f"Skipping malformed line: {line.strip()} ({e})")
    return None

def display_orders(orders, title="", show_footer=True, pause=True):
    headers = ["Order_ID", "CustomerID", "Product", "Qty", "Price", "Total", "DateTime", "Payment", "Details", "Status"]
    col_widths = [10, 12, 35, 5, 8, 10, 19, 14, 38, 10]

    def format_row(row_data):
        return " | ".join(f"{str(value)[:col_widths[i]]:<{col_widths[i]}}" for i, value in enumerate(row_data))

    total_width = sum(col_widths) + (len(col_widths) - 1) * 3 + 1
    print("-" * total_width)
    if title:
        print(f"{title:^{total_width}}")
        print("-" * total_width)
    print(format_row(headers))
    print("-" * total_width)

    for order in orders:
        row = [
            order['OrderID'],
            order['CustomerID'],
            order['Product'],
            order['Quantity'],
            f"{order['Price']:.2f}",
            f"{order['Total']:.2f}",
            order['DateTime'],
            order['PaymentMethod'],
            order['PaymentDetails'],
            order['DeliveryStatus']
        ]
        print(format_row(row))

    print("-" * total_width)
    
    if show_footer:
        print(f"Total Orders  : {len(orders)}")
        total_rev = sum(order['Total'] for order in orders)
        print(f"{'Total Revenue :'} RM {total_rev:.2f}")
    
    if pause:
        input("\nPress Enter to return...")