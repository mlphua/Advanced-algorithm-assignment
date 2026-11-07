"""Command-line Pharmacy Inventory System (Question 1).

Records live in BOTH a hash table and a plain list so that every search can
be timed against both structures.
"""
import time
from hash_table import HashTable
from product import Product

TABLE_SIZE = 31  # prime number -> spreads keys more evenly with key % size

SAMPLE_DATA = [
    (1042, "Paracetamol 500mg", 5.90, 120),
    (1073, "Ibuprofen 400mg", 8.50, 80),       # 1073 % 31 == 19 -> collides with 1042
    (1104, "Amoxicillin 250mg", 15.20, 45),    # 1104 % 31 == 19 -> collides again
    (2001, "Cetirizine 10mg", 7.30, 60),
    (2002, "Loratadine 10mg", 9.90, 55),
    (2003, "Omeprazole 20mg", 18.00, 40),
    (3002, "Cough Syrup 100ml", 12.80, 70),
    (4001, "Metformin 500mg", 11.00, 90),
    (4002, "Salbutamol Inhaler", 19.90, 30),
]


def linear_search(array, product_id):
    """Search a one-dimensional array (list) one element at a time."""
    for product in array:
        if product.product_id == product_id:
            return product
    return None


def read_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("  Please enter a whole number.")


def read_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  Please enter a number.")


def insert_product(table, array):
    pid = read_int("Enter Product ID: ")
    if table.search(pid) is not None:
        print("A product with this ID already exists.")
        return
    if table.is_full():
        print("Hash table is full. Cannot insert.")
        return
    name = input("Enter Product Name: ")
    price = read_float("Enter Price: ")
    stock = read_int("Enter Stock Quantity: ")
    try:
        product = Product(pid, name, price, stock)
    except ValueError as err:
        print(f"Invalid data: {err}")
        return
    slot = table.insert(pid, product)
    array.append(product)
    print(f"Product inserted successfully into slot [{slot}]")


REPEATS = 1000  # a single search takes ~1 microsecond, too small to time reliably


def average_seconds(func, repeats=REPEATS):
    """Run func many times and return the average seconds per call."""
    t0 = time.perf_counter_ns()
    for _ in range(repeats):
        func()
    return (time.perf_counter_ns() - t0) / repeats / 1e9


def search_product(table, array):
    pid = read_int("Enter Product ID to search: ")
    found = table.search(pid)
    hash_s = average_seconds(lambda: table.search(pid))
    array_s = average_seconds(lambda: linear_search(array, pid))

    if found is None:
        print("Product not found.")
    else:
        print("Product Found!")
        print(found)
    print(f"Search completed in {hash_s:.9f} seconds (Hash Table)")
    print(f"Search completed in {array_s:.9f} seconds (Array - same record)")
    print(f"(average of {REPEATS} repeated searches)")


def edit_product(table):
    pid = read_int("Enter Product ID to edit: ")
    product = table.search(pid)
    if product is None:
        print("Product not found.")
        return
    print(product)
    price = read_float("Enter new price: ")
    stock = read_int("Enter new stock quantity: ")
    if price < 0 or stock < 0:
        print("Price and stock cannot be negative.")
        return
    # The array holds the SAME object, so it is updated automatically.
    product.price, product.stock = price, stock
    print("Product updated.")


def delete_product(table, array):
    pid = read_int("Enter Product ID to delete: ")
    product = table.search(pid)
    if product is None:
        print("Product not found.")
        return
    table.delete(pid)
    array.remove(product)
    print("Product deleted.")


def display_table(table):
    print(f"Hash table size: {table.size} | Records: {len(table)} "
          f"| Load factor: {table.load_factor():.2f}")
    for slot_no, key, product in table.items():
        home = hash(key) % table.size
        note = "" if home == slot_no else f"  (collision, home slot was {home})"
        print(f"[{slot_no:2}] {product}{note}")


def main():
    table = HashTable(TABLE_SIZE)
    array = []
    for pid, name, price, stock in SAMPLE_DATA:
        product = Product(pid, name, price, stock)
        table.insert(pid, product)
        array.append(product)

    try:
        while True:
            print("\n==== Pharmacy Inventory System ====")
            print("1. Insert Product")
            print("2. Search Product")
            print("3. Edit Product")
            print("4. Delete Product")
            print("5. Display Hash Table")
            print("6. Exit")
            choice = input("Enter choice: ").strip()
            if choice == "1":
                insert_product(table, array)
            elif choice == "2":
                search_product(table, array)
            elif choice == "3":
                edit_product(table)
            elif choice == "4":
                delete_product(table, array)
            elif choice == "5":
                display_table(table)
            elif choice == "6":
                break
            else:
                print("Invalid choice, please enter 1-6.")
    except (EOFError, KeyboardInterrupt):
        print()
    print("Exiting Inventory System. Goodbye!")


if __name__ == "__main__":
    main()