from calendar import day_name
from collections import UserDict, defaultdict
from datetime import datetime
import re
from typing import Optional, List, Dict, Union


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

    def edit_phone(self, old_p: str, new_p: str) -> None:
        for p in self.phones:
            if p.value == old_p:
                p.value = new_p

    def find_phone(self, phone: str) -> Optional[Phone]:
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def remove_phone(self, phone: str) -> None:
        self.phones = [p for p in self.phones if p.value != phone]


class AddressBook(UserDict):
    def __init__(self):
        self.data = {}
        super().__init__()

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def delete(self, name: str) -> bool:
        record = self.find(name)
        if record:
            self.data.pop(record.name.value)
            return True
        return False

    def get_all_records(self) -> List[Record]:
        return list(self.data.values())

    def get_birthdays_per_week(self) -> None:
        users_with_day_this_week = defaultdict(list)
        updated_users_list = self._get_users_birthday_in_current_year(self.data)
        for user in updated_users_list:
            if day := self._estimate_birthday_delta(user):
                if day.lower() in ["saturday", "sunday"]:
                    users_with_day_this_week["Monday"].append(user.get("name"))
                else:
                    users_with_day_this_week[day].append(user.get("name"))

        sorted_days = sorted(users_with_day_this_week.keys(), key=lambda x: list(day_name).index(x))

        for day in sorted_days:
            print(f"{day}: {', '.join(users_with_day_this_week[day])}")

    def find(self, name: str) -> Optional[Record]:
        try:
            return self.data[name]
        except KeyError:
            return None

    def _get_users_birthday_in_current_year(self, data: Dict[str, ...]) -> List[Dict[str, Union[str, datetime]]]:
        updated_users_list = []
        for user in data:
            birthday = data[user].birthday
            if not birthday:
                continue
            birthday = datetime.strptime(birthday.value, "%d.%m.%Y")
            birthday = birthday.replace(year=datetime.today().date().year).date()
            name = data[user].name.value
            updated_users_list.append({"name": name, "birthday": birthday})
        return updated_users_list


    def _estimate_birthday_delta(self, user: Dict[str, Union[str, datetime]]) -> Optional[str]:
        delta_days = abs((user.get("birthday") - datetime.today().date()).days)
        if delta_days < 7:
            return user.get("birthday").strftime("%A")


def main():
    book = AddressBook()
    record = Record("John")
    record.add_phone("0969410202")
    record.add_phone("0969410203")
    record.add_birthday("09.03.1990")
    book.add_record(record)

    record = Record("Jane")
    record.add_phone("0969410204")
    record.add_phone("0969410205")
    record.add_birthday("14.01.1991")
    book.add_record(record)
    book.get_birthdays_per_week()


if __name__ == "__main__":
    main()
