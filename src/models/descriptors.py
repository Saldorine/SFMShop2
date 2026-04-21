class PositiveNumber:
    def __init__(self, name):
        self.name = name


    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name)


    def __set__(self, instance, value):
        if value < 0:
            raise ValueError(f"{self.name} не может быть отрицательным")
        setattr(instance, self.name, value)


class EmailDescriptor:
    def __init__(self, name):
        self.name = name


    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name)


    def __set__(self, instance, value):
        if "@" not in value:
            raise ValueError("Email должен содержать @")
        setattr(instance, self.name, value)


class AgeDescriptor:
    def __init__(self, name):
        self.name = name


    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name)


    def __set__(self, instance, value):
        if value < 18:
            raise ValueError("Пользователь должен быть старше 18 лет")
        setattr(instance, self.name, value)


class ValueFilled:
    def __init__(self, name):
        self.name = name


    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name)


    def __set__(self, instance, value):
        if not value:
            raise ValueError(f"{self.name} не может быть пустым")
        setattr(instance, self.name, value)


class CachedProperty:
    def __init__(self, func):
        self.func = func
        self.name = func.__name__

    def __get__(self, instance, owner):
        if instance is None:
            return self

        cache_attr = f"_cached_{self.name}"
        if hasattr(instance, cache_attr):
            print("КЭШ")
            return getattr(instance, cache_attr)

        value = self.func(instance)
        print("Расчет")
        setattr(instance, cache_attr, value)
        return value


