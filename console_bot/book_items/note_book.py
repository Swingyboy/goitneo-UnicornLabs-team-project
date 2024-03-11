from abc import ABC, abstractmethod
from collections import UserList
from typing import List
from fields import Note, Tag


class SortStrategy(ABC):
    """A class to represent a sort strategy."""
    @abstractmethod
    def sort(self, data):
        ...


class IndexSortStrategy(SortStrategy):
    """A class to represent a sort strategy by index."""
    def sort(self, data):
        return sorted(data, key=lambda note: note.index)


class TextSortStrategy(SortStrategy):
    """A class to represent a sort strategy by text."""
    def sort(self, data):
        return sorted(data, key=lambda note: note.text.value)


class TagSortStrategy(SortStrategy):
    """A class to represent a sort strategy by tag."""
    def sort(self, data):
        data_to_sort = [note for note in data if note.tags]
        data_not_to_sort = [note for note in data if not note.tags]
        try:
            sorted_data = sorted(data_to_sort, key=lambda note: note.tags[0].value)
            return sorted_data + data_not_to_sort
        except IndexError:
            return data


class NoteSorter:
    """A class to represent a note sorter."""
    def __init__(self, strategy: SortStrategy) -> None:
        self.strategy = strategy

    def sort(self, data, order="asc"):
        """Sort the notes."""
        sorted_data = self.strategy.sort(data)
        if order == "desc" and (isinstance(self.strategy, IndexSortStrategy) or isinstance(self.strategy, TextSortStrategy)):
            sorted_data.reverse()
        elif order == "desc" and isinstance(self.strategy, TagSortStrategy):
            sorted_data = sorted_data[::-1]
        return sorted_data


class NoteBook(UserList):
    """A class to represent a notebook."""
    def __init__(self) -> None:
        self.data = []
        super().__init__()

    def _sort(self, by: str, order: str = "asc") -> None:
        """Sort the notes."""
        if by == "index":
            strategy = IndexSortStrategy()
        elif by == "text":
            strategy = TextSortStrategy()
        elif by == "tag":
            strategy = TagSortStrategy()
        else:
            raise ValueError(f"Invalid sort attribute: {by}")

        sorter = NoteSorter(strategy)
        self.data = sorter.sort(self.data, order)

    def add_tags_to_note(self, index, *tags) -> str:
        """Add tags to a note."""
        try:
            self.data[index].tags.extend([Tag(tag) for tag in tags])
            return f"Tags added: {', '.join(tags)} to note with index: {index}"
        except IndexError:
            return f"Invalid note index: {index}"

    def change_text(self, new_text: str, idx: int = None) -> None:
        """Change the text of a note."""
        if not idx:
            idx = len(self.data) - 1
        self.data[idx].text.value = new_text

    def delete_note(self, idx: int = None) -> None:
        """Delete a note."""
        if not idx:
            idx = len(self.data) - 1
        self.data.pop(idx)

    def delete_tags_from_note(self, index, *tags) -> str:
        """Delete tags from a note."""
        try:
            for tag in tags:
                self.data[index].tags.remove(Tag(tag))
            return f"Tags removed: {', '.join(tags)} from note with index: {index}"
        except IndexError:
            return f"Invalid note index: {index}"

    def delete_by_tag(self, tag: str) -> None:
        """Delete notes by tag."""
        self.data = [note for note in self.data if tag not in note.tags]

    def new_note(self, *data) -> None:
        """Add a new note."""
        self.data.append(Note.from_tuple(*data))

    def search(self, by: str, query: str, sorted_by: str, order: str) -> List[Note]:
        """Search for a note."""
        if sorted_by and order:
            self._sort(sorted_by, order)
        if by == "tag":
            return self.search_by_tag(query)
        elif by == "text":
            return self.search_note(query)

    def search_note(self, query: str) -> list:
        """Search for a note by text."""
        return [note for note in self.data if query in note.text.value]

    def search_by_tag(self, tag: str) -> list:
        """Search for a note by tag."""
        return [note for note in self.data if tag in [t.value for t in note.tags]]

    def to_dict(self) -> List[dict]:
        """Convert the notebook to a dictionary."""
        return [note.to_dict() for note in self.data]

    @classmethod
    def from_dict(cls, data: List[dict]) -> "NoteBook":
        """Create a notebook from a dictionary."""
        note_book = cls()
        for note in data:
            new_note = Note.from_dict(note)
            note_book.data.append(new_note)
        return note_book
