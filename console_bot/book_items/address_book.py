from calendar import day_name
from collections import UserDict, defaultdict
from datetime import datetime
from typing import Any, Optional, List, Dict, Union

from fields.record import Record


class AddressBook(UserDict):
    """A class to represent an address book."""
    def __init__(self):
        self.data = {}
        super().__init__()

    def add_record(self, record: Record) -> None:
        """Add a record to the address book."""
        self.data[record.name.value] = record

    def delete_record(self, name: str) -> bool:
        """Delete a record from the address book."""
        record = self.find(name)
        if record:
            self.data.pop(record.name.value)
            return True
        return False

    def get_all_records(self) -> List[Record]:
        """Return all records in the address book."""
        return list(self.data.values())

    def to_dict(self) -> List[Dict[str, str]]:
        """Convert the address book to a dictionary."""
        res = []
        for record in self.data.values():
            res.append(record.to_dict())
        return res

    @classmethod
    def from_dict(cls, data: List[Dict[str, str]]) -> "AddressBook":
        """Create an address book from a dictionary."""
        address_book = cls()
        for record in data:
            new_record = Record.from_dict(record)
            address_book.add_record(new_record)
        return address_book

    def get_birthdays_per_week(self, num_of_days: int = 7) -> Optional[Dict[str, str]]:
        """Print the birthdays for the next `num_of_days` days."""
        users_with_day_this_week = defaultdict(list)
        updated_users_list = self._get_users_birthday_in_current_year(self.data)
        for user in updated_users_list:
            if day := self._estimate_birthday_delta(user, num_of_days):
                if day.lower() in ["saturday", "sunday"]:
                    users_with_day_this_week["Monday"].append(user.get("name").capitalize())
                else:
                    users_with_day_this_week[day].append(user.get("name").capitalize())

        sorted_days = sorted(users_with_day_this_week.keys(), key=lambda x: list(day_name).index(x))

        if not sorted_days:
            print("No birthdays this week.")
            return


        return {day: ', '.join(users_with_day_this_week[day]) for day in sorted_days}

    def find(self, name: str) -> Optional[Record]:
        """Find a record in the address book."""
        try:
            return self.data[name]
        except KeyError:
            return None

    def search(self, by_field: str, value: str) -> List[Record]:
        """Search for a record in the address book."""
        return [record for record in self.data.values() if value.lower() in getattr(record, by_field).value.lower()]

    def _get_users_birthday_in_current_year(self, data: Dict[str, Any]) -> List[Dict[str, Union[str, datetime]]]:
        """Return the list of users with their birthday in the current year."""
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

    def _estimate_birthday_delta(self, user: Dict[str, Union[str, datetime]], from_days: int) -> Optional[str]:
        """Estimate the birthday delta."""
        delta_days = abs((user.get("birthday") - datetime.today().date()).days)
        if delta_days < from_days:
            return user.get("birthday").strftime("%A")
