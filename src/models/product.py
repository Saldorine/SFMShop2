from src.models.exceptions import NegativePriceError, NegativeQuantityError
from src.models.mixins import LoggableMixin, ValidatableMixin, SerializableMixin

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
class Product(LoggableMixin, ValidatableMixin, SerializableMixin):
    name: str
    _price: float
    _quantity: int


    def __post_init__(self):
        self.validate()
        self.log(f"Товар создан: {repr(self)}")


    def validate(self):
        if self._price < 0:
            raise NegativePriceError("Цена товара не может быть отрицательной.")
        if self._quantity < 0:
            raise NegativeQuantityError("Цена товара не может быть отрицательной.")
        return True


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
        price = self._price
        self._price = value
        self.log(f"Цена товара изменена: {price} -> {value}")


    @property
    def quantity(self):
        return self._quantity


    @quantity.setter
    def quantity(self, value):
        if value < 0:
            raise NegativeQuantityError("Количество товара не может быть отрицательным.")
        quantity = self._quantity
        self._quantity = value
        self.log(f"Количество товара изменено: {quantity} -> {value}")


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
    product.quantity = 1
    print(product.is_valid())
    print(product.to_json())

    discount_p = PercentDiscount(10)
    discount_f = FixedDiscount(500)

    print(product.calculate_price(discount_p))
    print(product.calculate_price(discount_f))