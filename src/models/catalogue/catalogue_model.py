"""SQLAlchemy ORM model for the catalogues table."""

from src.models.base import db


class CatalogueModel(db.Model):
    """ORM model mapping the 'catalogues' table with its one-to-many
    books relationship."""

    __tablename__ = "catalogues"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, default="Main Catalogue")

    books = db.relationship("BookModel", back_populates="catalogue", lazy="select")

    def to_dict(self) -> dict:
        """Return catalogue fields as a dictionary including all linked
        books."""
        return {
            "id": self.id,
            "name": self.name,
            "books": [book.to_dict() for book in getattr(self, "books", [])],
        }

    def update(self, **kwargs) -> None:
        """Update model columns from keyword arguments."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
