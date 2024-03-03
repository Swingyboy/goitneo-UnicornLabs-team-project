from collections import UserDict
from typing import Optional, NoReturn


class Field:
    def __init__(self, value: str) -> NoReturn:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    def __init__(self, value: str) -> NoReturn:
        super().__init__(value)


class Phone(Field):
    def __init__(self, value: str) -> NoReturn:
        for char in value:
            if char.isalpha():
                raise ValueError("Phone number must contain only digits.")
        if len(value) < 10:
            raise ValueError("Phone number must be at least 10 digits.")
        super().__init__(value)


class Record:
    def __init__(self, name: str) -> NoReturn:
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old_p: str, new_p: str) -> NoReturn:
        for p in self.phones:
            if p.value == old_p:
                p.value = new_p

    def find_phone(self, phone: str) -> Optional[Phone]:
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def remove_phone(self, phone: str) -> NoReturn:
        self.phones = [p for p in self.phones if p.value != phone]


class AddressBook(UserDict):
    def __init__(self):
        self.data = {}
        super().__init__()

    def add_record(self, record: Record) -> NoReturn:
        self.data[record.name.value] = record

    def delete(self, name: str) -> NoReturn:
        try:
            del self.data[name]
        except KeyError:
            print(f"Contact {name} not found.")

    def find(self, name: str) -> Optional[Record]:
        try:
            return self.data[name]
        except KeyError:
            print(f"Contact {name} not found.")
