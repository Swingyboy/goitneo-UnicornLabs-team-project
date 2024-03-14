from typing import Optional
from field import Address, Birthday, Email, Name, Phone


class Record:
    """A record in the address book."""
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
        return f"Contact name: {self.name.value.capitalize()}, phone: {self.phone.value}, "

    def add_address(self, address: str) -> None:
        """Add an address to the record."""
        self.address = Address(address)

    def add_birthday(self, birthday: str) -> None:
        """Add a birthday to the record."""
        self.birthday = Birthday(birthday)

    def add_email(self, email: str) -> None:
        """Add an email to the record."""
        self.email = Email(email)

    def add_phone(self, phone) -> None:
        """Add a phone to the record."""
        self.phone = Phone(phone)

    def find_phone(self, phone: str) -> Optional[Phone]:
        """Find a phone number in the record."""
        if self.phone and self.phone.value == phone:
            return self.phone
        return None

    def to_dict(self):
        """Convert the record to a dictionary."""
        return {
            "name": self.name.value,
            "phone": self.phone.value if self.phone else None,
            "birthday": self.birthday.value if self.birthday else None,
            "email": self.email.value if self.email else None,
            "address": self.address.value if self.address else None
        }
    
    def update_address(self, new_address: str) -> None:
        """Update the address of the record."""
        if new_address:
            self.add_address(new_address)
        else:
            self.address = None

    def update_birthday(self, new_birthday: str) -> None:
        """Update the birthday of the record."""
        if new_birthday:
            self.add_birthday(new_birthday)
        else:
            self.birthday = None

    def update_email(self, new_email: str) -> None:
        """Update the email of the record."""
        if new_email:
            self.add_email(new_email)
        else:
            self.email = None

    def update_name(self, new_name: str) -> None:
        """Update the name of the record."""
        self.name = Name(new_name)

    def update_phone(self, new_phone: str) -> None:
        """Update the phone of the record."""
        self.add_phone(new_phone)

    def update_fields_from_tuple(self, *fields):
        """Update the fields of the record from a tuple."""
        if 1 < len(fields) > 4:
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
        """Create a record from a tuple."""
        record = cls(name)
        record.update_fields_from_tuple(*fields)
        if not record.phone:
            raise ValueError("Phone number is required.")
        return record

    @classmethod
    def from_dict(cls, data: dict) -> "Record":
        """Create a record from a dictionary."""
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
