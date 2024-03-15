from typing import List
from field import Tag, Text
from field_exceptions import NoteException


class Note:
    """A note with a message and tags."""
    _index = 0

    def __init__(self, summary: str, text: str, tags: List[str] = None) -> None:
        """Initialize the note with a message and tags."""
        self.summary = Text(summary)
        self.text = Text(text)
        self.tags = [Tag(tag) for tag in tags] if tags else []
        Note._index += 1
        self.index = Note._index

    def __del__(self):
        Note._index -= 1

    def add_tag(self, tag: str) -> None:
        """Add a tag to the note."""
        try:
            self.tags.append(Tag(tag))
        except ValueError:
            raise NoteException(f"Invalid tag: {tag}")
        except MemoryError:
            raise MemoryError(f"Memory is full. The tag {tag} cannot be created.")

    def add_tags(self, *tags) -> None:
        """Add tags to the note."""
        try:
            self.tags.extend([Tag(tag) for tag in tags])
        except ValueError:
            raise NoteException(f"Invalid tags: {tags}")
        except MemoryError:
            raise MemoryError(f"Memory is full. The tags {tags} cannot be created.")

    def add_text(self, text: str) -> None:
        """Add text to the note."""
        self.text = Text(text)

    def add_summary(self, summary: str) -> None:
        """Add a summary to the note."""
        self.summary = Text(summary)

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the note."""
        self.tags.remove(Tag(tag))

    def to_dict(self) -> dict:
        """Convert the note to a dictionary."""
        try:
            return {"summary": self.summary.value,"text": self.text.value, "tags": [tag.value for tag in self.tags]}
        except AttributeError as ex:
            raise NoteException(f"Invalid note: {ex}")
    
    def update_summary(self, summary: str) -> None:
        """Update the summary of the note."""
        self.add_summary(summary)

    def update_text(self, text: str) -> None:
        """Update the text of the note."""
        if text:
            self.add_text(text)
        else:
            self.text = None

    def update_tags(self, tags: str) -> None:
        """Update the tags of the note."""
        if tags:
            tags = tags.split(",")
            self.tags = [Tag(tag.strip()) for tag in tags]
        else:
            self.tags = []

    @classmethod
    def from_dict(cls, **kwargs) -> "Note":
        """Create a note from a dictionary."""
        try:
            return cls(kwargs["summary"], kwargs["text"], tags=kwargs["tags"] if "tags" in kwargs else None)
        except KeyError as ex:
            raise NoteException(f"Missing required field: {ex}")

    @classmethod
    def from_tuple(cls, *data) -> "Note":
        """Create a note from a tuple."""
        tags: List[str] = []
        if len(data) >= 1:
            # Extracting the message
            if data[0].startswith('"') and data[0].endswith('"'):
                text = data[0][1:-1]  # Remove the leading and trailing quotes
            else:
                for item in data:
                    if item.startswith('"'):
                        text = item[1:]
                    elif item.endswith('"'):
                        text = f"{text} {item[:-1]}"
                        break
                    else:
                        text = f"{text} {item}"

            # Extracting the tags if present
            if len(data) > 1 and 'tags' in data:
                tags_start_index = data.index('tags') + 1
                tags = list(data[tags_start_index:])
        else:
            raise NoteException("Invalid input for note")
        return cls(text, tags=tags if tags else None)
