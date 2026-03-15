from src.models.base import db


class BookModel(db.Model):
    """
    Modello SQLAlchemy per mappare la tabella 'books' nel database.
    Definisce le colonne e le relazioni (es. con il catalogo) per la persistenza dei libri.
    """

    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    work_id = db.Column(db.String(20), nullable=True, unique=True, index=True)
    title = db.Column(db.String(255), nullable=False)
    authors = db.Column(db.String(500), nullable=False)
    languages = db.Column(db.String(255), nullable=False)
    first_publish_year = db.Column(db.Integer, nullable=True)

    def to_dict(self) -> dict:
        """Restituisce le proprietà del libro in formato dizionario."""
        return {
            "id": self.id,
            "work_id": self.work_id,
            "title": self.title,
            "authors": self.authors,
            "languages": self.languages,
            "first_publish_year": self.first_publish_year,
        }

    def update(self, **kwargs) -> None:
        """Aggiorna le colonne del modello in base ai kwargs forniti."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    cover_url = db.Column(db.String(500), nullable=True)
    catalogue_id = db.Column(db.Integer, db.ForeignKey("catalogues.id"), nullable=True)

    catalogue = db.relationship("CatalogueModel", back_populates="books")
