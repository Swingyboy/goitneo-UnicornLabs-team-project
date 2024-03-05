import re


class Field:
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Birthday(Field):
    def __init__(self, value: str) -> None:
        if self._is_valid_date(value):
            super().__init__(value)
        else:
            raise ValueError("Date must be in format dd.mm.yyyy")

    def _is_valid_date(self, value) -> bool:
        pattern = r'^\d{2}\.\d{2}\.\d{4}$'
        if re.match(pattern, value):
            return True
        return False


class Name(Field):
    def __init__(self, value: str) -> None:
        super().__init__(value)


class Phone(Field):
    def __init__(self, value: str) -> None:
        for char in value:
            if char.isalpha():
                raise ValueError("Phone number must contain only digits.")
        if len(value) < 10:
            raise ValueError("Phone number must be at least 10 digits.")
        super().__init__(value)
