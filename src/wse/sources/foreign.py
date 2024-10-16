"""Foreign data source implementation."""

from toga.sources import Source


class Word:
    """A class to wrap individual word."""

    def __init__(self, id: str, foreign_word: str, russian_word: str) -> None:
        """Construct the wrap."""
        self.id = int(id)
        self.foreign_word = foreign_word
        self.russian_word = russian_word


class WordSource(Source):
    """Word entries source."""

    def __init__(self) -> None:
        """Construct the source."""
        super().__init__()
        self._words = []
        self.accessors = ['id', 'foreign_word', 'russian_word']

    def __len__(self) -> int:
        """Get len items."""
        return len(self._words)

    def __getitem__(self, index: int) -> str:
        """Get entry value."""
        return self._words[index]

    def index(self, entry: str) -> int:
        """Get entry index."""
        return self._words.index(entry)

    def add(self, entry: str) -> None:
        """Add entry."""
        word = Word(*entry)
        self._words.append(word)
        self.notify('insert', index=self._words.index(word), item=word)

    def remove(self, item: str) -> None:
        """Remove entry from entries."""
        index = self.index(item)
        self.notify('pre_remove', index=index, item=item)
        del self._words[index]
        self.notify('remove', index=index, item=item)

    def clear(self) -> None:
        """Delete all entries."""
        self._words = []
        self.notify('clear')
