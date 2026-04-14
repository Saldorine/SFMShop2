from abc import ABC, abstractmethod


class Payment:
    def __init__(self, order_id, amount, payment_method):
        self.order_id = order_id
        self.amount = amount
        self.payment_method = payment_method
        self.status = "pending"


class PaymentMethod(ABC):
    @abstractmethod
    def process(self, amount: float) -> bool:
        """Обработка платежа"""
        pass


    @abstractmethod
    def calculate_fee(self, amount: float) -> float:
        """Расчет комиссии"""
        pass


class CardPayment(PaymentMethod):
    def calculate_fee(self, amount: float) -> float:
        """Расчет комиссии для карты"""
        if amount > 10000:
            return amount * 0.02
        return amount * 0.03


    def process(self, amount: float) -> bool:
        """Обработка платежа картой"""
        fee = self.calculate_fee(amount)
        total = amount + fee
        print(f"Зарядка карты на сумму {total}")
        return True


class PayPalPayment(PaymentMethod):
    def calculate_fee(self, amount: float) -> float:
        """Расчет комиссии для PayPal"""
        return amount * 0.035


    def process(self, amount: float) -> bool:
        """Обработка платежа через PayPal"""
        fee = self.calculate_fee(amount)
        total = amount + fee
        print(f"Зарядка PayPal на сумму {total}")
        return True


class BankTransferPayment(PaymentMethod):
    def calculate_fee(self, amount: float) -> float:
        """Расчет комиссии для банковского перевода"""
        return 50


    def process(self, amount: float) -> bool:
        """Обработка банковского перевода"""
        fee = self.calculate_fee(amount)
        total = amount + fee
        print(f"Банковский перевод на сумму {total}")
        return True