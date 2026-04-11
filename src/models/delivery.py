from abc import ABC, abstractmethod


class Delivery(ABC):
    @abstractmethod
    def calculate_cost(self, distance: float) -> float:
        pass


class StandardDelivery(Delivery):
    def calculate_cost(self, distance: float) -> float:
        price = distance * 10
        return price


class ExpressDelivery(Delivery):
    def calculate_cost(self, distance: float) -> float:
        price = distance * 20
        return price


def calculate_cost(delivery: Delivery, distance: float) -> None:
    print("Цена доставки:", delivery.calculate_cost(distance))


calculate_cost(StandardDelivery(), 10)
calculate_cost(ExpressDelivery(), 10)