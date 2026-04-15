from src.models.exceptions import NegativePriceError, NegativeQuantityError
from src.models.mixins import LoggableMixin, ValidatableMixin, SerializableMixin
from src.models.metaclasses import ModelMeta
from src.models.descriptors import PositiveNumber, CachedProperty

from dataclasses import dataclass
from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, price: float) -> float:
        pass


class PercentDiscount(DiscountStrategy):
    def __init__(self, percent: float):
        self.percent = percent


    def apply(self, price: float) -> float:
        return price * (1 - self.percent / 100)


class FixedDiscount(DiscountStrategy):
    def __init__(self, amount: float):
        self.amount = amount


    def apply(self, price: float) -> float:
        return price - self.amount


@dataclass
class Product(LoggableMixin, SerializableMixin, metaclass=ModelMeta):
    price = PositiveNumber("_price")
    quantity = PositiveNumber("_quantity")

    def __init__(self, name: str, price: float, quantity: float):
        self.name = name
        self.price = price
        self.quantity = quantity


    def __post_init__(self):
        self.log(f"Товар создан: {repr(self)}")


    @classmethod
    def from_dict(cls, d):
        name = d["name"]
        price = d["price"]
        quantity = d["quantity"]
        return cls(name, price, quantity)


    @CachedProperty
    def get_total_price(self):
        return self.price * self.quantity


    def calculate_price(self, discount: DiscountStrategy):
        return discount.apply(self.price)


    def __str__(self):
        return f'Товар: {self.name}, Цена: {self.price} руб., Количество: {self.quantity}'


    def __lt__(self, other):
        return self.price < other.price


if __name__ == '__main__':
    product = Product('Ноутбук', 10000.00, 1)
    product.price = 15000.00
    product.quantity = 3


    print(product.get_total_price)
    print(product.get_total_price)