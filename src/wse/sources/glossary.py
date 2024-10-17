"""Glossary data source implementation."""

from toga.sources import Source


class Term:
    """A class to wrap individual term."""

    def __init__(
        self,
        id: str,
        term: str,
        definition: str,
    ) -> None:
        """Construct the term wrap."""
        self.id = int(id)
        self.term = term
        self.definition = definition


class TermSource(Source):
    """Glossary term entries source."""

    def __init__(self) -> None:
        """Construct the source."""
        super().__init__()
        self._terms = []
        self.accessors = ['id', 'term', 'definition']

    def __len__(self) -> int:
        """Get len items."""
        return len(self._terms)

    def __setitem__(self, index: int, term: Term) -> None:
        """Set term to terms by index."""
        self._terms.insert(index, term)
        self.notify('insert', index=self._terms.index(term), item=term)

    def __getitem__(self, index: int) -> str:
        """Get entry value."""
        return self._terms[index]

    def update(self, old_entry: Term, new_entry: Term) -> None:
        """Update the data source list."""
        index = self._terms.index(old_entry)
        self.remove(old_entry)
        self.__setitem__(index, new_entry)

    def index(self, entry: Term) -> int:
        """Get entry index."""
        return self._terms.index(entry)

    def add_entry(self, entry: tuple[str, ...]) -> None:
        """Add entry to terms.

        Adds ('item', 'item', ...) to self._terms (`list`).
        """
        term = Term(*entry)
        self.add_term(term)

    def add_term(self, term: Term) -> None:
        """Add term to terms.

        Add <wse.sources.glossary.Term X ...> to self._terms (`list`).
        """
        self._terms.append(term)
        self.notify('insert', index=self._terms.index(term), item=term)

    def remove(self, item: Term) -> None:
        """Remove entry from entries."""
        index = self.index(item)
        self.notify('pre_remove', index=index, item=item)
        del self._terms[index]
        self.notify('remove', index=index, item=item)

    def clear(self) -> None:
        """Delete all entries."""
        self._terms = []
        self.notify('clear')
