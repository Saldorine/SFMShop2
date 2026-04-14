from src.models.exceptions import InvalidOrderError, DataTypeError
from src.models.mixins import LoggableMixin, ValidatableMixin, SerializableMixin
from src.models.product import Product
from src.models.user import User


class Order(LoggableMixin, ValidatableMixin, SerializableMixin):
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
            total += product.get_total_price()
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


if __name__ == "__main__":
    product = Product("Ноутбук", 30000, 1)
    order = Order(User("Ваня", "vania@"), [product])
    new_product = Product("Холодильник", 70000, 1)
    order.add_product(new_product)
    OrderValidator.validate(order)
    total = OrderCalculator.calculate_total(order)

    print(total)