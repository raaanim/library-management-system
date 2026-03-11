from ..base import db


class BookModel(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    authors = db.Column(db.String(500), nullable=False)
    languages = db.Column(db.String(255), nullable=False)
    first_publish_year = db.Column(db.Integer, nullable=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "authors": self.authors.split(","),
            "languages": self.languages.split(","),
            "first_publish_year": self.first_publish_year,
        }

    def update_from_dict(self, data: dict) -> None:
        self.title = data["title"]
        self.authors = data["authors"]
        self.languages = data["languages"]
        self.first_publish_year = data.get("first_publish_year")
