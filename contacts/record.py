from typing import Optional
from field import Address, Birthday, Email, Name, Phone


class Record:
    def __init__(self,
                 name: str,
                 address: str = None,
                 phone: str = None,
                 birthday: str = None,
                 email: str = None
                 ) -> None:
        self.name: Name = Name(name)
        self.phone: Optional[Phone] = Phone(phone) if phone else None
        self.birthday: Optional[Birthday] = Birthday(birthday) if birthday else None
        self.email: Optional[Email] = Email(email) if email else None
        self.address: Optional[Address] = Address(address) if address else None

    def __str__(self):
        return f"Contact name: {self.name.value}, phone: {self.phone.value}, "

    def add_address(self, address: str) -> None:
        self.address = Address(address)

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def add_email(self, email: str) -> None:
        self.email = Email(email)

    def add_phone(self, phone) -> None:
        self.phone = Phone(phone)

    def update_address(self, new_address: str) -> None:
        self.add_address(new_address)

    def update_birthday(self, new_birthday: str) -> None:
        self.add_birthday(new_birthday)

    def update_email(self, new_email: str) -> None:
        self.add_email(new_email)

    def update_phone(self, new_phone: str) -> None:
        self.add_phone(new_phone)

    def find_phone(self, phone: str) -> Optional[Phone]:
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def to_dict(self):
        return {
            "name": self.name.value,
            "phone": self.phone.value if self.phone else None,
            "birthday": self.birthday.value if self.birthday else None,
            "email": self.email.value if self.email else None,
            "address": self.address.value if self.address else None
        }

    def update_fields_from_tuple(self, *fields):
        if  1 < len(fields) > 4:
            raise ValueError("Invalid number of arguments.")
        for item in fields:
            if len(item) == 10 and item.isdigit():
                self.add_phone(item)
            elif '@' in item and '.' in item:
                self.add_email(item)
            elif len(item) == 10 and item.count('.') == 2:
                self.add_birthday(item)
            else:
                self.add_address(item)

    @classmethod
    def from_tuple(cls, name: str, *fields) -> "Record":
        record = cls(name)
        record.update_fields_from_tuple(*fields)
        if not record.phone:
            raise ValueError("Phone number is required.")
        return record

    @classmethod
    def from_dict(cls, data: dict) -> "Record":
        record = cls(data.get("name"))
        if birthday := data.get("birthday"):
            record.add_birthday(birthday)
        if phone := data.get("phone"):
            record.add_phone(phone)
        else:
            raise ValueError("Phone number is required.")
        if email := data.get("email"):
            record.add_email(email)
        if address := data.get("address"):
            record.add_address(address)
        return record
