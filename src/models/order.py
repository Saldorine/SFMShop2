from src.models.exceptions import InvalidOrderError, DataTypeError


class Order:
    def __init__(self, user, products):
        if not products:
            raise InvalidOrderError("Заказ невалиден: пустой список товаров")

        self.user = user
        self.products = []
        for product in products:
            self.add_product(product)

        self.total = self.calculate_total()




    def calculate_total(self):
        total = 0
        for product in self.products:
            total += product.get_total_price()

        return total


    def add_product(self, product):
        if product.__class__.__name__ != 'Product':
            raise DataTypeError('Переданный объект не является экземляром класса Product')
        self.products.append(product)

    def __str__(self):
        return f'Заказ пользователя {self.user} на сумму {self.total} руб.'