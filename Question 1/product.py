"""Entity class for a pharmacy product."""


class Product:
    def __init__(self, product_id: int, name: str, price: float, stock: int):
        if product_id <= 0:
            raise ValueError("Product ID must be a positive integer")
        if not name.strip():
            raise ValueError("Product name cannot be empty")
        if price < 0:
            raise ValueError("Price cannot be negative")
        if stock < 0:
            raise ValueError("Stock cannot be negative")
        self.product_id = product_id   # int   - unique key, cheap to hash
        self.name = name.strip()       # str   - e.g. "Paracetamol 500mg"
        self.price = price             # float - price in RM
        self.stock = stock             # int   - units on hand

    def __str__(self):
        return (f"ID: {self.product_id} | Name: {self.name} | "
                f"Price: RM{self.price:.2f} | Stock: {self.stock}")