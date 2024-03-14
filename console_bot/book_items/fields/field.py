import re
from field_exceptions import FieldException


class Field:
    """Base class for all fields."""
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Address(Field):
    """A class to represent an address."""
    def __init__(self, value: str) -> None:
        super().__init__(value)


class Birthday(Field):
    """A class to represent a birthday."""
    def __init__(self, value: str) -> None:
        if self._is_valid_date(value):
            super().__init__(value)
        else:
            raise FieldException("Date must be in format dd.mm.yyyy")

    def _is_valid_date(self, value) -> bool:
        """Check if the date is in the correct format."""
        pattern = r'^\d{2}\.\d{2}\.\d{4}$'
        if re.match(pattern, value):
            return True
        return False


class Email(Field):
    """A class to represent an email."""
    def __init__(self, value: str) -> None:
        if self._is_valid_email(value):
            super().__init__(value)
        else:
            raise FieldException("Invalid email format")

    def _is_valid_email(self, value) -> bool:
        """Check if the email is in the correct format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, value):
            return True
        return False


class Name(Field):
    """A class to represent a name."""
    def __init__(self, value: str) -> None:
        super().__init__(value)


class Phone(Field):
    """A class to represent a phone number."""
    def __init__(self, value: str) -> None:
        if len(value) < 10:
            raise FieldException("Phone number must be at least 10 digits.")
        for char in value:
            if char.isalpha():
                raise FieldException("Phone number must contain only digits.")
        super().__init__(value)


class Tag(Field):
    """A class to represent a tag."""
    def __init__(self, value: str) -> None:
        super().__init__(value)

    def __eq__(self, other):
        return self.value == other.value

        
class Text(Field):
    """A class to represent a text."""
    def __init__(self, value: str) -> None:
        if not self._has_valid_length(value):
            raise FieldException("Text must be between 0 and 512 characters long.")
        super().__init__(value)

    def _has_valid_length(self, value: str) -> bool:
        """Check if the text has a valid length."""
        return 0 <= len(value) < 512
