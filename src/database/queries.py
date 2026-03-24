import psycopg2
from psycopg2 import Error


def get_user_order_history(conn, user_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT orders.id, products.name, order_items.quantity, order_items.price
                 FROM orders
                 INNER JOIN order_items ON order_items.order_id = orders.id
                 INNER JOIN products ON products.id = order_items.product_id
                 WHERE orders.user_id = %s
                 ORDER BY orders.created_at DESC""", (user_id,))
            result = cursor.fetchall()
        return result
    except Error as e:
        print("Ошибка при получении заказа:", e)
        return []


def get_order_statistics(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT user_id, users.name, COUNT(*), SUM(orders.total)
                FROM orders
                LEFT JOIN users ON users.id = user_id
                GROUP BY orders.user_id, users.name
                """
            )
            result = cursor.fetchall()
        return result
    except Error as e:
        print("Ошибка при формировании статистики по заказам:", e)
        return []


def get_top_products(conn, limit=5):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT order_items.product_id, products.name, SUM(order_items.quantity) as total_quantity
            FROM order_items
            LEFT JOIN products ON order_items.product_id = products.id
            GROUP BY order_items.product_id, products.name
            ORDER BY total_quantity DESC
            LIMIT %s""", (limit,))
            result = cursor.fetchall()
        return result
    except Error as e:
        print("Ошибка при получении ТОПа - товаров:", e)
        return []



