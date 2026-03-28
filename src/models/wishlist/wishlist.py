"""Domain entity representing a member's wishlist."""

from src.models.book.book import Book
from src.models.member.member import Member


class Wishlist:
    """Domain entity for a wishlist: lets members save and manage books
    of interest."""

    def __init__(self, member: Member) -> None:
        self.__member = member
        self.__books: list[Book] = []

    def get_member(self) -> Member:
        """Return the member who owns this wishlist."""
        return self.__member

    def get_books(self) -> list[Book]:
        """Return a copy of the wishlist's book list."""
        return self.__books.copy()

    def add_book(self, book: Book) -> None:
        """Add a book to the wishlist if it is not already present."""
        if book not in self.__books:
            self.__books.append(book)

    def remove_book(self, book: Book) -> None:
        """Remove a book from the wishlist if present."""
        if book in self.__books:
            self.__books.remove(book)

    def __str__(self) -> str:
        books_list = (
            ", ".join(
                [
                    title
                    for title in [book.get_title() for book in self.__books]
                    if title is not None
                ]
            )
            if self.__books
            else "nessun libro"
        )
        return f"Wishlist di {self.__member.get_username()}: {books_list}"
