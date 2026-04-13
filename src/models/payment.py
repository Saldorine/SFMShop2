class Payment:
    def __init__(self, amount):
        self.amount = amount


    def process_payment(self):
        raise NotImplementedError("Метод долен быть переопределен.")


class Loggable():
    def log(self):
        print("Loggable.log()")


class CardPayment(Payment, Loggable):
    def __init__(self, amount, card_number):
        super().__init__(amount)
        self.__card_number = card_number


    def process_payment(self):
        self.log()
        return f'Оплата картой **** {self.__card_number[-4:]}: {self.amount} руб.'


class PayPalPayment(Payment, Loggable):
    def __init__(self, amount, email):
        super().__init__(amount)
        self._email = email


    def get_email(self):
        return self._email


    def process_payment(self):
        self.log()
        return f'Оплата PayPal ({self._email}): {self.amount} руб.'