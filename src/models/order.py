from src.models.exceptions import InvalidOrderError, DataTypeError
from src.models.mixins import LoggableMixin, ValidatableMixin, SerializableMixin
from src.models.product import Product, ProductCalculator
from src.models.user import User
from src.models.metaclasses import ModelMeta
from src.models.notifications import EmailNotification
from src.models.discount import DiscountStrategy, FixedDiscount, PercentDiscount
from src.models.descriptors import ValueFilled, PositiveNumber

from abc import ABC, abstractmethod





class Order(LoggableMixin, SerializableMixin, metaclass=ModelMeta):
    product = ValueFilled('_product')
    total = PositiveNumber('_total')

    def __init__(self, user, products):
        self.user = user
        self.products = products.copy()
        self.total = OrderCalculator.calculate_total(self)
        self.log(f"Заказ создан: {repr(self)}")


    def add_product(self, product):
        if product.__class__.__name__ != 'Product':
            raise DataTypeError("Переданный объект не является экземпляром класса Product")
        self.products.append(product)
        self.total = OrderCalculator.calculate_total(self)
        self.log(f"В заказ добавлен новый товар: {product}")


    def __str__(self):
        return f"Заказ пользователя {self.user} на сумму {self.total} руб."


    def __repr__(self):
        return f"Заказ пользователя {self.user}."


class OrderCalculator:
    @staticmethod
    def calculate_total(order: Order):
        total = 0
        for product in order.products:
            total += ProductCalculator.get_total_price(product)
        return total


class OrderValidator:
    @staticmethod
    def validate(order: Order):
        if not order.products:
            raise InvalidOrderError("Заказ невалиден: пустой список товаров")
        if order.total < 0:
            raise ValueError("Сумма заказа не может быть отрицательной")
        if not isinstance(order.user, User):
            raise InvalidOrderError("Заказ невалиден: пользователь должен быть экземпляром класса User")
        return True


class OrderService:
    @staticmethod
    def processing():
        """Обработка заказа"""
        pass


class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order):
        pass


class OrderSQLPaymentRepository(OrderRepository):
    def save(self, order: Order):
        print(f"Сохранение заказа {order.user} в PostgreSQL")


if __name__ == "__main__":
    product = Product("Ноутбук", 30000, 1)
    order = Order(User(1,"Ваня", "vania@", 18, 10000), [product])
    new_product = Product("Холодильник", 70000, 1)
    order.add_product(new_product)
    OrderValidator.validate(order)
    total = OrderCalculator.calculate_total(order)
    mess = EmailNotification()
    mess.send(order)

    print(total)
    d = FixedDiscount(100)
    print(d.apply(total))