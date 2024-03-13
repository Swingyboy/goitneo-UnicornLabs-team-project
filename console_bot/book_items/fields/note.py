from typing import List
from field import Tag, Text


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
        self.tags.append(Tag(tag))

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the note."""
        self.tags.remove(Tag(tag))

    def to_dict(self) -> dict:
        """Convert the note to a dictionary."""
        return {"summary": self.summary.value,"text": self.text.value, "tags": [tag.value for tag in self.tags]}

    @classmethod
    def from_dict(cls, **kwargs) -> "Note":
        """Create a note from a dictionary."""
        return cls(kwargs["summary"], kwargs["text"], tags=kwargs["tags"] if "tags" in kwargs else None)

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
            raise ValueError("Invalid input for note")
        return cls(text, tags=tags if tags else None)
