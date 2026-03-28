"""SQLAlchemy ORM model for the books table."""

from src.models.base import db


class BookModel(db.Model):
    """ORM model mapping the 'books' table with its catalogue relationship."""

    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    work_id = db.Column(db.String(20), nullable=True, unique=True, index=True)
    title = db.Column(db.String(255), nullable=False)
    authors = db.Column(db.String(500), nullable=False)
    languages = db.Column(db.String(255), nullable=False)
    first_publish_year = db.Column(db.Integer, nullable=True)
    cover_url = db.Column(db.String(500), nullable=True)
    catalogue_id = db.Column(db.Integer, db.ForeignKey("catalogues.id"), nullable=True)

    catalogue = db.relationship("CatalogueModel", back_populates="books")

    def to_dict(self) -> dict:
        """Return the book's fields as a dictionary."""
        return {
            "id": self.id,
            "work_id": self.work_id,
            "title": self.title,
            "authors": self.authors,
            "languages": self.languages,
            "first_publish_year": self.first_publish_year,
            "cover_url": self.cover_url,
            "catalogue_id": self.catalogue_id,
        }

    def update(self, **kwargs) -> None:
        """Update model columns from keyword arguments."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
