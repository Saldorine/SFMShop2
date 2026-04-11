from abc import ABC, abstractmethod


class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass


class EmailNotification(Notification):
    def send(self, message: str) -> None:
        print("Email сообщение:", message)


class SMSNotification(Notification):
    def send(self, message: str) -> None:
        print("SMS сообщение:", message)


def send_notification(notification: Notification, message: str) -> None:
    notification.send(message)


send_notification(EmailNotification(), "Это сообщение было отправлено по Email.")
send_notification(SMSNotification(), "Это сообщение было отправлено по SMS.")

