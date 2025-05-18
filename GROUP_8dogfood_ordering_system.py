import hashlib
import os

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
        confirmpass = str(input("Enter confirm your passwrd : "))

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
                verify = True
                menu()
                break
            
        if not verify:
            print("Invalid email or password. Please try again.")

# def feedback():

# def profile():

def menu():
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

    while True:
        match menu_choose:
            case 1:
                print("case 1")
                # show_categories(categories)
                break
            case 2:
                print("case 2")
                # view_cart(cart, user_id)
                break
            case 3:
                print("case 3")
                break
            case 4:
                print("case 4")
                break
            case 5:
                print("case 5")
                break
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
    else:
        clear_screen()
        print("Input Wrong. Numbers are 1 or 2 only. Please choose one time : ")
