from src.models.base import SerializerMixin, db


class CatalogueModel(db.Model, SerializerMixin):
    __tablename__ = "catalogues"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, default="Main Catalogue")

    books = db.relationship("BookModel", back_populates="catalogue", lazy="select")

    def update_from_dict(self, data: dict) -> None:
        if "name" in data:
            self.name = data["name"]

        if "books" in data:
            books_data = data["books"]
            if isinstance(books_data, list):
                if not books_data:
                    self.books = []
                else:
                    first_item = books_data[0]
                    if not isinstance(first_item, (int, str)):
                        self.books = books_data

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "books": self._get_ids_from_relation("books"),
        }
