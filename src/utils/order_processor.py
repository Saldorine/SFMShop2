def load_orders_from_file(filename):
    orders = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                order = line.split(':')
                for i in range(len(order)):
                    order[i] = order[i].strip()
                orders.append(':'.join(order))
        return orders

    except FileNotFoundError:
        print(f'Файл "{filename}" не найден!')
        raise FileNotFoundError



def calculate_order_total(price, discount_rate):
    total = round(price * (1 - discount_rate), 2)
    return total


def get_discount_by_total(total):
    if total <= 0:
        return 0

    if total > 10000:
        discount_rate = 0.15
    elif total > 5000:
        discount_rate = 0.10
    else:
        discount_rate = 0.05

    return discount_rate


def process_orders(orders_data):
    result = []
    for order_data in orders_data:
        try:
            if order_data.count(':') != 3:
                raise ValueError(f'Ошибка при обработке данных: Строка "{order_data}" имеет не верный формат.')
            order_id, pre_total, status, user = order_data.split(':')

            if not pre_total.isdigit():
                raise ValueError(f'Ошибка при обработке данных: Сумма заказа "{pre_total}" не является числом.')
            pre_total = int(pre_total)
            discount_rate = get_discount_by_total(pre_total)
            total = calculate_order_total(pre_total, discount_rate)

            order = {'order_id': order_id, 'total': total, 'status': status, 'user': user}
            result.append(order)

        except ValueError as e:
            print(e)
            continue

    return result


def analyze_orders(processed_orders):
    stats = {
        'total_orders': 0,
        'total_sum': 0,
        'by_status': {},
        'unique_users': set()
    }

    for order in processed_orders:
        stats['total_orders'] += 1
        stats['total_sum'] += order['total']
        stats['by_status'][order['status']] = stats['by_status'].get(order['status'], 0) + 1
        stats['unique_users'].add(order['user'])

    stats['unique_users'] = list(stats['unique_users'])
    return stats

