from calendar import day_name
from collections import UserDict, defaultdict
from datetime import datetime
from typing import Optional, List, Dict, Union

from record import Record


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
                    users_with_day_this_week["Monday"].append(user.get("name").capitalize())
                else:
                    users_with_day_this_week[day].append(user.get("name").capitalize())

        sorted_days = sorted(users_with_day_this_week.keys(), key=lambda x: list(day_name).index(x))

        if not sorted_days:
            print("No birthdays this week.")
            return

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
