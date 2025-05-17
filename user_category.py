import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

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


if __name__ == "__main__":
    product_file = "product.txt"
    categories = load_categories("category.txt")
    products = load_products(product_file)

    clear_screen()
    user_id = input("Enter your user ID: ").strip()

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


