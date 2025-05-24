import os
import csv
import platform
from datetime import datetime
import hashlib

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def load_order_history(filename="orderhistory.txt"):
    history = []
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, start=1):
                parts = line.strip().split('|')
                if len(parts) < 6:
                    print(f"[❌ Line {line_num}] Skipped - Expected at least 6 parts but got {len(parts)}: {line.strip()}")
                    continue
                try:
                    # Extract base fields
                    user_id, product_name, quantity, unit_price, total_price, timestamp = parts[:6]
                    
                    # Extract payment info if available
                    payment_method = parts[6] if len(parts) > 6 else "Unknown"
                    payment_details = parts[7] if len(parts) > 7 else "N/A"
                    
                    history.append({
                        'timestamp': timestamp.strip(),
                        'user_id': user_id.strip(),
                        'product_name': product_name.strip(),
                        'quantity': int(quantity),
                        'unit_price': float(unit_price),
                        'total_price': float(total_price),
                        'payment_method': payment_method.strip(),
                        'payment_details': payment_details.strip()
                    })
                except ValueError as e:
                    print(f"[❌ Line {line_num}] Error converting values: {e}")
    return history

def load_admin_details(method, filename="staff.txt"):
    admin_details  = []
    global user_id
    # print(f"id = {user_id}")
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            for index, line in enumerate(f):
                parts = line.strip().split('|')
                if len(parts) == 6:
                    if method == "register" or method == "login" or method == "profile":
                        id, fullname, email, address, phonenumber, password = parts
                        admin_details.append({
                            'id': int(id),
                            'fullname': fullname.strip(),
                            'email': email.strip(),
                            'address': address.strip(),
                            'phonenumber' : phonenumber.strip(),
                            'password': password.strip(),
                        })

    return admin_details


def login():
    clear_screen()
    print("=== Admin Login ===")
    username = input("Username: ")
    password = input("Password: ")
    if username == "aikhong" and password == "aikhong":
        print("Login successful!\n")
        return True
    else:
        print("Invalid credentials.\n")
        return False

def show_main_menu():
    clear_screen()
    print("\n=== Admin Dashboard ===")
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
            new_id = str(int(data[-1][0]) + 1) if data else "1"
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
    clear_screen()
    print("[TODO: Implement file-based product management]\n")
    input("Press Enter to return...")

def manage_order():
    clear_screen()
    print("[TODO: Implement file-based order management]\n")
    input("Press Enter to return...")

def manage_feedback():
    clear_screen()
    file = "feedback.txt"
    data = load_data(file)
    print("\n--- Feedback Entries ---")
    for row in data:
        print(" | ".join(row))
    input("\nPress Enter to return...")

def generate_daily_report(date_str):
    clear_screen()
    history = load_order_history()
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        filtered = []
        for order in history:
            dt = datetime.strptime(order['timestamp'], "%Y-%m-%d %H:%M:%S").date()
            if dt == target_date:
                filtered.append(order)
        print(f"\n📅 Daily Report for {date_str}")
        print(f"{'Time':<20} | {'Product Name':<35} | {'Qty':>5} | {'Total (RM)':>10}")
        print("-" * 80)
        total = 0
        for o in filtered:
            print(f"{o['timestamp']:<20} | {o['product_name']:<35} | {o['quantity']:>5} | {o['total_price']:>10.2f}")
            total += o['total_price']
        print(f"\n💰 Total Revenue: RM{total:.2f}")
    except ValueError:
        print("❌ Invalid date format. Use YYYY-MM-DD.")

    input("\nPress Enter to return...")

def generate_monthly_report(month_str):
    clear_screen()
    history = load_order_history()
    try:
        target_month = datetime.strptime(month_str, "%Y-%m")
        filtered = []
        for order in history:
            dt = datetime.strptime(order['timestamp'], "%Y-%m-%d %H:%M:%S")
            if dt.year == target_month.year and dt.month == target_month.month:
                filtered.append(order)
        print(f"\n📅 Monthly Report for {month_str}")
        print(f"{'Time':<20} | {'Product Name':<35} | {'Qty':>5} | {'Total (RM)':>10}")
        print("-" * 80)
        total = 0
        for o in filtered:
            print(f"{o['timestamp']:<20} | {o['product_name']:<35} | {o['quantity']:>5} | {o['total_price']:>10.2f}")
            total += o['total_price']
        print(f"\n💰 Total Revenue: RM{total:.2f}")
    except ValueError:
        print("❌ Invalid month format. Use YYYY-MM.")

    input("\nPress Enter to return...")

def generate_annual_report(year_str):
    clear_screen()
    history = load_order_history()
    try:
        target_year = int(year_str)
        filtered = []
        for order in history:
            dt = datetime.strptime(order['timestamp'], "%Y-%m-%d %H:%M:%S")
            if dt.year == target_year:
                filtered.append(order)
        print(f"\n📅 Annual Report for {year_str}")
        print(f"{'Time':<20} | {'Product Name':<35} | {'Qty':>5} | {'Total (RM)':>10}")
        print("-" * 80)
        total = 0
        for o in filtered:
            print(f"{o['timestamp']:<20} | {o['product_name']:<35} | {o['quantity']:>5} | {o['total_price']:>10.2f}")
            total += o['total_price']
        print(f"\n💰 Total Revenue: RM{total:.2f}")
    except ValueError:
        print("❌ Invalid year format. Use YYYY.")

    input("\nPress Enter to return...")

