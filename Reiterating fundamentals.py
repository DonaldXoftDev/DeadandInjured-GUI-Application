# # --- THE RAW DATA ---
#
# initial_inventory = [
#     {"name": "Laptop", "stock": 10, "price": 1200, "reorder_level": 3},
#     {"name": "Mouse", "stock": 50, "price": 25, "reorder_level": 10},
#     {"name": "Monitor", "stock": 5, "price": 300, "reorder_level": 2},
#     {"name": "Keyboard", "stock": 8, "price": 75, "reorder_level": 5},
# ]
#
# orders = [
#     {"name": "Laptop", "qty": 2},
#     {"name": "Monitor", "qty": 4},
#     {"name": "Laptop", "qty": 10},
#     {"name": "Mouse", "qty": 45},
#     {"name": "Keyboard", "qty": 5},
# ]
#
# # --- THE STRUCTURE ---
#
# class Product:
#     def __init__(self, name, stock, price, reorder_level):
#         pass
#
# class WarehouseReportVM:
#     def __init__(self, product: Product):
#         pass
#
# class WarehouseProcessor:
#     def __init__(self, products: list[Product]):
#         pass
#
#     def process_orders(self, orders_list: list[dict]):
#         pass
#
# if __name__ == "__main__":
#     # Your execution logic here
#     pass


def is_unique(code: str) -> bool:
    clean_string = code.strip()
    return len(set(clean_string)) == 4

test_1 = '2345'
test_2 = '2448'
tests = [test_1, test_2]

results = []
for test in tests:
    unique = is_unique(test)
    results.append(unique)

print(results)

