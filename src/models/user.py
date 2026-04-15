from src.models.exceptions import ValidationError
from src.models.metaclasses import ModelMeta


class User(metaclass=ModelMeta):
    def __init__(self, name, email):
        self.name = name
        self._email = self.set_email(email)



    def get_info(self):
        return f'Пользователь: {self.name}, Email: {self._email}'


    def set_email(self, email):
        if self.email_validation(email):
            return email

    @staticmethod
    def email_validation(email):
        if '@' not in email:
            raise ValidationError('Неверный формат email')
        return True

    def __str__(self):
        return self.name