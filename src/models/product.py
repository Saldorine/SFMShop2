from src.models.exceptions import NegativePriceError, NegativeQuantityError
from dataclasses import dataclass


@dataclass
class Product:
    name: str
    _price: float
    _quantity: int


    def __post_init__(self):
        if self._price < 0:
            raise NegativePriceError("Цена товара не может быть отрицательной.")
        if self._quantity < 0:
            raise NegativeQuantityError("Цена товара не может быть отрицательной.")


    @classmethod
    def from_dict(cls, d):
        name = d["name"]
        price = d["price"]
        quantity = d["quantity"]
        return cls(name, price, quantity)


    @property
    def price(self):
        return self._price


    @price.setter
    def price(self, value):
        if value < 0:
            raise NegativePriceError("Цена товара не может быть отрицательной.")
        self._price = value


    @property
    def quantity(self):
        return self._quantity


    @quantity.setter
    def quantity(self, value):
        if value < 0:
            raise NegativeQuantityError("Количество товара не может быть отрицательным.")
        self._quantity = value

    def get_total_price(self):
        return self.price * self.quantity


    @staticmethod
    def calculate_discount(price, discount):
        return price - price * discount / 100


    def __str__(self):
        return f'Товар: {self.name}, Цена: {self.price} руб., Количество: {self.quantity}'


    def __lt__(self, other):
        return self.price < other.price

