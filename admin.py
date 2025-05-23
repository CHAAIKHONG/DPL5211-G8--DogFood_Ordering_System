import os
import csv
import platform

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def login():
    clear_screen()
    print("=== Admin Login ===")
    username = input("Username: ")
    password = input("Password: ")
    if username == "nicholas" and password == "Nczk.29":
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
    print("8. Logout")

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
        elif choice == "8":
            print("Logging out...\n")
            break
        else:
            print("Invalid choice. Please select a valid option.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    if login():
        admin_dashboard()
    else:
        print("Exiting program.")