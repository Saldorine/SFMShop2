from src.models.exceptions import NegativePriceError, NegativeQuantityError
from src.models.mixins import LoggableMixin, ValidatableMixin, SerializableMixin
from src.models.metaclasses import ModelMeta
from src.models.descriptors import PositiveNumber, CachedProperty
from src.models.discount import DiscountStrategy, PercentDiscount
from dataclasses import dataclass


@dataclass
class Product(ValidatableMixin, LoggableMixin, SerializableMixin, metaclass=ModelMeta):
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


    def __str__(self):
        return f'Товар: {self.name}, Цена: {self.price} руб., Количество: {self.quantity}'


    def __lt__(self, other):
        return self.price < other.price


class ProductValidator:
    @staticmethod
    def validate(product: Product):
        if product.price < 0:
            raise NegativePriceError("Цена товара должна быть положительной.")
        if product.quantity < 0:
            raise NegativeQuantityError("Количество товара должно быть положительным.")
        return True


class ProductCalculator:
    @staticmethod
    def calculate_price(product: Product, discount: DiscountStrategy):
        return discount.apply(product.price)

    @staticmethod
    def get_total_price(product: Product):
        return product.price * product.quantity

if __name__ == '__main__':
    product = Product('Ноутбук', 10000.00, 1)
    product.price = 15000.00
    product.quantity = 3


    print(ProductValidator.validate(product))
    print(ProductCalculator.calculate_price(product, PercentDiscount(10)))
    print(ProductCalculator.get_total_price(product, ))