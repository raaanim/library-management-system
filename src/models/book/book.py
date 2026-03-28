"""Domain entity representing a Book, with getters and setters."""


class Book:
    """Domain entity for a book: encapsulates title, authors, languages
    and metadata."""

    def __init__(self, **kwargs) -> None:
        self.__id: str | int | None = kwargs.get("id")
        self.__title: str | None = kwargs.get("title")
        self.__authors: list[str] = kwargs.get("authors", [])
        self.__languages: list[str] = kwargs.get("languages", [])
        self.__first_publish_year: int | None = kwargs.get("first_publish_year")
        self.__cover_url: str | None = kwargs.get("cover_url")

    def get_id(self) -> str | int | None:
        """Return the book identifier."""
        return self.__id

    def get_title(self) -> str | None:
        """Return the book title."""
        return self.__title

    def get_authors(self) -> list[str]:
        """Return a copy of the authors list."""
        return self.__authors.copy()

    def get_languages(self) -> list[str]:
        """Return a copy of the languages list."""
        return self.__languages.copy()

    def get_first_publish_year(self) -> int | None:
        """Return the first publication year."""
        return self.__first_publish_year

    def get_cover_url(self) -> str | None:
        """Return the cover image URL."""
        return self.__cover_url

    def set_title(self, title: str) -> None:
        """Set the book title."""
        self.__title = title

    def set_authors(self, authors: list[str]) -> None:
        """Set the authors list (stored as a copy)."""
        self.__authors = authors.copy()

    def set_languages(self, languages: list[str]) -> None:
        """Set the languages list (stored as a copy)."""
        self.__languages = languages.copy()

    def set_first_publish_year(self, year: int) -> None:
        """Set the first publication year."""
        self.__first_publish_year = year

    def set_cover_url(self, cover_url: str) -> None:
        """Set the cover image URL."""
        self.__cover_url = cover_url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Book):
            return False
        return self.__id == other.get_id()

    def __str__(self) -> str:
        authors = ", ".join(self.__authors)
        languages = ", ".join(self.__languages)
        return (
            f"{self.__title} ({self.__first_publish_year}) - "
            f"{authors} [{languages}]"
        )
