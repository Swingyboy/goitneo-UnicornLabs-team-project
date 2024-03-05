from typing import Optional
from field import Birthday, Name, Phone


class Record:
    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old_p: str, new_p: str) -> bool:
        if old_p not in self.phones:
            return False
        for p in self.phones:
            if p.value == old_p:
                p.value = new_p
                return True
        return False

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
