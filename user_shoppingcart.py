import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

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

def view_cart(cart, user_id):
    user_cart = [item for item in cart if item['user_id'] == user_id]
    if not user_cart:
        print("🛒 The cart is empty or the User ID does not exist.")
    else:
        print(f"\nShopping cart for user {user_id}:")
        print(f"\n{'Product':<35} {'|Quantity':<12} {'|Unit Price':<14} {'|Total':<14}")
        print("====================================+============+==============+==============")
        for item in user_cart:
            print(f"{item['product_name']:<35} | {item['quantity']:<10} | ${item['unit_price']:<11.2f} | ${item['total_price']:<11.2f}")
        total = sum(item['total_price'] for item in user_cart)
        print(f"\nTotal Amount: ${total:.2f}")


def delete_cart(cart, user_id):
    user_cart = [item for item in cart if item['user_id'] == user_id]
    if not user_cart:
        print("❌ No cart found for this user. Nothing was deleted.")
        return cart

    print(f"\nShopping cart for user {user_id}:")
    print(f"\n{'No':<4} {'|Product':<37} {'|Quantity':<12} {'|Unit Price':<14} {'|Total Price':<14}")
    print("=====+=====================================+============+==============+==============")
    for idx, item in enumerate(user_cart, 1):
        print(f"{idx:<4} | {item['product_name']:<35} | {item['quantity']:<10} | ${item['unit_price']:<11.2f} | ${item['total_price']:<11.2f}")

    try:
        choice = int(input("\nEnter the number of the product to delete (0 to cancel): "))
        if choice == 0:
            print("❌ Deletion cancelled.")
            return cart
        elif 1 <= choice <= len(user_cart):
            product_to_delete = user_cart[choice - 1]
            cart.remove(product_to_delete)
            print(f"✅ Product '{product_to_delete['product_name']}' has been removed from the cart.")
        else:
            print("❌ Invalid choice.")
    except ValueError:
        print("❌ Please enter a valid number.")

    return cart


def main():
    cart = load_cart()
    while True:
        clear_screen()
        print("==== Shopping Cart Menu ====")
        print("1. View Shopping Cart")
        print("2. Delete Shopping Cart")
        print("3. Exit")
        choice = input("Choose an option (1-3): ").strip()
        clear_screen()
        if choice == "1":
            user_id = input("Enter User ID: ").strip()
            view_cart(cart, user_id)
        elif choice == "2":
            user_id = input("Enter User ID to delete cart: ").strip()
            cart = delete_cart(cart, user_id)
            save_cart(cart)
        elif choice == "3":
            print("Thank you! Exiting the program.")
            break
        else:
            print("❌ Invalid choice. Please enter a number from 1 to 3.")

        input("\nPress Enter to return to the menu...")

if __name__ == "__main__":
    main()
