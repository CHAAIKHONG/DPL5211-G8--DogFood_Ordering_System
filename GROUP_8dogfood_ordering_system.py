import hashlib
import os
from datetime import datetime 
from collections import defaultdict
import csv

user_id = None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_user_details(method, filename="users_details.txt"):
    user_details  = []
    global user_id
    # print(f"id = {user_id}")
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            for index, line in enumerate(f):
                parts = line.strip().split('|')
                if len(parts) == 6:
                    if method == "register" or method == "login" or method == "profile":
                        id, fullname, email, address, phonenumber, password = parts
                        user_details.append({
                            'id': int(id),
                            'fullname': fullname.strip(),
                            'email': email.strip(),
                            'address': address.strip(),
                            'phonenumber' : phonenumber.strip(),
                            'password': password.strip(),
                        })
                    elif method == "profile":
                        id, username, password_hash, fullname, email, address, phonenumber, password = parts
                        user_details = {
                            "id": int(id),
                            "username": username.strip(),
                            "email": email.strip(),
                            'address': address.strip(),
                            'phonenumber' : phonenumber.strip(),
                            "password_hash": password_hash.strip()
                        }

    return user_details

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

def load_categories(filename):
    categories = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip().replace('|', '|')
                if line:
                    parts = line.split('|')
                    if len(parts) == 2:
                        category_id = parts[0].strip()
                        category_name = parts[1].strip()
                        categories[category_id] = category_name
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    return categories

def load_products(filename):
    products = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip().replace('|', '|')
                if line:
                    parts = line.split('|')
                    if len(parts) >= 6:
                        product_id = parts[0].strip()
                        category_id = parts[1].strip()
                        product_name = parts[2].strip()
                        price = parts[3].strip()
                        stock = parts[4].strip()
                        details = ','.join(parts[5:]).strip()
                        products.append({
                            'product_id': product_id,
                            'category_id': category_id,
                            'product_name': product_name,
                            'price': price,
                            'stock': stock,
                            'details': details
                        })
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    return products

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

