"""SQLAlchemy ORM model for the wishlists table."""

from src.models.base import db

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


class WishlistModel(db.Model):
    """ORM model mapping the 'wishlists' table with one-to-one member and
    many-to-many books."""

    __tablename__ = "wishlists"

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(
        db.Integer,
        db.ForeignKey("members.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    def to_dict(self) -> dict:
        """Return the wishlist id and owner member_id as a dictionary."""
        return {
            "id": self.id,
            "member_id": self.member_id,
        }

    def update(self, **kwargs) -> None:
        """Update model columns from keyword arguments."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    member = db.relationship("MemberModel", backref="wishlist")
    books = db.relationship(
        "BookModel",
        secondary=wishlist_books,
        lazy="subquery",
        backref=db.backref("wishlists", lazy=True),
    )
