import psycopg2
from psycopg2 import Error

from src.models.exceptions import InvalidOrderError
from src.models.product import Product
from src.models.order import Order
from fastapi import HTTPException

from src.models.user import User


def connect_to_db():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="sfmshop",
            user="postgres",
            password="12345678"
            )
        return conn
    except Error as e:
        print("Ошибка при подключении к базе данных:", e)
        return None


def add_product(conn, name, price, quantity):
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)", (name, price, quantity))
            conn.commit()
    except Error  as e:
        print("Ошибка при добавлении товара:", e)


def get_all_products(conn, limit=10, offset=0):
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, name, price, quantity FROM products LIMIT %s OFFSET %s", (limit, offset))
        products = []
        for db_product in cursor.fetchall():
            product = Product(*db_product[1:])
            product.id = db_product[0]
            products.append(product.__dict__)
    return products



def get_product_by_id(conn, id):
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, name, price, quantity FROM products WHERE id = %s", (id,))
        result = cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail=f"Товар с id={id} не найден")
        product = Product(*result[1:])
        product.id = result[0]
    return product



def update_product_price(conn, product_id, new_price):
    with conn.cursor() as cursor:
        cursor.execute("UPDATE products SET price=%s WHERE id=%s", (new_price, product_id))
        conn.commit()



def update_product(conn, product_id, new_name, new_price):
    with conn.cursor() as cursor:
        cursor.execute("UPDATE products SET name=%s, price=%s WHERE id=%s RETURNING id", (new_name, new_price, product_id))
        product = get_product_by_id(conn, cursor.fetchone()[0])
        conn.commit()
        return product


def delete_product(conn, product_id):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
        conn.commit()


def get_all_users(conn, limit=10, offset=0):
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, name, email FROM users LIMIT %s OFFSET %s", (limit, offset))
        users = []
        for db_user in cursor.fetchall():
            user = User(*db_user[1:])
            user.id = db_user[0]
            users.append(user.__dict__)
        return users


def get_user_by_id(conn, user_id):
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, name, email FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail=f"Пользователь с id={user_id} не найден")
        user = User(*result[1:])
        user.id = result[0]
    return user


def create_user(conn, name, email):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id", (name, email))
        conn.commit()
        return cursor.fetchone()[0]


def create_order(conn, user_id, products):
    db_products = []
    for product in products:
        db_product = get_product_by_id(conn, product[0])
        if db_product is None:
            raise HTTPException(status_code=404, detail=f'Товар с id={product[0]} не найден.')
        db_product.quantity = product[1]
        db_products.append(db_product)
    order = Order(user_id, db_products)
    total = order.calculate_total()

    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO orders (user_id, total) VALUES (%s, %s) RETURNING id", (user_id, total))
        order_id = cursor.fetchone()[0]
        for product in db_products:
            cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                           (order_id, product.id, product.quantity, product.price))
        conn.commit()
    conn.close()

    return order



def get_user_orders(conn, user_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM orders WHERE user_id=%s", (user_id, ))
            result = cursor.fetchall()
        return result
    except Error as e:
        print("Ошибка при получении заказа пользователя:", e)
        return []


def delete_order(conn, order_id):
    try:
        with conn.cursor() as cursor:
            deleted_rows = 0
            cursor.execute("DELETE FROM order_items WHERE order_id=%s", (order_id, ))
            deleted_rows += cursor.rowcount
            cursor.execute("DELETE FROM orders WHERE id=%s", (order_id, ))
            deleted_rows += cursor.rowcount

            conn.commit()
        return deleted_rows
    except Error as e:
        print("Ошибка при попытке удалить заказ:", e)
        return None


if __name__ == '__main__':
    conn = connect_to_db()
    print(get_all_products(conn))