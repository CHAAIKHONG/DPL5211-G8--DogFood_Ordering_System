import os
from collections import defaultdict

from collections import defaultdict

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


def main():
    history = load_order_history()
    user_id = input("🔍 Enter your User ID to view order history: ").strip()
    view_order_history(history, user_id)

if __name__ == "__main__":
    main()
