from src.models.base import db


class BookModel(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    authors = db.Column(db.String(500), nullable=False)
    languages = db.Column(db.String(255), nullable=False)
    first_publish_year = db.Column(db.Integer, nullable=True)
    cover_url = db.Column(db.String(500), nullable=True)
    catalogue_id = db.Column(db.Integer, db.ForeignKey("catalogues.id"), nullable=True)

    catalogue = db.relationship("CatalogueModel", back_populates="books")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "authors": self.authors.split(","),
            "languages": self.languages.split(","),
            "first_publish_year": self.first_publish_year,
            "cover_url": self.cover_url,
            "catalogue_id": self.catalogue_id,
        }

    def update_from_dict(self, data: dict) -> None:
        self.title = data["title"]
        self.authors = (
            ",".join(data["authors"])
            if isinstance(data["authors"], list)
            else data["authors"]
        )
        self.languages = (
            ",".join(data["languages"])
            if isinstance(data["languages"], list)
            else data["languages"]
        )
        self.first_publish_year = data.get("first_publish_year")
        self.cover_url = data.get("cover_url")
        self.catalogue_id = data.get("catalogue_id")
