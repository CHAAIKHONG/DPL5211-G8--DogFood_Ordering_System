import os
import csv
import platform

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def login():
    clear_screen()
    print("===== Admin Login =====")
    username = input("Username : ")
    password = input("Password : ")
    if username == "nicholas" and password == "Nczk.29":
        print("Login successful!\n")
        return True
    else:
        print("Invalid credentials.\n")
        return False

def show_main_menu():
    clear_screen()
    print("=== Admin Dashboard ===")
    print("1. Manage Category")
    print("2. Manage Product")
    print("3. Manage Order")
    print("4. Manage Feedback")
    print("5. Report")
    print("6. Manage Staff Account")
    print("7. Profile")
    print("0. Logout")

def load_data(filename, delimiter=","):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as file:
        reader = csv.reader(file, delimiter=delimiter)
        return list(reader)

def save_data(filename, data, delimiter=","):
    with open(filename, "w", newline='') as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerows(data)

def manage_category():
    file = "category.txt"
    data = load_data(file)
    while True:
        clear_screen()
        print("\n--- Manage Category ---")
        print("1. View Categories")
        print("2. Add Category")
        print("3. Delete Category")
        print("4. Back to Main Menu")
        choice = input("Select option: ")
        if choice == "1":
            clear_screen()
            print("\n--- Category List ---")
            for row in data:
                print(" | ".join(row))
            input("\nPress Enter to continue...")
        elif choice == "2":
            name = input("Enter new category name: ")
            new_id = str(int(data[-1][0]) + 1 if data else 1)
            data.append([new_id, name])
            save_data(file, data)
            print("Category added.")
            input("Press Enter to continue...")
        elif choice == "3":
            del_id = input("Enter ID to delete: ")
            data = [row for row in data if row[0] != del_id]
            save_data(file, data)
            print("Category deleted.")
            input("Press Enter to continue...")
        elif choice == "4":
            break
        else:
            print("Invalid option.")
            input("Press Enter to continue...")

def manage_product():
    file = "product.txt"
    data = load_data(file, delimiter="|")
    while True:
        clear_screen()
        display_product_list(data, status_filter="active")
        print("\n------------------------")
        print("     Manage Product     ")
        print("------------------------")
        print("1. Add Product")
        print("2. Edit Product")
        print("3. Delete Product")
        print("4. Restore Deleted Product")
        print("0. Back to Main Menu")
        choice = input("\nSelect option: ")

        if choice == "1":
            clear_screen()
            display_product_list(data, status_filter="active")
            display_categories()
            category_id = input("\nEnter Category ID    : ")
            while category_id not in category_map:
                print("\nInvalid Category ID. Please select from the list.")
                category_id = input("Enter Category ID    : ")
            name = input("Enter Product Name   : ")
            price = input("Enter Price          : ")
            stock = input("Enter Stock Quantity : ")
            description = input("Enter Description    : ")
            new_id = str(int(data[-1][0]) + 1 if data else 1)
            status = "active"
            data.append([new_id, category_id, name, price, stock, description, status])
            save_data(file, data, delimiter="|")
            print("Product added.")
            input("Press Enter to continue...")

        elif choice == "2":
            clear_screen()
            display_product_list(data, status_filter="active")
            edit_id = input("\nEnter Product ID to edit: ")
            found = False
            for row in data:
                if row[0] == edit_id and row[6] == "active":
                    found = True
                    print(f"\nEditing product: {row[2]}")
                    print("\nWhat do you want to edit?")
                    print("1. Category")
                    print("2. Product Name")
                    print("3. Price")
                    print("4. Stock")
                    print("5. Description")
                    print("0. Cancel")
                    sub_choice = input("\nSelect option: ")

                    if sub_choice == "1":
                        display_categories()
                        new_cat = input(f"\nEnter new Category ID [{row[1]}]: ") or row[1]
                        while new_cat not in category_map:
                            new_cat = input("Invalid Category ID. Re-enter: ")
                        row[1] = new_cat
                    elif sub_choice == "2":
                        row[2] = input(f"Enter new Product Name [{row[2]}]: ") or row[2]
                    elif sub_choice == "3":
                        row[3] = input(f"Enter new Price [{row[3]}]: ") or row[3]
                    elif sub_choice == "4":
                        row[4] = input(f"Enter new Stock [{row[4]}]: ") or row[4]
                    elif sub_choice == "5":
                        row[5] = input(f"Enter new Description [{row[5]}]: ") or row[5]
                    elif sub_choice == "0":
                        print("Edit cancelled.")
                    else:
                        print("Invalid option.")
                    break
            if found:
                save_data(file, data, delimiter="|")
                print("Product updated.")
            else:
                print("Active product not found.")
            input("Press Enter to continue...")

        elif choice == "3":
            clear_screen()
            display_product_list(data, status_filter="active")
            del_id = input("Enter Product ID to delete: ")
            found = False
            for row in data:
                if row[0] == del_id and row[6] == "active":
                    row[6] = "deleted"
                    found = True
                    break
            if found:
                save_data(file, data, delimiter="|")
                print(f"Product ID {del_id} marked as deleted.")
            else:
                print("Active product not found.")
            input("Press Enter to continue...")

        elif choice == "4":
            clear_screen()
            display_product_list(data, status_filter="deleted")
            restore_id = input("Enter Product ID to restore: ")
            restored = False
            for row in data:
                if row[0] == restore_id and row[6] == "deleted":
                    row[6] = "active"
                    restored = True
                    break
            if restored:
                save_data(file, data, delimiter="|")
                print("Product restored.")
            else:
                print("Deleted product not found.")
            input("Press Enter to continue...")

        elif choice == "0":
            break
        else:
            print("Invalid option.")
            input("Press Enter to continue...")


