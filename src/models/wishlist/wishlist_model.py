from ..base import db
from ..book.book_model import BookModel


class WishlistModel(db.Model):
    __tablename__ = "wishlists"

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(
        db.Integer, db.ForeignKey("members.id"), unique=True, nullable=False
    )

    member = db.relationship("MemberModel", backref="wishlist")
    books = db.relationship(
        "BookModel",
        backref="wishlists",
    )

    def update_from_dict(self, data: dict) -> None:
        if "books" in data:
            self.books = [
                db.session.get(BookModel, book_id) for book_id in data["books", []]
            ]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "member_id": self.member_id,
            "books": [book.id for book in self.books],
        }
