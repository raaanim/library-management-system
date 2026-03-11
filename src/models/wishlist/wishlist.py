from ..book.book import Book
from ..member.member import Member


class Wishlist:
    def __init__(self, member: Member, books: list[Book] = None) -> None:
        self.member = member
        self.books = list(books or [])

    def add_book(self, book: Book) -> None:
        if book not in self.books:
            self.books.append(book)

    def remove_book(self, book: Book) -> None:
        if book in self.books:
            self.books.remove(book)

    def __str__(self) -> str:
        books_list = (
            ", ".join([book.title for book in self.books])
            if self.books
            else "nessun libro"
        )
        return f"Wishlist di {self.member.get_username()}: {books_list}"
