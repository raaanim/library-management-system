from src.models.base import SerializerMixin, db
from src.models.book.book_model import BookModel

# Association table for Many-to-Many relationship between Wishlists and Books
wishlist_books = db.Table(
    "wishlist_books",
    db.Column(
        "wishlist_id",
        db.Integer,
        db.ForeignKey("wishlists.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "book_id",
        db.Integer,
        db.ForeignKey("books.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class WishlistModel(db.Model, SerializerMixin):
    __tablename__ = "wishlists"

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(
        db.Integer,
        db.ForeignKey("members.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    member = db.relationship("MemberModel", backref="wishlist")
    books = db.relationship(
        "BookModel",
        secondary=wishlist_books,
        lazy="subquery",
        backref=db.backref("wishlists", lazy=True),
    )

    def update_from_dict(self, data: dict) -> None:
        if "books" in data:
            book_ids = data.get("books", [])
            fetched_books = [db.session.get(BookModel, b_id) for b_id in book_ids]
            self.books = [b for b in fetched_books if b is not None]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "member_id": self.member_id,
            "books": self._get_ids_from_relation("books"),
        }
