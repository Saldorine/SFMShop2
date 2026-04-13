class LoggableMixin:
    def log(self, message):
        print(message)


class ValidatableMixin:
    def validate(self):
        pass

    def is_valid(self):
        try:
            self.validate()
            return True
        except ValueError:
            return False


class SerializableMixin:
    def to_json(self):
        return {
            "class": self.__class__.__name__,
            "data": self.__dict__
        }