from src.models.product import Product
from datetime import datetime
import random
import time


'''Функции измерения производительности'''


def benchmark_optimizations(list_funcs: list[tuple[list]]):
    results = {}

    for funcs in list_funcs:
        before_func, *before_args = funcs[0]
        after_func, *after_args = funcs[1]

        # До оптимизации
        start_time = time.time()
        result_before = before_func(*before_args)
        time_before = time.time() - start_time

        # После оптимизации
        start_time = time.time()
        result_after = after_func(*after_args)
        time_after = time.time() - start_time

        results[before_func.__name__] = {
            "time_before": time_before,
            "time_after": time_after,
            "speedup": time_before / time_after if time_after > 0 else 0
        }

        print("Результаты оптимизации:")
        for func_name, metrics in results.items():
            print(f"{func_name}:")
            print(f"  До: {metrics['time_before']:.6f} сек")
            print(f"  После: {metrics['time_after']:.6f} сек")
            print(f"  Ускорение: {metrics['speedup']:.2f}x")

        return results


'''Заменить линейный поиск в списках на поиск в словарях'''

products = []
for i in range(1000):
    product = Product(f"Product {i}", random.randint(1, 10000), i)
    product.id = i
    products.append(product)


# До оптимизации (O(n))
def find_product_list(products: list[Product], product_id: int):
    """Поиск по id товара в списке"""

    for product in products:
        if product.id == product_id:
            return product
    return None


# После оптимизации (O(1))
def create_products_catalog(products: list[Product]):
    return {product.id: product for product in products}


def find_product_dict(products_index: dict, product_id: int):
    """Поиск по id товара в словаре"""

    return products_index.get(product_id)

#Замер производительности
products_index = create_products_catalog(products)
product_id = 777
result = benchmark_optimizations(
    [(
        [find_product_list, products, product_id],
        [find_product_dict, products_index, product_id])
    ])
print()


'''Использовать sort'''

def bubble_sort(products: list[Product]):
    n = len(products)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if products[j].price > products[j + 1].price:
                products[j], products[j + 1] = products[j + 1], products[j]
                swapped = True
        if not swapped:
            break
    return products


#Эффективная сортировка
def efficient_sort(products: list[Product]):
    return sorted(products, key=lambda product: product.price)




result = benchmark_optimizations(
    [(
        [bubble_sort, products.copy()],
        [efficient_sort, products])
    ])