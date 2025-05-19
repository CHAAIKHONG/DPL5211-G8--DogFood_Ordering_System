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
                parts = line.strip().split(',')
                if len(parts) == 4:
                    if method == "register" or method == "login" or method == "profile":
                        id, fullname, email, password = parts
                        user_details.append({
                            'id': int(id),
                            'fullname': fullname.strip(),
                            'email': email.strip(),
                            'password': password.strip(),
                        })
                    elif method == "profile":
                        id, username, email, password_hash = parts
                        user_details = {
                            "id": int(id),
                            "username": username.strip(),
                            "email": email.strip(),
                            "password_hash": password_hash.strip()
                        }

    return user_details

def load_categories(filename):
    categories = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip().replace('，', ',')
                if line:
                    parts = line.split(',')
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
                line = line.strip().replace('，', ',')
                if line:
                    parts = line.split(',')
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
                parts = line.strip().split(',')
                if len(parts) != 6:
                    print(f"[❌ Line {line_num}] Skipped - Expected 6 parts but got {len(parts)}: {line.strip()}")
                    continue
                try:
                    user_id, product_name, quantity, unit_price, total_price, timestamp = parts
                    history.append({
                        'timestamp': timestamp.strip(),
                        'user_id': user_id.strip(),
                        'product_name': product_name.strip(),
                        'quantity': int(quantity),
                        'unit_price': float(unit_price),
                        'total_price': float(total_price)
                    })
                except ValueError as e:
                    print(f"[❌ Line {line_num}] Error converting values: {e}")
    return history

