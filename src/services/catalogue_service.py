"""Service layer for catalogue and book management."""

from src.models.base import db
from src.models.book.book_model import BookModel
from src.models.catalogue.catalogue_model import CatalogueModel


class CatalogueService:
    """Singleton service for book catalogue operations."""

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def get_or_create_book(self, form_data: dict) -> BookModel:
        """Return existing book by work_id or create and persist a new one."""
        work_id = form_data.get("work_id")
        existing = BookModel.query.filter_by(work_id=work_id).first()
        if existing:
            return existing

        catalogue = CatalogueModel.query.first()
        catalogue_id = catalogue.id if catalogue else None

        first_publish_year = form_data.get("first_publish_year")
        if first_publish_year:
            try:
                first_publish_year = int(first_publish_year)
            except (ValueError, TypeError):
                first_publish_year = None

        book = BookModel(
            work_id=work_id,
            title=form_data.get("title") or "",
            authors=form_data.get("authors") or "",
            languages=form_data.get("languages") or "eng",
            first_publish_year=first_publish_year,
            cover_url=form_data.get("cover_url"),
            catalogue_id=catalogue_id,
        )
        db.session.add(book)
        db.session.flush()
        return book

    def get_random_books(self, limit: int = 20) -> list[BookModel]:
        """Return a random sample of books from the catalogue."""
        return BookModel.query.order_by(db.func.random()).limit(limit).all()

    def get_book_by_id(self, book_id: int) -> BookModel | None:
        """Fetch a book by primary key; return None if not found."""
        return db.session.get(BookModel, book_id)


catalogue_service = CatalogueService()
