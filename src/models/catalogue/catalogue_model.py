from src.models.base import db


class CatalogueModel(db.Model):
    """
    Modello SQLAlchemy per mappare la tabella 'catalogues' nel database.
    Gestisce i dati del catalogo e la relazione (uno-a-molti) con i libri ad esso associati.
    """

    __tablename__ = "catalogues"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, default="Main Catalogue")

    books = db.relationship("BookModel", back_populates="catalogue", lazy="select")

    def to_dict(self) -> dict:
        """Restituisce le proprietà a dizionario."""
        return {
            "id": self.id,
            "name": self.name,
            "books": [book.to_dict() for book in getattr(self, "books", [])],
        }

    def update(self, **kwargs) -> None:
        """Aggiorna le colonne in base ai kwargs forniti."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
