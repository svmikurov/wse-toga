"""Foreign data source implementation."""

from toga.sources import Source


class Word:
    """A class to wrap individual word."""

    def __init__(self, foreign_word: str, native_word: str) -> None:
        """Construct the word wrap."""
        self.foreign_word = foreign_word
        self.native_word = native_word


class WordSource(Source):
    """Word entries source."""

    def __init__(self) -> None:
        """Construct the source."""
        super().__init__()
        self._words = []
        self.accessors = ['foreign_word', 'native_word']

    def __len__(self) -> int:
        """Get len items."""
        return len(self._words)

    def __getitem__(self, index: int) -> str:
        """Get entry value."""
        return self._words[index]

    def index(self, entry: str) -> int:
        """Get entry index."""
        return self._words.index(entry)

    def add_entry(self, entry: tuple[str, ...]) -> None:
        """Add entry to terms.

        Adds ('item', 'item', ...) to self._terms (`list`).
        """
        term = Word(*entry)
        self.add_term(term)

    def add_term(self, term: Word) -> None:
        """Add term to terms.

        Add <wse.sources.glossary.Term X ...> to self._terms (`list`).
        """
        self._words.append(term)
        self.notify('insert', index=self._words.index(term), item=term)

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