def save_users(users, filename="users_details.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for user in users.values():
            f.write(f"{user['id']},{user['fullname']},{user['email']},{user['password_hash']}\n")

def register():
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("                       Register                         ")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    checkpass = False
    while not checkpass:
        fullname = str(input("Enter your fullname : "))
        email = str(input("Enter your email    : "))
        password = str(input("Enter your password : "))
        confirmpass = str(input("Enter confirm your password : "))

        if password == confirmpass:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            users = load_user_details("register")
            next_id = users[-1]['id'] + 1 if users else 1

            with open("users_details.txt", "a") as f:
                f.write(f"{next_id},{fullname},{email},{hashed_password}\n")

            print("Password confirmed! Registration successful.")
            input("Press Enter to continue...")
            checkpass = True
        else:
            print("Passwords do not match. Please try again.\n")

def login():
    global user_id
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("                           Login                        ")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    verify = False

    while not verify:
        email = str(input("Enter your email    : "))
        password = str(input("Enter your password : "))
        hidden_password = hashlib.sha256(password.encode()).hexdigest()
        users = load_user_details("login")

        for user in users:
            if email == user['email'] and hidden_password == user['password']:
                print(f"Welcome, {user['fullname']}")
                user_id = user['id']
                verify = True
                menu()
                break

        if not verify:
            print("Invalid email or password. Please try again.")

def save_products(products, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for p in products:
            line = f"{p['product_id']},{p['category_id']},{p['product_name']},{p['price']},{p['stock']},{p['details']}\n"
            file.write(line)

def show_categories(categories):
    print("Category List:")
    print("-" * 30)
    for category_id, category_name in categories.items():
        print(f"{category_id}. {category_name}")
    print("0. Exit")

def show_products_by_category(products, category_id, category_name):
    clear_screen()
    print(f"Products in Category {category_name}:")
    print("-" * 30)
    found = False
    for product in products:
        if product['category_id'] == category_id:
            print(f"{product['product_id']}. {product['product_name']} - ${product['price']}")
            found = True
    if not found:
        print("No products found in this category.")
    print("\n0. Back")

def show_product_detail(product):
    clear_screen()
    print(f"Product ID: {product['product_id']}")
    print(f"Name: {product['product_name']}")
    print(f"Price: ${product['price']}")
    print(f"Stock: {product['stock']}")
    print(f"Details: {product['details']}")
    print("\n0. Back")
    if int(product['stock']) > 0:
        print("1. Add to cart")
    else:
        print("❌ Out of stock - Cannot add to cart")

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
                print("Quantity exceeds stock. Please enter a smaller number.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    total_price = float(product['price']) * quantity
    with open('user_shoppingcart.txt', 'a', encoding='utf-8') as f:
        f.write(f"{user_id},{product['product_name']},{quantity},{product['price']},{total_price:.2f}\n")

    # 更新库存
    product['stock'] = str(int(product['stock']) - quantity)
    save_products(products, product_file)
    print("✅ Product added to cart!")
    input("Press Enter to continue...")

def load_cart(filename="user_shoppingcart.txt"):
    cart = []
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(',')
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
            f.write(f"{item['user_id']},{item['product_name']},{item['quantity']},{item['unit_price']},{item['total_price']}\n")

def view_and_purchase(cart, user_id):
    user_cart = [item for item in cart if item['user_id'] == user_id]
    if not user_cart:
        print("🛒 The cart is empty or the User ID does not exist.")
        return cart

    print(f"\n🛍️ Shopping cart for user {user_id}:")
    print(f"\n{'No':<4} {'|Product':<37} {'|Quantity':<13} {'|Unit Price':<14} {'|Total':<10}")
    print("=====+=====================================+=============+==============+==============")
    for idx, item in enumerate(user_cart, 1):
        print(f"{idx:<4} | {item['product_name']:<35} | {item['quantity']:<11} | ${item['unit_price']:<11.2f} | ${item['total_price']:<9.2f}")

    try:
        choice = input("\nEnter the numbers of items to purchase (e.g. 1,2) or -1 for all, or 0 to go back menu: ").strip()
        if choice == '0':
            return cart
        elif choice == '-1':
            selected_items = user_cart
        else:
            indices = [int(x) for x in choice.split(',') if x.strip().isdigit()]
            selected_items = [user_cart[i - 1] for i in indices if 1 <= i <= len(user_cart)]

        if not selected_items:
            print("❌ No valid items selected.")
            return cart

        # 获取当前下单时间
        order_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Save selected items to order history
        with open("orderhistory.txt", 'a', encoding='utf-8') as f:
            for item in selected_items:
                f.write(f"{item['user_id']},{item['product_name']},{item['quantity']},{item['unit_price']},{item['total_price']},{order_datetime}\n")

        # Remove selected items from cart
        for item in selected_items:
            cart.remove(item)

        print("✅ Purchase completed and saved to orderhistory.txt")
    except Exception as e:
        print(f"❌ Error: {e}")
    return cart

def delete_items(cart, user_id):
    user_cart = [item for item in cart if item['user_id'] == user_id]
    if not user_cart:
        print("🛒 The cart is empty or the User ID does not exist.")
        return cart

    print(f"\n🗑️ Delete items from cart for user {user_id}:")
    print(f"{'No':<4} {'|Product':<35} {'|Quantity':<10} {'|Unit Price':<13} {'|Total':<10}")
    print("=====+===================================+============+===============+==============")
    for idx, item in enumerate(user_cart, 1):
        print(f"{idx:<4} | {item['product_name']:<35} | {item['quantity']:<10} | ${item['unit_price']:<11.2f} | ${item['total_price']:<9.2f}")

    try:
        choice = input("\nEnter the numbers of items to delete (e.g. 1,2) or 0 to go back menu: ").strip()
        if choice == '0':
            print("❌ Deletion cancelled.")
            return cart

        indices = [int(x) for x in choice.split(',') if x.strip().isdigit()]
        selected_items = [user_cart[i - 1] for i in indices if 1 <= i <= len(user_cart)]

        if not selected_items:
            print("❌ No valid items selected.")
            return cart

        for item in selected_items:
            cart.remove(item)

        print("✅ Selected items deleted from cart.")
    except Exception as e:
        print(f"❌ Error: {e}")
    return cart

def view_order_history(history, user_id):
    user_history = [item for item in history if item['user_id'] == user_id]
    if not user_history:
        print(f"📦 No order history found for User ID {user_id}.")
        return

    # Group by timestamp
    grouped_orders = defaultdict(list)
    for item in user_history:
        grouped_orders[item['timestamp']].append(item)

    print(f"\n📄 Order History for User {user_id}:")

    for timestamp in sorted(grouped_orders.keys()):
        print(f"\n🕒 Order Time: {timestamp}")
        print(f"{'No':<4} {'|Product':<37} {'|Quantity':<12} {'|Unit Price':<15} {'|Total':<10}")
        print("=====+=====================================+============+===============+==============")
        group_total = 0
        for idx, item in enumerate(grouped_orders[timestamp], 1):
            print(f"{idx:<4} | {item['product_name']:<35} | {item['quantity']:<10} | ${item['unit_price']:<12.2f} | ${item['total_price']:<9.2f}")
            group_total += item['total_price']
        print(f"{'':<52} Subtotal: ${group_total:.2f}")

def view_profile(user):
    clear_screen()
    print("📄 Your Profile:")
    print(f"👤 Username : {user['fullname']}")
    print(f"📧 Email    : {user['email']}")
    input("\nPress Enter to return to menu...")

# 更新资料
def update_profile(user, users):
    while True:
        clear_screen()
        print("✏️ What would you like to update?")
        print("1. Name")
        print("2. Email")
        print("3. Password")
        print("4. Cancel")
        choice = input("Enter option (1-4): ").strip()

        old_email = user["email"]

        if choice == "1":
            new_name = input("Enter new username: ").strip()
            if new_name:
                user["fullname"] = new_name
                print("✅ Username updated.")
                break

        elif choice == "2":
            new_email = input("Enter new email: ").strip()
            if new_email:
                user["email"] = new_email
                users[new_email] = user
                del users[old_email]
                print("✅ Email updated.")
                break

        elif choice == "3":
            while True:
                new_pass = input("Enter new password: ").strip()
                confirm_pass = input("Confirm password: ").strip()
                if new_pass and new_pass == confirm_pass:
                    user["password_hash"] = hash_password(new_pass)
                    print("✅ Password updated.")
                    break
                else:
                    print("❌ Passwords do not match. Please try again.")
                    retry = input("Retry? (y/n): ").strip().lower()
                    if retry != 'y':
                        return
            break

        elif choice == "4":
            return
        else:
            print("❌ Invalid choice.")
            input("Press Enter to try again...")

    save_users(users)
    input("Press Enter to return to menu...")

def category():
    product_file = "product.txt"
    categories = load_categories("category.txt")
    products = load_products(product_file)
    global user_id

    clear_screen()

    while True:
        clear_screen()
        show_categories(categories)
        
        selected_category = input("\nEnter a category ID to view its products (or 0 to exit): ").strip()
        if selected_category == "0":
            print("Goodbye!")
            break
        elif selected_category in categories:
            while True:
                show_products_by_category(products, selected_category, categories[selected_category])
                selected_product = input("\nEnter a product ID to see details (or 0 to go back): ").strip()
                if selected_product == "0":
                    break
                product = next((p for p in products if p['product_id'] == selected_product and p['category_id'] == selected_category), None)
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
                                print("❌ This product is out of stock. Cannot add to cart.")
                                input("Press Enter to continue...")
                            break
                        else:
                            print("❌ Invalid code. Please try again.")
                            input("Press Enter to continue...")
                    break  # Exit product detail loop
                else:
                    print("❌ Invalid product ID. Please try again.")
                    input("Press Enter to continue...")
        else:
            print("❌ Invalid category ID. Please try again.")
            input("Press Enter to continue...")

def shoppingcart():
    cart = load_cart()
    global user_id
    while True:
        clear_screen()
        print("==== Shopping Cart System ====")
        print("1. View Shopping Cart & Purchase")
        print("2. Delete Items from Cart")
        print("3. Exit")
        choice = input("Choose an option (1-3): ").strip()
        clear_screen()
        if choice == "1":
            # user_id = input("Enter your User ID: ").strip()
            cart = view_and_purchase(cart, user_id)
            save_cart(cart)
        elif choice == "2":
            # user_id = input("Enter your User ID: ").strip()
            cart = delete_items(cart, user_id)
            save_cart(cart)
        elif choice == "3":
            print("Thank you! Exiting the program.")
            break
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")
        input("\nPress Enter to return to the menu...")

def orderhistory():
    global user_id
    history = load_order_history()
    view_order_history(history, user_id)

def feedback():
    global user_id
    print("Please select FeedBack type")
    print("1. Product")
    print("2. Staff")
    print("0. Back to Main Menu")
    
    while True:
        choice = input("Please enter (1 or 2) : ")
        if choice == '1':
            title = 'Product'
            break
        elif choice == '2':
            title = 'Staff'
            break
        elif choice == '0':
            menu()
            break
        else:
            print("Invalid input. Please enter again.")

    user_input = input("Enter your FeedBack : ")
    
    with open("feedback.txt", "a", encoding="utf-8") as f:
        f.write(f"{user_id},{title},{user_input}\n")
    
    print("Your FeedBack already saving. Thank you!")

def profile():
    global user_id
    # users = load_user_details("profile")
    # user = login(users) 
    user = load_user_details("profile")
    
    print(user)
    for user in user:
        if user_id == user['id']:
            while True:
                clear_screen()
                print("=== MENU ===")
                print("1. View Profile")
                print("2. Update Profile")
                print("3. Logout")
                option = input("Choose an option: ").strip()

                if option == "1":
                    view_profile(user)
                elif option == "2":
                    update_profile(user, user_id)
                elif option == "3":
                    print("👋 Logged out.")
                    break
                else:
                    print("❌ Invalid option.")
                    input("Press Enter to try again...")
        else:
            print("not user")

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
                print("Invalid input. Please choose between 0-5.")

while True:
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("                Welcome to Dog Food Shop                ")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("1. Login")
    print("2. Register")
    print("0. Exit")
    first_choose = int(input("You want to login our system or register new account. Please enter the number : "))

    if first_choose == 1:
        login()
        # break
    elif first_choose == 2:
        register()
        # break
    elif first_choose == 0:
        exit()
    else:
        clear_screen()
        print("Input Wrong. Numbers are 1 or 2 only. Please choose one time : ")
