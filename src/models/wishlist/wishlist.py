from src.models.book.book import Book
from src.models.member.member import Member


class Wishlist:
    def __init__(self, member: Member) -> None:
        self.__member = member
        self.__books: list[Book] = []

    def get_member(self) -> Member:
        return self.__member

    def get_books(self) -> list[Book]:
        return self.__books.copy()

    def add_book(self, book: Book) -> None:
        if book not in self.__books:
            self.__books.append(book)

    def remove_book(self, book: Book) -> None:
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
