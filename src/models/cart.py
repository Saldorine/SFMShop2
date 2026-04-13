from product import Product


class ShoppingCart:
    def __init__(self):
        self.items = []


    def __add__(self, product: Product):
        if not isinstance(product, Product):
            raise ValueError("Попытка добавить в корзину объект не класса Product")

        new_shopping_cart = ShoppingCart()
        new_shopping_cart.items = self.items.copy()
        new_shopping_cart.items.append(product)
        return new_shopping_cart


    def __len__(self):
        return len(self.items)


    def __iter__(self):
        return iter(self.items)


if __name__ == "__main__""":
    products = [
        Product("Ноутбук", 10000, 1),
        Product("Мышь", 5000, 1),
        Product("Холодильник", 7000, 1)
    ]

    shoppingcart = ShoppingCart()
    shoppingcart += products[0]
    shoppingcart += products[1]
    shoppingcart += products[2]

    print("Количество товаров в корзине:", len(shoppingcart))

    for product in shoppingcart:
        print(product)