def save_users(users, filename="users_details.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for user in users:  # users is a list, not a dict
            f.write(f"{user['id']}|{user['fullname']}|{user['email']}|{user['address']}|{user['phonenumber']}|{user['password']}\n")

def register():
    clear_screen()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("                       Register                         ")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    
    fullname = str(input("Enter username         : "))
    
    users = load_user_details("register")  # 预加载一次现有用户
    
    # Email validation loop + duplicate checking
    while True:
        email = str(input("Enter your email       : "))
        if "@" not in email or "." not in email:
            print("\033[91mInvalid email. Please enter a valid email address (must contain '@' and '.').\033[0m\n")
            continue
        
        # 检查 email 是否已存在
        email_exists = any(user['email'] == email for user in users)
        if email_exists:
            print("\033[91mThis email is already registered. Please use a different email.\033[0m\n")
        else:
            break  # 通过格式和重复检查
    
    address = str(input("Enter home address     : "))
    while True:
        phonenumber = input("Enter phone number     : ").strip()
        if phonenumber.isdigit():
            break
        else:
            print("\033[91mInvalid phone number. Please enter number only.\033[0m")
    max_attempts = 3
    attempts = 0

    while attempts < max_attempts:
        password = str(input("Enter password         : "))
        confirmpass = str(input("Enter confirm password : "))
        
        if password == confirmpass:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            next_id = users[-1]['id'] + 1 if users else 1

            with open("users_details.txt", "a") as f:
                f.write(f"{next_id}|{fullname}|{email}|{address}|{phonenumber}|{hashed_password}\n")

            print("\n\033[96mPassword confirmed! Registration successful.\033[0m")
            input("Press Enter to continue...")
            return
        else:
            attempts += 1
            remaining = max_attempts - attempts
            if remaining > 0:
                print(f"\033[91mPasswords do not match. You have {remaining} attempt(s) left.\033[0m\n")
            else:
                input("\033[91mToo many failed attempts. Press enter to continue....\033[0m")
                return

def login():
    global user_id
    clear_screen()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("                          Login                          ")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        email = str(input("Enter your email    : "))
        password = str(input("Enter your password : "))
        hidden_password = hashlib.sha256(password.encode()).hexdigest()

        users = load_user_details("login")

        found = False
        for user in users:
            if email == user['email'] and hidden_password == user['password']:
                found = True
                clear_screen()
                print("╔" + "═" * 50 + "╗")
                print("║" + " " * 50 + "║")

                welcome_msg = f"Welcome, {user['fullname']}!"
                centered_msg = welcome_msg.center(50)
                print(f"║{centered_msg}║")

                print("║" + " " * 50 + "║")
                print("╚" + "═" * 50 + "╝")
                input("\nPress Enter to continue...")
                clear_screen()
                user_id = user['id']
                menu()
                return  # Exit function if login successful
                break

        if not found:
            # Try staff.txt
            users = load_admin_details("login")
            if email == "manager@gmail.com" and password == "manager@123":
                found = True
                clear_screen()
                print("╔" + "═" * 50 + "╗")
                print("║" + " " * 50 + "║")

                welcome_msg = f"Welcome, Manager!"
                centered_msg = welcome_msg.center(50)
                print(f"║{centered_msg}║")

                print("║" + " " * 50 + "║")
                print("╚" + "═" * 50 + "╝")
                input("\nPress Enter to continue...")
                clear_screen()
                user_id = "S1"
                admin_dashboard("superadmin") # when admin part add in this file than menu() change to admin_menu()
                return  # Exit function if login successful
            else :
                for user in users:
                    if email == user['email'] and hidden_password == user['password']:
                        found = True
                        clear_screen()
                        print("╔" + "═" * 50 + "╗")
                        print("║" + " " * 50 + "║")

                        welcome_msg = f"Welcome, {user['fullname']} staff!"
                        centered_msg = welcome_msg.center(50)
                        print(f"║{centered_msg}║")

                        print("║" + " " * 50 + "║")
                        print("╚" + "═" * 50 + "╝")
                        input("\nPress Enter to continue...")
                        clear_screen()
                        user_id = user['id']
                        admin_dashboard("admin") # when admin part add in this file than menu() change to admin_menu()
                        return  # Exit function if login successful
                    
        # If login fails
        attempts += 1
        remaining = max_attempts - attempts
        if remaining > 0:
            print(f"\033[91mInvalid email or password. You have {remaining} attempt(s) left.\033[0m\n")
        else:
            input("\033[91mToo many failed login attempts. Press enter to continue...\033[0m")
            return

def save_products(products, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for p in products:
            line = f"{p['product_id']}|{p['category_id']}|{p['product_name']}|{p['price']}|{p['stock']}|{p['details']}\n"
            file.write(line)

def show_categories(categories):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("                        Category                        ")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    for category_id, category_name in categories.items():
        print(f"{category_id}. {category_name}")
    print("\n0. Go Back main menu")

def show_product_detail(product):
    clear_screen()
    # print(f"Product ID  : {product['product_id']}")
    print(f"Name        : {product['product_name']}")
    print(f"Price       : ${product['price']}")
    print(f"Stock       : {product['stock']}")
    print(f"Details     : {product['details']}")
    print("\n0. Go back main menu")
    if int(product['stock']) > 0:
        print("1. Add to cart")
    else:
        print("\033[91mOut of stock - Cannot add to cart\033[0m")

def add_to_cart(user_id, product, products, product_file):
    if int(product['stock']) == 0:
        print("❌ Cannot add to cart. This product is out of stock.")
        input("Press Enter to continue...")
        return

    while True:
        try:
            quantity = int(input("Enter quantity to add: "))
            if quantity <= 0:
                print("Please enter a valid quantity greater than 0.")
                continue
            elif quantity > int(product['stock']):
                print("\033[91mQuantity exceeds stock. Please enter a smaller number.\033[0m")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    total_price = float(product['price']) * quantity
    with open('user_shoppingcart.txt', 'a', encoding='utf-8') as f:
        f.write(f"{user_id}|{product['product_name']}|{quantity}|{product['price']}|{total_price:.2f}\n")

    # 更新库存
    product['stock'] = str(int(product['stock']) - quantity)
    save_products(products, product_file)
    print("\033[96mProduct added to cart!\033[0m")
    input("Press Enter to continue...")

def show_products_by_category(products, category_id, category_name):
    clear_screen()
    print(f"Products in Category {category_name}:")
    print("~" * 40)
    
    # Filter products by category
    category_products = [p for p in products if p['category_id'] == category_id]
    
    if not category_products:
        print("\033[91mNo products found in this category.\033[0m")
        print("\n0. Go back main menu")
        return None, None
    
    # Add sorting options with input validation
    while True:
        clear_screen()
        print(f"Products in Category {category_name}:")
        print("~" * 40)
        print("\nSort by:")
        print("1. Price (Low to High)")
        print("2. Price (High to Low)")
        print("3. Name (A-Z)")
        print("4. Name (Z-A)")
        print("0. Skip sorting")
        
        sort_choice = input("\nEnter your choice: ").strip()
        
        if sort_choice == "0" or sort_choice == "":
            # No sorting - maintain original order but keep product_id as reference
            break
        elif sort_choice == "1":
            category_products.sort(key=lambda x: float(x['price']))
            break
        elif sort_choice == "2":
            category_products.sort(key=lambda x: float(x['price']), reverse=True)
            break
        elif sort_choice == "3":
            category_products.sort(key=lambda x: x['product_name'].lower())
            break
        elif sort_choice == "4":
            category_products.sort(key=lambda x: x['product_name'].lower(), reverse=True)
            break
        else:
            input("\033[91mInvalid choice. Please enter 1-4 or 0 to skip. Press Enter to try again...\033[0m")
            continue
    
    # Display products with both original product_id and sequential numbering
    clear_screen()
    print(f"Products in Category {category_name}:")
    print("~" * 40)
    
    # Create a mapping between display numbers and actual products
    numbered_products = list(enumerate(category_products, start=1))
    product_mapping = {str(num): product for num, product in numbered_products}
    
    for num, product in numbered_products:
        print(f"{num}. {product['product_name']} - ${product['price']}")
    
    print("\n0. Go back main menu")
    
    # Return both the numbered products list and the mapping
    return numbered_products, product_mapping

def category():
    product_file = "product.txt"
    categories = load_categories("category.txt")
    products = load_products(product_file)
    global user_id

    clear_screen()

    while True:
        clear_screen()
        show_categories(categories)
        # Add search option
        print("\nEnter 's' to search products")
        selected_option = input("\nEnter a category ID to view its products or option: ").strip().lower()
        
        if selected_option == "0":
            clear_screen()
            break
        elif selected_option == "s":
            # Search functionality
            search_term = input("Enter product name to search: ").strip().lower()
            found_products = [p for p in products if search_term in p['product_name'].lower()]
            
            if not found_products:
                input("\033[91mNo products found. Press Enter to continue...\033[0m")
                continue
                
            # Create a mapping between display numbers and actual products
            numbered_products = list(enumerate(found_products, start=1))
            product_mapping = {str(num): product for num, product in numbered_products}
            
            # Display search results with sequential numbers
            clear_screen()
            print(f"Search results for '{search_term}':")
            print("~" * 40)
            for num, product in numbered_products:
                category_name = categories.get(product['category_id'], "Unknown Category")
                print(f"{num}. {product['product_name']} (Category: {category_name}) - ${product['price']}")
            
            # Allow viewing product details from search results
            selected_number = input("\nEnter product number to see details (or 0 to go back): ").strip()
            if selected_number == "0":
                continue
                
            # Get the actual product using the mapping
            product = product_mapping.get(selected_number)
            if product:
                while True:
                    show_product_detail(product)
                    choice = input("Choose an option: ").strip()
                    if choice == "0":
                        break
                    elif choice == "1":
                        if int(product['stock']) > 0:
                            add_to_cart(user_id, product, products, product_file)
                        else:
                            input("\033[91mThis product is out of stock. Cannot add to cart.\033[0m")
                        break
                    else:
                        input("\033[91mInvalid code. Please press Enter to try again.\033[0m")
            else:
                input("\033[91mInvalid product number. Please press Enter to try again.\033[0m")
                
        elif selected_option in categories:
            
            while True:
                numbered_products, product_mapping = show_products_by_category(products, selected_option, categories[selected_option])
                if numbered_products is None:  # No products in category
                    break
                                    
                selected_number = input("\nEnter a product number to see details (or 0 to go back): ").strip()
                if selected_number == "0":
                    break
                                
                # Get the actual product using the mapping
                product = product_mapping.get(selected_number)
                if product:
                    while True:
                        show_product_detail(product)
                        choice = input("Choose an option: ").strip()
                        if choice == "0":
                            break
                        elif choice == "1":
                            if int(product['stock']) > 0:
                                add_to_cart(user_id, product, products, product_file)
                            else:
                                input("\033[91mThis product is out of stock. Cannot add to cart.\033[0m")
                            break
                        else:
                            input("\033[91mInvalid code. Please press Enter to try again.\033[0m")
                    break  # Exit product detail loop
                else:
                    input("\033[91mInvalid product number. Please press Enter to try again.\033[0m")
        else:
            input("\033[91mInvalid category ID or option. Please press Enter to try again.\033[0m")

def load_cart(filename="user_shoppingcart.txt"):
    cart = []
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    user_id, product_name, quantity, unit_price, total_price = parts
                    cart.append({
                        'user_id': user_id.strip(),
                        'product_name': product_name.strip(),
                        'quantity': int(quantity),
                        'unit_price': float(unit_price),
                        'total_price': float(total_price)
                    })
    return cart

def save_cart(cart, filename="user_shoppingcart.txt"):
    with open(filename, 'w', encoding='utf-8') as f:
        for item in cart:
            f.write(f"{item['user_id']}|{item['product_name']}|{item['quantity']}|{item['unit_price']}|{item['total_price']}\n")

def view_and_purchase(cart, user_id):
    while True:
        user_cart = [item for item in cart if item['user_id'] == str(user_id)]

        if not user_cart:
            print("\033[91mThe cart is empty.\033[0m")
            input("Press Enter to continue...")
            return cart
        
        clear_screen()
        print(f"\n{'No':<4} {'|Product':<37} {'|Quantity':<13} {'|Unit Price':<14} {'|Total':<10}")
        print("=====+=====================================+=============+==============+==============")
        for idx, item in enumerate(user_cart, 1):
            print(f"{idx:<4} | {item['product_name']:<35} | {item['quantity']:<11} | ${item['unit_price']:<11.2f} | ${item['total_price']:<9.2f}")
        
        print("\n0. Go back main menu")
        choice = input("\nEnter the numbers of items to purchase (e.g. 1,2 or -1 for all): ").strip()

        if choice == '0':
            return cart
        
        # Calculate selected items and total amount
        if choice == '-1':
            selected_items = user_cart.copy()
        else:
            try:
                # First validate all input numbers
                input_numbers = [x.strip() for x in choice.split(',')]
                invalid_numbers = [num for num in input_numbers if not num.isdigit() or int(num) < 1 or int(num) > len(user_cart)]
                
                if invalid_numbers:
                    print(f"\033[91mInvalid item numbers: {', '.join(invalid_numbers)}. Please enter numbers between 1 and {len(user_cart)}.\033[0m")
                    input("Press Enter to try again...")
                    continue
                
                # All numbers are valid, get the items
                indices = [int(x) for x in input_numbers]
                selected_items = [user_cart[i-1] for i in indices]
                
                if not selected_items:
                    print("\033[91mNo valid items selected.\033[0m")
                    input("Press Enter to try again...")
                    continue
                    
            except Exception as e:
                print(f"\033[91mInvalid input format: {e}. Please try again.\033[0m")
                input("Press Enter to try again...")
                continue
        
        # Calculate total for selected items only
        total_amount = sum(item['total_price'] for item in selected_items)
        
        # Payment method selection
        while True:
            clear_screen()
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("                     Payment Method                     ")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(f"Total Amount: ${total_amount:.2f}")
            print("\n1. Cash on Delivery")
            print("2. Visa")
            print("0. Cancel Purchase")
            
            payment_choice = input("\nSelect payment method: ").strip()
            
            if payment_choice == '0':
                return cart
            elif payment_choice == '1':
                payment_method = "Cash on Delivery"
                payment_details = "N/A"
                break
            elif payment_choice == '2':
                while True:
                    clear_screen()
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    print("                         Visa Payment                   ")
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    
                    # Enhanced Visa card number input with auto-formatting
                    while True:
                        card_number = input("Enter Visa card number (16 digits, starts with 4): ").replace(" ", "").replace("-", "")
                        if not card_number.isdigit():
                            print("\033[91mCard number must contain only digits.\033[0m")
                            continue
                        if len(card_number) != 16:
                            print("\033[91mCard number must be exactly 16 digits.\033[0m")
                            continue
                        if not card_number.startswith('4'):
                            print("\033[91mVisa cards must start with 4.\033[0m")
                            continue
                        break
                    
                    # Format the card number for display as user types
                    formatted_card = ' '.join([card_number[i:i+4] for i in range(0, 16, 4)])
                    print(f"Formatted card: {formatted_card}")
                    
                    # Enhanced expiry date validation
                    while True:
                        expiry_date = input("Enter expiry date (MM/YY): ").strip()
                        if len(expiry_date) != 5 or expiry_date[2] != '/':
                            print("\033[91mInvalid format. Use MM/YY (e.g. 12/25).\033[0m")
                            continue
                        
                        try:
                            month = int(expiry_date[:2])
                            year = int(expiry_date[3:])
                            current_year = datetime.now().year % 100
                            current_month = datetime.now().month
                            
                            # Validate month
                            if month < 1 or month > 12:
                                print("\033[91mInvalid month. Must be between 01-12.\033[0m")
                                continue
                            
                            # Validate year (current year to current year + 5)
                            if year < current_year or year > current_year + 5:
                                print(f"\033[91mExpiry year must be between {current_year} and {current_year + 5}.\033[0m")
                                continue
                            
                            # If current year, check month hasn't passed
                            if year == current_year and month < current_month:
                                print("\033[91mThis card has already expired.\033[0m")
                                continue
                            
                            break
                        except ValueError:
                            print("\033[91mInvalid date. Use numbers only (e.g. 12/25).\033[0m")
                    
                    # CVV validation
                    while True:
                        cvv = input("Enter CVV (3 digits): ").strip()
                        if len(cvv) != 3 or not cvv.isdigit():
                            print("\033[91mInvalid CVV. Must be exactly 3 digits.\033[0m")
                            continue
                        break
                    
                    masked_card = f"****-****-****-{card_number[-4:]}"
                    payment_method = "Visa"
                    payment_details = f"Card: {masked_card}, Exp: {expiry_date}"
                    break
                break
            else:
                print("\033[91mInvalid choice. Please try again.\033[0m")
                input("Press Enter to continue...")
        
        # Generate and display receipt
        order_datetime = datetime.now()
        formatted_datetime = order_datetime.strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            # Create receipt folder if it doesn't exist
            if not os.path.exists('receipt'):
                os.makedirs('receipt')
            
            # Generate a unique filename for the receipt
            receipt_filename = f"receipt/receipt_{user_id}_{order_datetime.strftime('%Y%m%d_%H%M%S')}.txt"
            
            # Save receipt to file
            with open(receipt_filename, 'w', encoding='utf-8') as f:
                f.write("============================================================\n")
                f.write("                      PURCHASE RECEIPT                      \n")
                f.write("============================================================\n")
                f.write(f"Order Date: {formatted_datetime}\n")
                f.write(f"User ID: {user_id}\n")
                f.write(f"Payment Method: {payment_method}\n")
                if payment_method == "Visa":
                    f.write(f"Payment Details: {payment_details}\n")
                f.write("\n")
                f.write(f"{'Product':<30} {'Qty':<5} {'Price':<10} {'Total':<10}\n")
                f.write("-" * 55 + "\n")
                
                for item in selected_items:
                    f.write(f"{item['product_name'][:29]:<30} {item['quantity']:<5} ${item['unit_price']:<9.2f} ${item['total_price']:<9.2f}\n")
                f.write("\n")
                f.write(f"{'Total Amount:':<45} ${total_amount:.2f}\n")
                f.write("============================================================\n")
                f.write("                Thank you for your purchase!                \n")
                f.write("============================================================\n")
            
            # Save to order history
            with open("orderhistory.txt", 'a', encoding='utf-8') as f:
                for item in selected_items:
                    f.write(f"{item['user_id']}|{item['product_name']}|{item['quantity']}|{item['unit_price']}|{item['total_price']}|{formatted_datetime}|{payment_method}|{payment_details}\n")
            
            # Display receipt to user
            clear_screen()
            print("============================================================")
            print("                      PURCHASE RECEIPT                      ")
            print("============================================================")
            print(f"Order Date: {formatted_datetime}")
            print(f"Payment Method: {payment_method}")
            if payment_method == "Visa":
                print(f"Payment Details: {payment_details}")
            print("\n")
            print(f"{'Product':<30} {'Qty':<5} {'Price':<10} {'Total':<10}")
            print("-" * 55)
            
            for item in selected_items:
                print(f"{item['product_name'][:29]:<30} {item['quantity']:<5} ${item['unit_price']:<9.2f} ${item['total_price']:<9.2f}")
            print("\n")
            print(f"\033[33m{'Total Amount:':<45} ${total_amount:.2f}\033[0m")
            print("============================================================")
            print("                Thank you for your purchase!                ")
            print("============================================================")
            
            # Remove purchased items from cart
            for item in selected_items:
                cart.remove(item)
            
            input("\nPress Enter to return to main menu...")
            return cart
            
        except Exception as e:
            print(f"\033[91mError processing payment: {e}\033[0m")
            input("Press Enter to try again...")
            continue
               
def delete_items(cart, user_id):
    while True:
        user_cart = [item for item in cart if item['user_id'] == str(user_id)]

        if not user_cart:
            print("\033[91mThe cart is empty.\033[0m")
            input("Press Enter to continue...")
            return cart

        clear_screen()
        print(f"{'No':<4} {'|Product':<35} {'|Quantity':<12} {'|Unit Price':<15} {'|Total':<12}")
        print("=====+=====================================+============+===============+==============")
        for idx, item in enumerate(user_cart, 1):
            print(f"{idx:<4} | {item['product_name']:<35} | {item['quantity']:<10} | ${item['unit_price']:<11.2f} | ${item['total_price']:<9.2f}")

        print("\n0. Go back main menu")

        try:
            choice = input("\nEnter the numbers of items to delete (e.g. 1,2): ").strip()

            if choice == '0':
                print("\033[91mDeletion cancelled.\033[0m")
                input("Press Enter to continue...")
                return cart

            indices = [int(x) for x in choice.split('|') if x.strip().isdigit()]
            selected_items = [user_cart[i - 1] for i in indices if 1 <= i <= len(user_cart)]

            if not selected_items:
                print("\033[91mNo valid items selected.\033[0m")
                input("Press Enter to try again...")
                continue  # Go back to top to re-display table

            for item in selected_items:
                cart.remove(item)

            print("\033[96mSelected items deleted from cart.\033[0m")
            input("Press Enter to continue...")
            return cart  # Exit function after successful deletion

        except Exception as e:
            print(f"\033[91mError: {e}\033[0m")
            input("Press Enter to try again...")
            continue  # Re-display table on error

def view_order_history(history, user_id):
    user_history = [item for item in history if item['user_id'] == str(user_id)]
    if not user_history:
        print("\033[91mNo order history found.\033[0m")
        input("Press Enter to return to main menu...")
        return

    grouped_orders = defaultdict(list)
    for item in user_history:
        grouped_orders[item['timestamp']].append(item)

    clear_screen()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("                                    Order History                                    ")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    for timestamp in sorted(grouped_orders.keys()):
        order_group = grouped_orders[timestamp]
        first_item = order_group[0]
        
        print(f"\n🕒 Order Time: {timestamp}")
        print(f"💳 Payment Method: {first_item['payment_method']}")
        if first_item['payment_method'] == "Visa":
            print(f"🔒 Payment Details: {first_item['payment_details']}")
            
        print(f"\n{'No':<4} {'|Product':<37} {'|Quantity':<12} {'|Unit Price':<15} {'|Total':<10}")
        print("=====+=====================================+============+===============+==============")
        group_total = 0
        for idx, item in enumerate(order_group, 1):
            print(f"{idx:<4} | {item['product_name']:<35} | {item['quantity']:<10} | ${item['unit_price']:<12.2f} | ${item['total_price']:<9.2f}")
            group_total += item['total_price']
        print(f"\033[33m{'':<52} Subtotal: ${group_total:.2f}\033[0m")

    print("\n\033[92mEnd of all order history.\033[0m")
    input("Press Enter to return to main menu...")
    clear_screen()
    
def view_profile(user):
    clear_screen()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("                      View Profile                      ")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"Username      : {user['fullname']}")
    print(f"Email         : {user['email']}")
    print(f"Home address  : {user['address']}")
    print(f"Phone number  : {user['phonenumber']}")
    input("\nPress Enter to return to main menu...")

# 更新资料
def update_profile(user, users):
    while True:
        clear_screen()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("                     Update Profile                     ")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("1. Name")
        print("2. Email")
        print("3. Password")
        print("4. Home address")
        print("5. Phone number")
        print("\n0. Go back main menu")
        choice = input("Please enter your choice: ").strip()

        old_email = user["email"]

        if choice == "1":
            print("\n=======================================")
            new_name = input("Enter new username: ").strip()
            if new_name:
                user["fullname"] = new_name
                # Update the user in the users list
                for u in users:
                    if u['id'] == user['id']:
                        u['fullname'] = new_name
                        break
                save_users(users)
                input("\033[96mUsername updated.Press enter to continue...\033[0m")
                break

        elif choice == "2":
            while True:
                print("\n=======================================")
                new_email = input("Enter new email: ").strip()
                
                if "@" not in new_email or "." not in new_email:
                    print("\033[91mInvalid email. Must contain '@' and '.'.\033[0m")
                    continue
                    
                if new_email:
                    if any(u['email'] == new_email for u in users if u['id'] != user['id']):
                        input("\033[91mEmail already in use by another account. Press Enter to try again...\033[0m")
                        continue
                    
                    user["email"] = new_email
                    for u in users:
                        if u['id'] == user['id']:
                            u['email'] = new_email
                            break
                    save_users(users)
                    input("\033[96mEmail updated. Press enter to continue...\033[0m")
                    break

        elif choice == "3":
            while True:
                print("\n=======================================")
                new_pass = input("Enter new password: ").strip()
                confirm_pass = input("Confirm password: ").strip()
                if new_pass and new_pass == confirm_pass:
                    new_hash = hashlib.sha256(new_pass.encode()).hexdigest()
                    user["password"] = new_hash
                    # Update the user in the users list
                    for u in users:
                        if u['id'] == user['id']:
                            u['password'] = new_hash
                            break
                    save_users(users)
                    input("\033[96mPassword updated.Press enter to continue...\033[0m")
                    break
                else:
                    print("\033[91mPasswords do not match.\033[0m")
                    retry = input("Do you want to try again? (y/n): ").strip().lower()
                    if retry != 'y':
                        return
            break

        elif choice == "4":
            print("\n=======================================")
            new_address = input("Enter new home address: ").strip()
            if new_address:
                user["address"] = new_address
                for u in users:
                    if u['id'] == user['id']:
                        u['address'] = new_address
                        break
                save_users(users)
                input("\033[96mAddress updated. Press enter to continue...\033[0m")
                break
            
        elif choice == "5": 
            while True:
                print("\n=======================================")
                new_phone = input("Enter new phone number: ").strip()
                if new_phone.isdigit():
                    user["phonenumber"] = new_phone
                    for u in users:
                        if u['id'] == user['id']:
                            u['phonenumber'] = new_phone
                            break
                    save_users(users)
                    input("\033[96mPhone number updated.Press enter to continue...\033[0m")
                    break
                else:
                    print("\033[91mInvalid phone number. Please enter number only.\033[0m")

        elif choice == "0":
            return
        else:
            input("\033[91mInvalid choice. Press Enter to try again...\033[0m")

    save_users(users)
    # input("Press Enter to return to menu...")

# def category():
#     product_file = "product.txt"
#     categories = load_categories("category.txt")
#     products = load_products(product_file)
#     global user_id

#     clear_screen()

#     while True:
#         clear_screen()
#         show_categories(categories)
        
#         selected_category = input("\nEnter a category ID to view its products : ").strip()
#         if selected_category == "0":
#             clear_screen()
#             break
#         elif selected_category in categories:
#             while True:
#                 show_products_by_category(products, selected_category, categories[selected_category])
#                 selected_product = input("\nEnter a product ID to see details (or 0 to go back): ").strip()
#                 if selected_product == "0":
#                     break
#                 product = next((p for p in products if p['product_id'] == selected_product and p['category_id'] == selected_category), None)
#                 if product:
#                     while True:
#                         show_product_detail(product)
#                         choice = input("Choose an option: ").strip()
#                         if choice == "0":
#                             break
#                         elif choice == "1":
#                             if int(product['stock']) > 0:
#                                 add_to_cart(user_id, product, products, product_file)
#                             else:
#                                 input("\033[91mThis product is out of stock. Cannot add to cart.\033[0m")
#                             break
#                         else:
#                             input("\033[91mInvalid code. Please press Enter to try again.\033[0m")
#                     break  # Exit product detail loop
#                 else:
#                     input("\033[91mInvalid product ID. Please press Enter to try again.\033[0m")
#         else:
#             input("\033[91mInvalid category ID. Please press Enter to try again.\033[0m")

def shoppingcart():
    cart = load_cart()
    global user_id
    while True:
        clear_screen()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("                     Shopping Cart                      ")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")        
        print("1. View Shopping Cart & Purchase")
        print("2. Delete Items from Cart")
        print("\n0. Go back main menu")
        choice = input("Choose an option : ").strip()
        clear_screen()
        if choice == "1":
            cart = view_and_purchase(cart, user_id)
            save_cart(cart)
        elif choice == "2":
            cart = delete_items(cart, user_id)
            save_cart(cart)
        elif choice == "0":
            break
        else:
            input("\033[91mInvalid choice. Press Enter to try again...\033[0m")

def orderhistory():
    global user_id
    history = load_order_history()
    view_order_history(history, user_id)

def show_feedback_menu():
    clear_screen()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("                        Feedback                        ")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")    
    print("1. Product")
    print("2. Staff")
    print("\n0. Go back main menu")

def feedback():
    global user_id

    while True:
        show_feedback_menu()
        choice = input("Please enter your choice : ")
        if choice == '1':
            title = 'Product'
            break
        elif choice == '2':
            title = 'Staff'
            break
        elif choice == '0':
            clear_screen()
            menu()
            return
        else:
            print("\033[91mInvalid input. Please enter again.\033[0m")
            input("Press Enter to continue...")

    user_input = input("Enter your FeedBack : ")
    
    with open("feedback.txt", "a", encoding="utf-8") as f:
        f.write(f"{user_id}|{title}|{user_input}\n")
    
    input("\033[96mYour FeedBack already saving. Thank you!\033[0m")
    clear_screen()

def profile(user_id):
    users = load_user_details("profile")  # This loads all users
    user = None
    print(user_id)    

    # Find the current user
    for u in users:
        if user_id == u['id']:
            user = u
            break
    if user:
        while True:
            clear_screen()
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("                          Profile                       ")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("1. View Profile")
            print("2. Update Profile")
            print("\n0. Go back main menu")
            option = input("Please enter your choice: ").strip()

            if option == "1":
                view_profile(user)
            elif option == "2":
                update_profile(user, users)  # Pass both current user and all users
            elif option == "0":
                clear_screen()
                break
            else:
                input("\033[91mInvalid option. Press Enter to try again...\033[0m")
    else:
        print("User not found")
        input("Press Enter to continue...")

def check_order_status():
    global user_id
    
    def parse_order_line(line):
        parts = line.strip().split('|')
        if len(parts) >= 9:  # 确保有足够的部分
            return {
                'user_id': parts[0],
                'product_name': parts[1],
                'quantity': parts[2],
                'unit_price': parts[3],
                'total_price': parts[4],
                'timestamp': parts[5],
                'payment_method': parts[6],
                'payment_details': parts[7],
                'status': parts[8] if len(parts) >= 9 else 'Pending'  # 默认Pending
            }
        return None

    # 直接读取orderhistory.txt文件
    try:
        with open('orderhistory.txt', 'r', encoding='utf-8') as f:
            orders = [parse_order_line(line) for line in f if parse_order_line(line)]
    except FileNotFoundError:
        print("\033[91mOrder history file not found.\033[0m")
        input("Press Enter to return to main menu...")
        return

    # 筛选当前用户的订单
    user_orders = [order for order in orders if order['user_id'] == str(user_id)]
    
    if not user_orders:
        print("\033[91mNo orders found for your account.\033[0m")
        input("Press Enter to return to main menu...")
        return

    # 按状态分组
    status_groups = {'Pending': [], 'Delivery': [], 'Completed': []}
    for order in user_orders:
        status = order['status']
        if status in status_groups:
            status_groups[status].append(order)
        else:
            status_groups['Pending'].append(order)  # 未知状态默认为Pending

    clear_screen()
    print("==================================================")
    print("                YOUR ORDER STATUS                ")
    print("==================================================")
    
    # 显示各状态订单
    for status, orders in status_groups.items():
        if not orders:
            continue
            
        print(f"\n{status.upper()} ORDERS ({len(orders)})")
        print("=" * 50)
        print(f"{'Date':<12} {'Product':<25} {'Status':<12}")
        print("-" * 50)
        
        for order in sorted(orders, key=lambda x: x['timestamp'], reverse=True):
            date = order['timestamp'].split()[0]  # 只取日期部分
            product = order['product_name'][:24] + '...' if len(order['product_name']) > 24 else order['product_name']
            print(f"{date:<12} {product:<25} {order['status']:<12}")
    
    input("\nPress Enter to continue...")


def menu():
    global user_id
    while True:
        clear_screen()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("                Welcome to Dog Food Shop                ")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("1. Product List")
        print("2. Shopping Cart")
        print("3. Purchase History")
        print("4. Check Order Status")  # New option added here
        print("5. FeedBack")
        print("6. Profile")
        print("0. Logout")

        menu_choose = input("\nEnter number of module you need to continue : ")

        try:
            menu_choose = int(menu_choose)
        except ValueError:
            print("\033[91mInvalid input. Please enter a number.\033[0m")
            input("\nPress Enter to return to the menu...")
            continue

        match menu_choose:
            case 1:
                category()
            case 2:
                shoppingcart()
            case 3:
                orderhistory()
            case 4:  # New case for checking order status
                check_order_status()
            case 5:
                feedback()
            case 6:
                profile(user_id)
            case 0:
                break
            case _:
                print("\033[91mInvalid input. Please choose between 0-6.\033[0m")
                input("\nPress Enter to return to the menu...")
                

# ------------------------------- admin module --------------------------------------------------------------------------
def show_main_menu(role):
    clear_screen()
    print("========== Admin Dashboard ==========")
    print("=====================================")
    print("1. Manage Category")
    print("2. Manage Product")
    print("3. Manage Order")
    print("4. Manage Feedback")
    print("5. Report")
    if role == "superadmin":
        print("6. Manage Staff Account")
    else:
        print("6. Profile")
    print("\n0. Logout")

def load_data(filename, delimiter="|"):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as file:
        reader = csv.reader(file, delimiter=delimiter)
        return list(reader)

def save_data(filename, data, delimiter="|"):
    with open(filename, "w", newline='') as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerows(data)
# manage category
def manage_category():
    file = "category.txt"

    def load_data(file):
        try:
            with open(file, "r") as f:
                lines = f.readlines()
            # Only include valid rows with at least ID and Category Name
            return [line.strip().split("|") for line in lines if "|" in line and len(line.strip().split("|")) == 2]
        except FileNotFoundError:
            return []

    def save_data(file, data):
        with open(file, "w") as f:
            for row in data:
                f.write("|".join(row) + "\n")

    data = load_data(file)

    def view_categories():
        clear_screen()
        print("-" * 50)
        print(" " * 18 + "Category List")
        print("-" * 50)
        print(f"{'Category ID':<12} | {'Category Name'}")
        print("-" * 50)
        for row in data:
            if len(row) >= 2:
                print(f"{row[0]:<12} | {row[1]}")
        print("-" * 50)

    def add_category():
        nonlocal data
        name = input("Enter new category name: ").strip()
        if not name:
            print("\033[91mCategory name cannot be empty.\033[0m")
        elif any(row[1].lower() == name.lower() for row in data):
            print("\033[91mCategory already exists.\033[0m")
        else:
            new_id = str(int(data[-1][0]) + 1 if data else 1)
            data.append([new_id, name])
            save_data(file, data)
            input("\033[96mCategory added successfully. Press Enter to continue...\033[0m")
        input("enter")

    def edit_category():
        nonlocal data
        edit_id = input("Enter ID to edit: ").strip()
        for row in data:
            if row[0] == edit_id:
                print(f"\nCurrent name: {row[1]}")
                new_name = input("Enter new category name: ").strip()
                if not new_name:
                    print("\033[91mName cannot be empty.\033[0m")
                elif any(r[1].lower() == new_name.lower() and r[0] != edit_id for r in data):
                    print("\033[91mDuplicate category name.\033[0m")
                else:
                    row[1] = new_name
                    save_data(file, data)
                    print("\033[96mCategory updated.\033[0m")
                break
        else:
            print("\033[91mCategory ID not found.\033[0m")
        input("Press Enter to continue...")

    def delete_category():
        nonlocal data
        del_id = input("Enter ID to delete: ").strip()
        if any(row[0] == del_id for row in data):
            data = [row for row in data if row[0] != del_id]
            save_data(file, data)
            print("\033[96mCategory deleted.\033[0m")
        else:
            print("\033[91mCategory ID not found.\033[0m")
        input("Press Enter to continue...")

    while True:
        clear_screen()
        print("========== Manage Category ==========")
        print("=====================================")
        print("1. View Categories")
        print("2. Add Category")
        print("3. Edit Category")
        print("4. Delete Category")
        print("\n0. Go back Main Menu")
        choice = input("\nSelect option: ").strip()

        if choice == "1":
            view_categories()
            input("\nPress Enter to continue...")
        elif choice == "2":
            clear_screen()
            view_categories()
            add_category()
        elif choice == "3":
            clear_screen()
            view_categories()
            edit_category()
        elif choice == "4":
            clear_screen()
            view_categories()
            delete_category()
        elif choice == "0":
            break
        else:
            input("\033[91mInvalid option. Press Enter to try again...\033[0m")
# manage product
def manage_product():
    file = "product.txt"
    data = load_data(file, delimiter="|")
    
    while True:
        clear_screen()
        display_product_list(data, status_filter="active")
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("     Manage Product     ")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("1. Add Product")
        print("2. Edit Product")
        print("3. Delete Product")
        print("4. Restore Deleted Product")
        print("\n0. Go back Main Menu")
        choice = input("\nSelect option: ")

        if choice == "1":
            clear_screen()
            display_product_list(data, status_filter="active")
            display_categories()
            category_id = input("\nEnter Category ID    : ")
            while not is_valid_category_id(category_id):
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
            input("\033[96mProduct added.Press Enter to continue...\033[0m")

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
                        while not is_valid_category_id(category_id):
                            print("\nInvalid Category ID. Please select from the list.")
                            new_cat = input("Enter Category ID    : ")
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
                        print("\033[91mEdit cancelled.\033[0m")
                    else:
                        print("\033[91mInvalid option.\033[0m")
                    break
            if found:
                save_data(file, data, delimiter="|")
                print("\033[96mProduct updated.\033[0m")
            else:
                print("\033[91mActive product not found.\033[0m")
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
                print(f"\033[96mProduct ID {del_id} marked as deleted.\033[0m")
            else:
                print("\033[91mActive product not found.\033[0m")
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
                print("\033[96mProduct restored.\033[0m")
            else:
                print("\033[91mDeleted product not found.\033[0m")
            input("Press Enter to continue...")

        elif choice == "0":
            break
        else:
            input("\033[91mInvalid option. Press Enter to continue...\033[0m")

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
            f"{get_category_name_by_id(row_data[1]):<{col_widths[1]}} | "
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

def display_categories():
    cfile = "category.txt"
    cdata = load_data(cfile)

    if not cdata:
        print("No categories found.")
        return

    headers = ["ID", "Name"]

    # 计算每一列的最大宽度（包括标题）
    col_widths = [
        max(len(headers[i]), max(len(row[i]) for row in cdata)) for i in range(len(headers))
    ]

    # 打印标题线
    print("\n" + "=" * (sum(col_widths) + len(col_widths) * 3 + 1))
    print("|", end="")
    for i, header in enumerate(headers):
        print(f" {header:<{col_widths[i]}} |", end="")
    print()
    print("=" * (sum(col_widths) + len(col_widths) * 3 + 1))

    # 打印数据行
    for row in cdata:
        print("|", end="")
        for i, cell in enumerate(row):
            print(f" {cell:<{col_widths[i]}} |", end="")
        print()
    print("=" * (sum(col_widths) + len(col_widths) * 3 + 1))


def get_category_name_by_id(category_id):
    cfile = "category.txt"
    cdata = load_data(cfile)
    for row in cdata:
        if row[0] == category_id:
            return row[1]
    return "Category"

def is_valid_category_id(category_id):
    cdata = load_data("category.txt", delimiter="|")
    return any(row[0].strip() == category_id.strip() for row in cdata)

# manage order
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
        print("========== Order Management =========")
        print("=====================================")
        print("1. View all orders")
        print("2. Filter by payment method")
        print("3. Filter by Delivery Status")
        print("4. Update Delivery Status")
        print("\n0. Go back main menu")
        choice = input("\nSelect an option: ")

        if choice == "1":
            clear_screen()
            display_orders(orders, "ALL ORDERS")

        elif choice == "2":
            clear_screen()
            print("Filter Options:")
            print("1. Visa")
            print("2. Cash on Delivery")
            while True:
                method_choice = input("Please enter your choice:  ")

                method = ""
                if method_choice == "1":
                    method = "Visa"
                    break
                elif method_choice == "2":
                    method = "Cash on Delivery"
                    break
                else:
                    input("\033[91mInvalid Method option. Please press Enter to try again.\033[0m")
                    
            if method:
                filtered = [o for o in orders if o['PaymentMethod'].lower() == method.lower()]
                title = f"Orders Paid by {method}"
            else:
                filtered = orders
                title = "All Orders (No Filter)"

            clear_screen()
            display_orders(filtered, title)

        elif choice == "3":
            clear_screen()
            print("Filter Status:")
            print("1. Pending")
            print("2. Delivery")
            print("3. Completed")
            while True:
                status_choice = input("Please enter your choice:   ")

                status = ""
                if status_choice == "1":
                    status = "Pending"
                    break
                elif status_choice == "2":
                    status = "Delivery"
                    break
                elif status_choice == "3":
                    status = "Completed"
                    break
                else:
                    input("\033[91mInvalid Status option. Please press Enter to try again.\033[0m")

            if status:
                filtered = [o for o in orders if o['DeliveryStatus'] == status]
                title = f"Orders with Status: {status}"
            else:
                filtered = orders
                title = "All Orders (No Filter)"

            clear_screen()
            display_orders(filtered, title)

        elif choice == "4":
            clear_screen()
            display_orders(orders, "All Orders", show_footer=False, pause=False)
            oid_str = input("Enter Order ID to update status: ").strip()
            if not oid_str.isdigit():
                input("\033[91mInvalid Order ID. Press Enter to continue...\033[0m")
                continue
            oid = int(oid_str)
            if 1 <= oid <= len(orders):
                current_status = orders[oid-1]['DeliveryStatus']
                print(f"\nCurrent status: {current_status}")
                print("\nSelect new status:")
                print("1. Pending")
                print("2. Delivery")
                print("3. Completed")
                print("0. Cancel")
                
                status_choice = input("\nEnter your choice: ").strip()
                
                if status_choice == "1":
                    new_status = "Pending"
                elif status_choice == "2":
                    new_status = "Delivery"
                elif status_choice == "3":
                    new_status = "Completed"
                elif status_choice == "0":
                    print("\033[91mStatus update cancelled.\033[0m")
                    input("Press Enter to continue...")
                    continue
                else:
                    input("\033[91mInvalid choice. Press Enter to continue...\033[0m")
                    continue
                
                # Validate status transition
                valid_transitions = {
                    "Pending": ["Delivery"],
                    "Delivery": ["Completed"],
                    "Completed": []
                }
                
                if current_status in valid_transitions and new_status in valid_transitions[current_status]:
                    orders[oid-1]['DeliveryStatus'] = new_status
                    save_orders(orders)
                    print(f"\033[96mOrder {oid} status updated to {new_status}.\033[0m")
                else:
                    print(f"\033[91mInvalid status transition from {current_status} to {new_status}.\033[0m")
                    print("Allowed transitions:")
                    print(f"- Pending → Delivery")
                    print(f"- Delivery → Completed")
                
            else:
                print(f"\033[91mNo order found with Order ID {oid}.\033[0m")
            input("Press Enter to continue...")

        elif choice == "0":
            break
        else:
            input("\033[91mInvalid option. Press Enter to continue...\033[0m")

def parse_order_line(line, order_id):
    parts = line.strip().split('|')
    if len(parts) >= 8:  # Changed from 9 to 8 since we'll add status if missing
        # If status is missing (old records), default to Pending
        status = parts[8] if len(parts) >= 9 else "Pending"
        return {
            'CustomerID': parts[0],
            'Product': parts[1],
            'Quantity': int(parts[2]),
            'Price': float(parts[3]),
            'Total': float(parts[4]),
            'DateTime': parts[5],
            'PaymentMethod': parts[6],
            'PaymentDetails': parts[7],
            'DeliveryStatus': status
        }
    return None

def save_orders(orders):
    try:
        with open("orderhistory.txt", "w") as file:
            for o in orders:
                # Ensure all fields exist, defaulting empty ones
                line = "|".join([
                    o.get('CustomerID', ''),
                    o.get('Product', ''),
                    str(o.get('Quantity', 0)),
                    f"{o.get('Price', 0):.2f}",
                    f"{o.get('Total', 0):.2f}",
                    o.get('DateTime', ''),
                    o.get('PaymentMethod', ''),
                    o.get('PaymentDetails', ''),
                    o.get('DeliveryStatus', 'Pending')  # Default to Pending if missing
                ])
                file.write(line + "\n")
    except Exception as e:
        print(f"Error saving orders: {e}")

def display_orders(orders, title="", show_footer=True, pause=True):
    headers = ["Order_ID", "CustomerID", "Product", "Qty", "Price", "Total", "DateTime", "Payment", "Details", "Status"]
    col_widths = [9, 10, 30, 5, 8, 10, 19, 16, 30, 10]

    def format_row(data):
        return " | ".join(f"{str(data[i])[:col_widths[i]]:<{col_widths[i]}}" for i in range(len(data)))

    total_width = sum(col_widths) + 3 * (len(col_widths) - 1)
    print("-" * total_width)
    if title:
        print(f"{title:^{total_width}}")
        print("-" * total_width)
    print(format_row(headers))
    print("-" * total_width)

    for idx, o in enumerate(orders, start=1):
        row = [
            idx,
            o['CustomerID'],
            o['Product'],
            o['Quantity'],
            f"{o['Price']:.2f}",
            f"{o['Total']:.2f}",
            o['DateTime'],
            o['PaymentMethod'],
            o['PaymentDetails'],
            o['DeliveryStatus']
        ]
        print(format_row(row))

    print("-" * total_width)
    if show_footer:
        print(f"\033[93mTotal Orders : {len(orders)}\033[0m")
        total_amount = sum(o['Total'] for o in orders)
        print(f"\033[93mTotal Revenue: RM {total_amount:.2f}\033[0m")
    if pause:
        input("\nPress Enter to continue...")

# show feedback
def manage_feedback():
    clear_screen()
    
    # Load feedback data
    feedback_data = load_data("feedback.txt")
    
    # Load user data to map IDs to usernames
    users = {}
    try:
        with open("users_details.txt", 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 2:  # At least ID and username
                    users[parts[0]] = parts[1]  # Map ID to username
    except FileNotFoundError:
        print("User data file not found.")
        input("\nPress Enter to return...")
        return

    if not feedback_data:
        print("No feedback entries found.")
        input("\nPress Enter to return...")
        return

    # Prepare table data
    table_data = []
    for row in feedback_data:
        if len(row) >= 3:  # Ensure we have ID, title, and feedback
            user_id = row[0]
            username = users.get(user_id, f"Unknown (ID: {user_id})")
            title = row[1]
            feedback = row[2]
            table_data.append([username, title, feedback])

    # Display table
    print("================================ FEEDBACK ENTRIES ========================================")
    print(f"{'Username':<20} | {'Type':<15} | {'Feedback':<50}")
    print("="*90)
    
    for entry in table_data:
        username, title, feedback = entry
        # Split long feedback into multiple lines if needed
        feedback_lines = [feedback[i:i+50] for i in range(0, len(feedback), 50)]
        
        # Print first line with username and title
        print(f"{username[:19]:<20} | {title[:14]:<15} | {feedback_lines[0][:49]:<50}")
        
        # Print remaining feedback lines (if any) with empty username and title columns
        for line in feedback_lines[1:]:
            print(f"{'':<20} | {'':<15} | {line[:49]:<50}")
        
        print("-"*90)  # Separator between entries

    input("\nPress Enter to return...")
# generate report
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
        print(f"\n\033[93mTotal Revenue: RM{total:.2f}\033[0m")
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
        print(f"\n\033[93mTotal Revenue: RM{total:.2f}\033[0m")
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
        print(f"\n\033[93mTotal Revenue: RM{total:.2f}\033[0m")
    except ValueError:
        print("❌ Invalid year format. Use YYYY.")

    input("\nPress Enter to return...")

def show_report_menu():
    while True:
        clear_screen()
        print("========= Report Management =========")
        print("=====================================")
        print("1. Daily Report")
        print("2. Monthly Report")
        print("3. Annual Report")
        print("\n0. Go back main menu")
        choice = input("Select report type: ")

        if choice == "1":
            while True:
                clear_screen()
                print("~~~~~ Daily Report ~~~~~")
                print("1. Search by date")
                print("2. Today's report")
                print("\n0. Back")
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
                print("~~~~~ Monthly Report ~~~~~")
                print("1. Search by month")
                print("2. This month's report")
                print("\n0. Back")
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
                print("~~~~~ Annual Report ~~~~~")
                print("1. Search by year")
                print("2. This year's report")
                print("\n0. Back")
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
            admin_dashboard("superadmin")
            break
        else:
            input("\033[91mInvalid Report Type or option. Please press Enter to try again.\033[0m")
# manage staff account
def show_staff():
    clear_screen()
    staff_list = load_admin_details("profile")
    
    if not staff_list:
        print("No staff members found.")
        input("\nPress Enter to return...")
        return

    # Define column widths
    col_widths = {
        'id': 4,
        'fullname': 20,
        'email': 25,
        'address': 25,
        'phonenumber': 15
    }

    # Create the header
    headers = [
        "ID".center(col_widths['id']),
        "Name".center(col_widths['fullname']),
        "Email".center(col_widths['email']),
        "Address".center(col_widths['address']),
        "Phone".center(col_widths['phonenumber'])
    ]
    
    # Print table header
    print("╔" + "═"*(col_widths['id']+2) + "╦" + 
          "═"*(col_widths['fullname']+2) + "╦" + 
          "═"*(col_widths['email']+2) + "╦" + 
          "═"*(col_widths['address']+2) + "╦" + 
          "═"*(col_widths['phonenumber']+2) + "╗")
    
    print("║ " + " ║ ".join(headers) + " ║")
    
    print("╠" + "═"*(col_widths['id']+2) + "╬" + 
          "═"*(col_widths['fullname']+2) + "╬" + 
          "═"*(col_widths['email']+2) + "╬" + 
          "═"*(col_widths['address']+2) + "╬" + 
          "═"*(col_widths['phonenumber']+2) + "╣")

    # Print each staff member's information
    for staff in staff_list:
        id_col = str(staff['id']).center(col_widths['id'])
        name_col = staff['fullname'][:col_widths['fullname']].ljust(col_widths['fullname'])
        email_col = staff['email'][:col_widths['email']].ljust(col_widths['email'])
        address_col = staff['address'][:col_widths['address']].ljust(col_widths['address'])
        phone_col = staff['phonenumber'][:col_widths['phonenumber']].ljust(col_widths['phonenumber'])
        
        print(f"║ {id_col} ║ {name_col} ║ {email_col} ║ {address_col} ║ {phone_col} ║")
    
    # Print table footer
    print("╚" + "═"*(col_widths['id']+2) + "╩" + 
          "═"*(col_widths['fullname']+2) + "╩" + 
          "═"*(col_widths['email']+2) + "╩" + 
          "═"*(col_widths['address']+2) + "╩" + 
          "═"*(col_widths['phonenumber']+2) + "╝")
    
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

    print("\033[96mStaff added successfully.\033[0m")
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
        print("\033[96mStaff deleted successfully.\033[0m")
    input("Press Enter to return...")

def manage_staff_account():
    while True:
        clear_screen()
        print("======== Manage Staff Account =======")
        print("=====================================")
        print("1. Show staff")
        print("2. Add staff")
        print("3. Delete staff")
        print("\n0. Go back main menu")
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
            input("\033[91mInvalid choice. Press Enter to try again...\033[0m")

def show_profile(user_id):
    admin_details = load_admin_details("profile")
    for staff in admin_details:
        if staff["id"] == user_id:
            print(f"\n--- Profile Info ---")
            print(f"Name    : {staff['fullname']}")
            print(f"Email   : {staff['email']}")
            print(f"Address : {staff['address']}")
            print(f"Phone   : {staff['phonenumber']}")
            return
    print("User not found.")

def edit_profile(user_id):
    admin_details = load_admin_details("profile")
    found = False

    for staff in admin_details:
        if staff["id"] == user_id:
            found = True
            while True:
                clear_screen()
                print("=== Edit Profile ===")
                print("1. Name")
                print("2. Email")
                print("3. Address")
                print("4. Phone Number")
                print("5. Password")
                print("0. Save and Return")
                choice = input("Enter your choice: ")

                if choice == "1":
                    staff['fullname'] = input(f"New Name [{staff['fullname']}]: ") or staff['fullname']
                elif choice == "2":
                    staff['email'] = input(f"New Email [{staff['email']}]: ") or staff['email']
                elif choice == "3":
                    staff['address'] = input(f"New Address [{staff['address']}]: ") or staff['address']
                elif choice == "4":
                    staff['phonenumber'] = input(f"New Phone Number [{staff['phonenumber']}]: ") or staff['phonenumber']
                elif choice == "5":
                    new_password = input("Enter New Password: ")
                    confirm_password = input("Confirm Password: ")
                    if new_password == confirm_password:
                        staff['password'] = hashlib.sha256(new_password.encode()).hexdigest()
                        print("\033[96mPassword updated successfully.\033[0m")
                    else:
                        print("Passwords do not match.")
                        input("Press Enter to continue...")
                elif choice == "0":
                    break
                else:
                    print("Invalid choice.")
                    input("Press Enter to continue...")

            break  # done editing

    if found:
        # 保存更改到 staff.txt
        with open("staff.txt", "w", encoding="utf-8") as f:
            for staff in admin_details:
                line = f"{staff['id']}|{staff['fullname']}|{staff['email']}|{staff['address']}|{staff['phonenumber']}|{staff['password']}\n"
                f.write(line)
        print("\n\033[96mProfile updated successfully.\033[0m")
    else:
        print("User not found.")

def admin_profile(user_id):
    while True:
        clear_screen()
        print("=== Profile Menu ===")
        print("1. Show Profile")
        print("2. Edit Profile")
        print("0. Back")
        choice = input("Enter choice: ")
        
        if choice == "1":
            clear_screen()
            show_profile(user_id)
            input("\nPress Enter to return...")
        elif choice == "2":
            clear_screen()
            edit_profile(user_id)
            input("\nPress Enter to return...")
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
            input("Press Enter to continue...")

# admin dashboard
def admin_dashboard(role):
    global user_id
    while True:
        show_main_menu(role)
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
            if role == "admin":
                admin_profile(user_id)
            else:
                manage_staff_account()
        elif choice == "0":
            print("Logging out...\n")
            break
        else:
            input("\033[91mInvalid choice. Please select a valid option. Press Enter to continue...\033[0m")

while True:
    clear_screen()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("                Welcome to Dog Food Shop                ")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("1. Login")
    print("2. Register")
    print("\n0. Exit")
    first_choose = input("Please Enter your choice : ")

    if first_choose == "1":
        login()
        # break
    elif first_choose == "2":
        register()
        # break
    elif first_choose == "0":
        exit()
    else:
        input("\033[91m\nInvalid input.Press Enter to try again...\033[0m")
        clear_screen()
