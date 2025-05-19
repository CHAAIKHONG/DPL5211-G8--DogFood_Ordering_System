import hashlib
import os

user_id = None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_user_details(filename="users_details.txt"):
    user_details  = []
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 4:
                    id, fullname, email, password = parts
                    user_details.append({
                        'id': int(id),
                        'fullname': fullname.strip(),
                        'email': email.strip(),
                        'password': password.strip(),
                    })
    return user_details

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
            users = load_user_details()
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
        users = load_user_details()

        for user in users:
            if email == user['email'] and hidden_password == user['password']:
                print(f"Welcome, {user['fullname']}")
                user_id = user['id']
                verify = True
                menu()
                break

        if not verify:
            print("Invalid email or password. Please try again.")

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


# def profile():

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
                print("case 1")
                # show_categories(categories)
                # break
            case 2:
                print("case 2")
                # view_cart(cart, user_id)
                # break
            case 3:
                print("case 3")
                # break
            case 4:
                print("case 4")
                feedback()
                # break
            case 5:
                print("case 5")
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
