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
                    if len(parts) >= 6:  # 新增price, stock, details
                        product_id = parts[0].strip()
                        category_id = parts[1].strip()
                        product_name = parts[2].strip()
                        price = parts[3].strip()
                        stock = parts[4].strip()
                        details = ','.join(parts[5:]).strip()  # 防止details中有逗号
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

if __name__ == "__main__":
    categories = load_categories("category.txt")
    products = load_products("product.txt")

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
                # 查找对应产品
                product = next((p for p in products if p['product_id'] == selected_product and p['category_id'] == selected_category), None)
                if product:
                    while True:
                        show_product_detail(product)
                        back = input("\nEnter 0 to go back: ").strip()
                        if back == "0":
                            break
                else:
                    print("Invalid product ID.")
                    input("Press Enter to continue...")
        else:
            print("Invalid category ID.")
            input("Press Enter to continue...")
