from typing import Optional
from field import Address, Birthday, Email, Name, Phone


class Record:
    def __init__(self,
                 name: str,
                 address: str = None,
                 phones: list = None,
                 birthday: str = None,
                 email: str = None
                 ) -> None:
        self.name: Name = Name(name)
        self.phones: list = [Phone(p) for p in phones] if phones else []
        self.birthday: Optional[Birthday] = Birthday(birthday) if birthday else None
        self.email: Optional[Email] = Email(email) if email else None
        self.address: Optional[Address] = Address(address) if address else None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_address(self, address: str) -> None:
        self.address = Address(address)

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def add_email(self, email: str) -> None:
        self.email = Email(email)

    def add_phone(self, phone) -> None:
        self.phones.append(Phone(phone))

    def add_phones(self, phones: list) -> None:
        for phone in phones:
            self.add_phone(phone)

    def edit_phone(self, old_p: str, new_p: str) -> bool:
        if old_p not in self.phones:
            return False
        for p in self.phones:
            if p.value == old_p:
                p.value = new_p
                return True
        return False

    def update_address(self, new_address: str) -> None:
        self.address = Address(new_address)

    def update_birthday(self, new_birthday: str) -> None:
        self.birthday = Birthday(new_birthday)

    def update_email(self, new_email: str) -> None:
        self.email = Email(new_email)

    def update_phones(self, new_p: list) -> bool:
        for p in new_p:
            if p not in [phone.value for phone in self.phones]:
                self.phones.append(Phone(p))
        return True

    def find_phone(self, phone: str) -> Optional[Phone]:
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def to_dict(self):
        return {
            "name": self.name.value,
            "phones": [p.value for p in self.phones],
            "birthday": self.birthday.value if self.birthday else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Record":
        record = cls(data.get("name"))
        if birthday := data.get("birthday"):
            record.add_birthday(birthday)
        for phone in data.get("phones"):
            record.add_phone(phone)
        return record

    def remove_phone(self, phone: str) -> None:
        self.phones = [p for p in self.phones if p.value != phone]
