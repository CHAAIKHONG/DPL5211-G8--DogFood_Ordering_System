import hashlib
import os

# 清除屏幕
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# 加密密码
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 载入用户资料（以 Email 为 Key）
def load_users(filename="users_details.txt"):
    users = {}
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 4:
                    user_id, username, email, password_hash = parts
                    users[email] = {
                        "user_id": user_id,
                        "username": username,
                        "email": email,
                        "password_hash": password_hash
                    }
    return users

# 保存用户资料
def save_users(users, filename="users_details.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for user in users.values():
            f.write(f"{user['user_id']},{user['username']},{user['email']},{user['password_hash']}\n")

# 登录功能（使用 Email）
def login(users):
    while True:
        clear_screen()
        print("🔐 LOGIN")
        email = input("📧 Email: ").strip()
        password = input("🔑 Password: ").strip()
        if email in users and users[email]["password_hash"] == hash_password(password):
            print(f"\n✅ Welcome, {users[email]['username']}!")
            return users[email]
        else:
            print("❌ Invalid email or password. Try again.")
            input("Press Enter to continue...")

# 显示资料
def view_profile(user):
    clear_screen()
    print("📄 Your Profile:")
    print(f"👤 Username : {user['username']}")
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
                user["username"] = new_name
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

# 主流程
def main():
    users = load_users()
    user = login(users)

    if user:
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
                update_profile(user, users)
            elif option == "3":
                print("👋 Logged out.")
                break
            else:
                print("❌ Invalid option.")
                input("Press Enter to try again...")

if __name__ == "__main__":
    main()
