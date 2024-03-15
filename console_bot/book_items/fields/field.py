import re
from field_exceptions import FieldException
from prompt_toolkit.validation import Validator, ValidationError

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
        DateValidator().validate(value)
        super().__init__(value)


class Email(Field):
    """A class to represent an email."""
    def __init__(self, value: str) -> None:
        EmailValidator().validate(value)
        super().__init__(value)


class Name(Field):
    """A class to represent a name."""
    def __init__(self, value: str) -> None:
        super().__init__(value)


class Phone(Field):
    """A class to represent a phone number."""
    def __init__(self, value: str) -> None:
        PhoneValidator().validate(value)
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

class PhoneValidator(Validator):
    def validate(self, data):
        text = data
        if not isinstance(data, str):
            text = data.text

        if text and not text.isdigit():
            raise ValidationError(message='Phone can contain only digits')
        if len(text) < 3:
            raise ValidationError(message='Phone min len is 3')
        
class EmailValidator(Validator):
    def validate(self, data):
        text = data
        if not isinstance(data, str):
            text = data.text

        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, text) is None:
            raise ValidationError(message='Invalid email format')

class DateValidator(Validator):
    def validate(self, data):
        text = data
        if not isinstance(data, str):
            text = data.text

        pattern = r'^\d{2}\.\d{2}\.\d{4}$'
        if re.match(pattern, text) is None:
            raise ValidationError(message='Invalid date format, expected: DD.MM.YYYY')
        
        res=text.split(".")
        if int(res[0]) > 31:
            raise ValidationError(message='Day can not be greater than 31')
        if int(res[0]) == 0:
            raise ValidationError(message='Day can not be 0')
        if int(res[1]) > 12:
            raise ValidationError(message='Month can not be greater than 31')
        if int(res[1]) == 0:
            raise ValidationError(message='Month can not be 0')
        if int(res[2]) == 0:
            raise ValidationError(message='Year can not be 0')
