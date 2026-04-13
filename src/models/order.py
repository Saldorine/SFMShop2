from src.models.exceptions import InvalidOrderError, DataTypeError
from src.models.mixins import LoggableMixin, ValidatableMixin, SerializableMixin
from src.models.product import Product


class Order(LoggableMixin, ValidatableMixin, SerializableMixin):
    def __init__(self, user, products):
        if not products:
            raise InvalidOrderError("Заказ невалиден: пустой список товаров")

        self.user = user
        self.products = []
        for product in products:
            self.add_product(product)

        self.total = self.calculate_total()
        self.log(f"Заказ создан: {repr(self)}")


    def validate(self):
        if self.total < 0:
            raise ValueError("Сумма заказа не может быть отрицательной")
        return True


    def calculate_total(self):
        total = 0
        for product in self.products:
            total += product.get_total_price()

        return total


    def add_product(self, product):
        if product.__class__.__name__ != 'Product':
            raise DataTypeError("Переданный объект не является экземпляром класса Product")
        self.products.append(product)
        self.total = self.calculate_total()
        self.log(f"В заказ добавлен новый товар: {product}")


    def __str__(self):
        return f"Заказ пользователя {self.user} на сумму {self.total} руб."


    def __repr__(self):
        return f"Заказ пользователя {self.user}."


if __name__ == "__main__":
    product = Product("Ноутбук", 30000, 1)
    order = Order("Ваня", [product])
    new_product = Product("Холодильник", 70000, 1)
    order.add_product(new_product)
    print(order.is_valid())
    print(order.to_json())