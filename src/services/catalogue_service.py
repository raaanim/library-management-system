from src.models.base import db
from src.models.book.book_model import BookModel


class CatalogueService:

    def get_all_books(self) -> list[BookModel]:
        return BookModel.query.all()

    def get_book_by_id(self, book_id: int) -> BookModel | None:
        return BookModel.query.get(book_id)

    def add_book(self, data: dict) -> BookModel:
        book = BookModel(
            title=data["title"],
            authors=data["authors"],
            languages=data["languages"],
            first_publish_year=data.get("first_publish_year"),
        )
        db.session.add(book)
        db.session.commit()
        return book

    def remove_book(self, book_id: int) -> bool:
        book = self.get_book_by_id(book_id)
        if book is None:
            return False
        db.session.delete(book)
        db.session.commit()
        return True

    def search_by_title(self, title: str) -> list[BookModel]:
        return BookModel.query.filter(
            BookModel.title.ilike(
                f"%{title}%"
            )  # è una ricerca case-insensitive, quindi "tolkien" trova anche "Tolkien"
        ).all()

    def search_by_author(self, author: str) -> list[BookModel]:
        return BookModel.query.filter(BookModel.authors.ilike(f"%{author}%")).all()
