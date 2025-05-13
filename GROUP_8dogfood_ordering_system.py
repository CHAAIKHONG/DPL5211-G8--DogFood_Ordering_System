import hashlib

def register():
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("                       Register                         ")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    checkpass = False
    while not checkpass:
        fullname = str(input("Enter your fullname : "))
        email = str(input("Enter your email : "))
        password = str(input("Enter your password : "))
        confirmpass = str(input("Enter confirm your passwrd : "))

        if password == confirmpass:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            with open("users.txt", "a") as f:
                f.write(f"{fullname},{email},{hashed_password}\n")

            print("Password confirmed! Registration successful.")
            input("Press Enter to continue...")
            checkpass = True
        else:
            print("Passwords do not match. Please try again.\n")


print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("                Welcome to Dog Food Shop                ")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("")
register()
