import re


class Field:
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Address(Field):
    def __init__(self, value: str) -> None:
        super().__init__(value)


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


class Email(Field):
    def __init__(self, value: str) -> None:
        if self._is_valid_email(value):
            super().__init__(value)
        else:
            raise ValueError("Invalid email format")

    def _is_valid_email(self, value) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
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


class Tag(Field):
    def __init__(self, value: str) -> None:
        super().__init__(value)

    def __eq__(self, other):
        return self.value == other.value

        
class Text(Field):
    def __init__(self, value: str) -> None:
        if not self._has_valid_length(value):
            raise ValueError("Text must be between 1 and 512 characters long.")
        super().__init__(value)

    def _has_valid_length(self, value: str) -> bool:
        return 0 < len(value) < 512