def show_report_menu():
    while True:
        clear_screen()
        print("\n--- Report Management ---")
        print("1. Daily Report")
        print("2. Monthly Report")
        print("3. Annual Report")
        print("0. Back")
        choice = input("Select report type: ")

        if choice == "1":
            while True:
                clear_screen()
                print("\n--- Daily Report ---")
                print("1. Search by date")
                print("2. Today's report")
                print("0. Back")
                sub_choice = input("Select option: ")
                if sub_choice == "1":
                    date_str = input("Enter date (YYYY-MM-DD): ")
                    generate_daily_report(date_str)
                    break
                elif sub_choice == "2":
                    today_str = datetime.today().strftime('%Y-%m-%d')
                    generate_daily_report(today_str)
                    break
                elif sub_choice == "0":
                    break
                else:
                    input("\033[91mInvalid Daily Report option. Please press Enter to try again.\033[0m")

        elif choice == "2":
            while True:
                clear_screen()
                print("\n--- Monthly Report ---")
                print("1. Search by month")
                print("2. This month's report")
                print("0. Back")
                sub_choice = input("Select option: ")
                if sub_choice == "1":
                    month_str = input("Enter month (YYYY-MM): ")
                    generate_monthly_report(month_str)
                    break
                elif sub_choice == "2":
                    month_str = datetime.today().strftime('%Y-%m')
                    generate_monthly_report(month_str)
                    break
                elif sub_choice == "0":
                    break
                else:
                    input("\033[91mInvalid Monthly Report option. Please press Enter to try again.\033[0m")

        elif choice == "3":
            while True:
                clear_screen()
                print("\n--- Annual Report ---")
                print("1. Search by year")
                print("2. This year's report")
                print("0. Back")
                sub_choice = input("Select option: ")
                if sub_choice == "1":
                    year_str = input("Enter year (YYYY): ")
                    generate_annual_report(year_str)
                    break
                elif sub_choice == "2":
                    year_str = datetime.today().strftime('%Y')
                    generate_annual_report(year_str)
                    break
                elif sub_choice == "0":
                    break
                else:
                    input("\033[91mInvalid Annual Report option. Please press Enter to try again.\033[0m")

        elif choice == "0":
            admin_dashboard()
            break
        else:
            input("\033[91mInvalid Report Type or option. Please press Enter to try again.\033[0m")

# def manage_staff_account():
#     clear_screen()
#     print("[TODO: Implement file-based staff management]\n")
#     input("Press Enter to return...")

def show_staff():
    clear_screen()
    staff_list = load_admin_details("profile")  # 可用 profile/login/register 都行
    print("ID | Name | Email | Address | Phone")
    print("-" * 50)
    for staff in staff_list:
        print(f"{staff['id']} | {staff['fullname']} | {staff['email']} | {staff['address']} | {staff['phonenumber']}")

def add_staff():
    clear_screen()
    staff_list = load_admin_details("register")
    new_id = max([staff["id"] for staff in staff_list], default=0) + 1

    fullname = input("Enter full name: ")
    email = input("Enter email: ")
    address = input("Enter address: ")
    phoneno = input("Enter phone number: ")
    password = input("Enter password: ")

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    new_line = f"{new_id}|{fullname}|{email}|{address}|{phoneno}|{hashed_password}"
    
    with open("staff.txt", "a", encoding="utf-8") as f:
        f.write(new_line + "\n")

    print("Staff added successfully.")
    input("Press Enter to return...")

def delete_staff():
    clear_screen()
    staff_list = load_admin_details("profile")
    show_staff()
    delete_id = input("\nEnter the ID of the staff to delete: ")

    try:
        delete_id = int(delete_id)
    except ValueError:
        print("Invalid ID format.")
        input("Press Enter to return...")
        return

    new_list = [staff for staff in staff_list if staff["id"] != delete_id]

    if len(new_list) == len(staff_list):
        print("Staff ID not found.")
    else:
        # 重新写入文件
        with open("staff.txt", "w", encoding="utf-8") as f:
            for staff in new_list:
                line = f'{staff["id"]}|{staff["fullname"]}|{staff["email"]}|{staff["address"]}|{staff["phonenumber"]}|{staff["password"]}'
                f.write(line + "\n")
        print("Staff deleted successfully.")
    input("Press Enter to return...")

def manage_staff_account():
    while True:
        clear_screen()
        print("=== Manage Staff Account ===")
        print("1. Show staff")
        print("2. Add staff")
        print("3. Delete staff")
        print("0. Return")
        choice = input("Enter choice: ")

        if choice == "1":
            show_staff()
            input("\nPress Enter to return...")
        elif choice == "2":
            add_staff()
        elif choice == "3":
            delete_staff()
        elif choice == "0":
            break
        else:
            input("Invalid choice. Press Enter to try again...")

def profile():
    clear_screen()
    print("[TODO: Implement user profile view/edit]\n")
    input("Press Enter to return...")

def admin_dashboard():
    while True:
        show_main_menu()
        choice = input("Select an option: ")
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
            print("Logging out...\n")
            break
        else:
            input("\033[91mInvalid choice. Please select a valid option. Press Enter to continue...\033[0m")

if __name__ == "__main__":
    if login():
        admin_dashboard()
    else:
        print("Exiting program.")