def display_product_list(product_data=None, status_filter=None):
    file = "product.txt"
    data = load_data(file, delimiter="|") if product_data is None else product_data

    if status_filter:
        data = [row for row in data if row[6] == status_filter]

    headers = ["ID", "Category", "Name", "Price", "Stock", "Description", "Status"]
    col_widths = [4, 15, 30, 8, 6, 45, 10]

    def format_row(row_data):
        return (
            f"{row_data[0]:<{col_widths[0]}} | "
            f"{category_map.get(row_data[1], 'Unknown'):<{col_widths[1]}} | "
            f"{row_data[2][:col_widths[2]]:<{col_widths[2]}} | "
            f"{row_data[3]:>{col_widths[3]}} | "
            f"{row_data[4]:>{col_widths[4]}} | "
            f"{row_data[5][:col_widths[5]]:<{col_widths[5]}} | "
            f"{row_data[6]:<{col_widths[6]}}"
        )

    total_width = sum(col_widths) + 6 * 3 + 1
    print("-" * total_width)
    title = f"PRODUCT LIST - {status_filter.upper()}" if status_filter else "PRODUCT LIST"
    print(f"{title:^{total_width}}")
    print("-" * total_width)
    print(format_row(headers))
    print("-" * total_width)

    for row in data:
        if len(row) == 6:
            row.append("active")
        print(format_row(row))

    print("-" * total_width)

category_map = {
    "1": "Dry Food",
    "2": "Wet Food",
    "3": "Raw Frozen",
    "4": "Freeze-Dried",
    "5": "Homemade"
}

def display_categories():
    print("\n----------------")
    print("   Categories   ")
    print("----------------")
    for cid, cname in category_map.items():
        print(f"{cid}. {cname}")

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
  
def manage_feedback():
    clear_screen()
    file = "feedback.txt"
    data = load_data(file)
    print("\n--- Feedback Entries ---")
    for row in data:
        print(" | ".join(row))
    input("\nPress Enter to return...")

def show_report_menu():
    clear_screen()
    print("\n--- Report Management ---")
    print("1. Daily Report")
    print("2. Monthly Report")
    print("3. Annual Report")
    choice = input("Select report type: ")
    if choice == "1":
        print("Generating Daily Report...\n")
    elif choice == "2":
        print("Generating Monthly Report...\n")
    elif choice == "3":
        print("Generating Annual Report...\n")
    else:
        print("Invalid report option.\n")
    input("Press Enter to return...")

def manage_staff_account():
    clear_screen()
    print("[TODO: Implement file-based staff management]\n")
    input("Press Enter to return...")

def profile():
    clear_screen()
    print("[TODO: Implement user profile view/edit]\n")
    input("Press Enter to return...")

def admin_dashboard():
    while True:
        show_main_menu()
        choice = input("\nSelect an option: ")
        if choice == "1":
            manage_category()
        elif choice == "2":
            manage_product()
        elif choice == "3":
            manage_order()
        elif choice == "4":
            manage_feedback()
        elif choice == "5":
            show_report_menu()
        elif choice == "6":
            manage_staff_account()
        elif choice == "7":
            profile()
        elif choice == "0":
            login()
            break
        else:
            print("Invalid choice. Please select a valid option.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    if login():
        admin_dashboard()
    else:
        print("Exiting program.")