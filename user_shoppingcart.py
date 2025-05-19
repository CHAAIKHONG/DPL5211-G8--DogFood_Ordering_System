import os
from datetime import datetime 

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


def main():
    cart = load_cart()
    while True:
        clear_screen()
        print("==== Shopping Cart System ====")
        print("1. View Shopping Cart & Purchase")
        print("2. Delete Items from Cart")
        print("3. Exit")
        choice = input("Choose an option (1-3): ").strip()
        clear_screen()
        if choice == "1":
            user_id = input("Enter your User ID: ").strip()
            cart = view_and_purchase(cart, user_id)
            save_cart(cart)
        elif choice == "2":
            user_id = input("Enter your User ID: ").strip()
            cart = delete_items(cart, user_id)
            save_cart(cart)
        elif choice == "3":
            print("Thank you! Exiting the program.")
            break
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")
        input("\nPress Enter to return to the menu...")

if __name__ == "__main__":
    main()
