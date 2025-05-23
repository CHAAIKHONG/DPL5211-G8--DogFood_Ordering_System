import hashlib
import os
from datetime import datetime 
from collections import defaultdict

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

# def register():
#     clear_screen()
#     print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#     print("                       Register                         ")
#     print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    
#     fullname = str(input("Enter username         : "))
#     # Email validation loop
#     while True:
#         email = str(input("Enter your email       : "))
#         if "@" in email and "." in email:
#             break
#         else:
#             print("\033[91mInvalid email. Please enter a valid email address (must contain '@' and '.').\033[0m\n")

#     address = str(input("Enter home address     : "))
#     while True:
#         phonenumber = input("Enter phone number     : ").strip()
#         if phonenumber.isdigit():
#             break
#         else:
#             print("\033[91mInvalid phone number. Please enter number only.\033[0m")
#     max_attempts = 3
#     attempts = 0

#     while attempts < max_attempts:
#         password = str(input("Enter password         : "))
#         confirmpass = str(input("Enter confirm password : "))
        
#         if password == confirmpass:
#             hashed_password = hashlib.sha256(password.encode()).hexdigest()
#             users = load_user_details("register")
#             next_id = users[-1]['id'] + 1 if users else 1

#             with open("users_details.txt", "a") as f:
#                 f.write(f"{next_id}|{fullname}|{email}|{address}|{phonenumber}|{hashed_password}\n")

#             print("\n\033[96mPassword confirmed! Registration successful.\033[0m")
#             input("Press Enter to continue...")
#             return  # Exit the function successfully
#         else:
#             attempts += 1
#             remaining = max_attempts - attempts
#             if remaining > 0:
#                 print(f"\033[91mPasswords do not match. You have {remaining} attempt(s) left.\033[0m\n")
#             else:
#                 input("\033[91mToo many failed attempts.Press enter to continue....\033[0m")
#                 return

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
            for user in users:
                if email == user['email'] and hidden_password == user['password']:
                    found = True
                    clear_screen()
                    print("╔" + "═" * 50 + "╗")
                    print("║" + " " * 50 + "║")

                    welcome_msg = f"Welcome, {user['fullname']} satff!"
                    centered_msg = welcome_msg.center(50)
                    print(f"║{centered_msg}║")

                    print("║" + " " * 50 + "║")
                    print("╚" + "═" * 50 + "╝")
                    input("\nPress Enter to continue...")
                    clear_screen()
                    user_id = user['id']
                    menu() # when admin part add in this file than menu() change to admin_menu()
                    return  # Exit function if login successful
                    break

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
    print("\n0. Go Back Menu")

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
        
        print("\n0. Go back to main menu")
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

        print("\n0. Go back to main menu")

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
    print("\0. Go back main menu")

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

def profile():
    global user_id
    users = load_user_details("profile")  # This loads all users
    user = None
    
    # Find the current user
    for u in users:
        if user_id == u['id']:
            user = u
            break
            
    if user:
        while True:
            clear_screen()
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("                          Menu                          ")
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

def menu():
    while True:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("                Welcome to Dog Food Shop                ")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("1. Product List")
        print("2. Shopping Cart")
        print("3. Purchase History")
        print("4. FeedBack")
        print("5. Profile")
        print("0. Logout")

        menu_choose = int(input("\nEnter number of module you need to continue : "))

        match menu_choose:
            case 1:
                # print("case 1")
                category()
                # break
            case 2:
                # print("case 2")
                shoppingcart()
                # break
            case 3:
                # print("case 3")
                orderhistory()
                # break
            case 4:
                # print("case 4")
                feedback()
                # break
            case 5:
                # print("case 5")
                profile()
                # break
            case 0:
                print("case 0")
                break
            case _:
                print("\033[91mInvalid input. Please choose between 0-5.\033[0m")
                input("\nPress Enter to return to the menu...")
                clear_screen()

while True:
    clear_screen()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("                Welcome to Dog Food Shop                ")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("1. Login")
    print("2. Register")
    print("\n0. Exit")
    first_choose = int(input("Please Enter your choice : "))

    if first_choose == 1:
        login()
        # break
    elif first_choose == 2:
        register()
        # break
    elif first_choose == 0:
        exit()
    else:
        input("\033[91m\nInvalid input.Press Enter to try again...\033[0m")
        clear_screen()
