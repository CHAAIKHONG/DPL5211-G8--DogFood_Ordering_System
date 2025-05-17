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
                    if len(parts) == 3:
                        product_id = parts[0].strip()
                        category_id = parts[1].strip()
                        product_name = parts[2].strip()
                        products.append({
                            'product_id': product_id,
                            'category_id': category_id,
                            'product_name': product_name
                        })
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    return products


def show_categories(categories):
    print("Category List:")
    print("-" * 30)
    for category_id, category_name in categories.items():
        print(f"{category_id}. {category_name}")


def show_products_by_category(products, category_id):
    print(f"\nProducts in Category {category_id}:")
    found = False
    for product in products:
        if product['category_id'] == category_id:
            print(f"- {product['product_name']}")
            found = True
    if not found:
        print("No products found in this category.")


if __name__ == "__main__":
    categories = load_categories("category.txt")
    products = load_products("product.txt")
    
    show_categories(categories)

    selected_id = input("\nEnter a category ID to view its products (e.g. 1, 2, 3): ").strip()

    if selected_id in categories:
        show_products_by_category(products, selected_id)
    else:
        print("Invalid category ID.")
