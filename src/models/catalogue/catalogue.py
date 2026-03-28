"""Domain entity representing the library catalogue (Singleton)."""

from src.models.book.book import Book


class Catalogue:
    """Singleton catalogue holding the in-memory list of books."""

    __instance = None

    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton instance for testing purposes."""
        cls.__instance = None

    def __new__(cls) -> "Catalogue":
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        if not hasattr(self, "__booklist"):
            self.__booklist: list[Book] = []

    def get_booklist(self) -> list[Book]:
        """Return a copy of the current book list."""
        return self.__booklist.copy()

    def set_booklist(self, booklist: list[Book]) -> None:
        """Replace the book list with a copy of the provided list."""
        self.__booklist = booklist.copy()

    def add_book(self, book: Book) -> None:
        """Append a book to the catalogue."""
        self.__booklist.append(book)

    def remove_book(self, book: Book) -> None:
        """Remove a book from the catalogue; raise ValueError if not found."""
        if book in self.__booklist:
            self.__booklist.remove(book)
        else:
            raise ValueError("Book not found in catalogue.")

    def search_by_title(self, title: str) -> list[Book]:
        """Return books whose title contains the given string
        (case-insensitive)."""
        results = [
            book
            for book in self.__booklist
            if (book_title := book.get_title()) is not None
            and title.lower() in book_title.lower()
        ]
        if not results:
            print("Book not found.")
        return results

    def search_by_author(self, author: str) -> list[Book]:
        """Return books that have at least one author matching the given
        string."""
        results = [
            book
            for book in self.__booklist
            if any(author.lower() in a.lower() for a in book.get_authors())
        ]
        if not results:
            print("Book not found.")
        return results

    def search_by_language(self, language: str) -> list[Book]:
        """Return books available in the given language."""
        results = [
            book
            for book in self.__booklist
            if any(language.lower() in lang.lower() for lang in book.get_languages())
        ]
        if not results:
            print("Book not found.")
        return results

    def __str__(self) -> str:
        return f"Available books: {[str(book) for book in self.__booklist]}"
