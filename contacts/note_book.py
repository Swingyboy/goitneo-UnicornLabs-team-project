from collections import UserList
from typing import List
from note import Note


class NoteBook(UserList):
    def __init__(self) -> None:
        self.data = []
        super().__init__()

    def change_text(self, new_text: str, idx: int = None) -> None:
        if not idx:
            idx = len(self.data) - 1
        self.data[idx].text.value = new_text

    def delete_note(self, idx: int = None) -> None:
        if not idx:
            idx = len(self.data) - 1
        self.data.pop(idx)

    def delete_by_tag(self, tag: str) -> None:
        self.data = [note for note in self.data if tag not in note.tags]

    def new_note(self, *data) -> None:
        self.data.append(Note.from_tuple(*data))

    def search(self, by: str, query: str) -> List[Note]:
        if by == "tag":
            return self.search_by_tag(query)
        elif by == "text":
            return self.search_note(query)

    def search_note(self, query: str) -> list:
        return [note for note in self.data if query in note.text.value]

    def search_by_tag(self, tag: str) -> list:
        return [note for note in self.data if tag in [t.value for t in note.tags]]

    def to_dict(self) -> List[dict]:
        return [note.to_dict() for note in self.data]

    @classmethod
    def from_dict(cls, data: List[dict]) -> "NoteBook":
        note_book = cls()
        for note in data:
            new_note = Note.from_dict(note)
            note_book.data.append(new_note)
        return note_book
