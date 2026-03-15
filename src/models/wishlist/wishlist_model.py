from src.models.base import db

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


class WishlistModel(db.Model):
    """
    Modello SQLAlchemy che riflette la tabella 'wishlists' nel database.
    Gestisce la relazione uno-a-uno con il membro e molti-a-molti con i libri.
    """

    __tablename__ = "wishlists"

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(
        db.Integer,
        db.ForeignKey("members.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    def to_dict(self) -> dict:
        """Ritorna la wishlist e l'ID del proprietario."""
        return {
            "id": self.id,
            "member_id": self.member_id,
        }

    def update(self, **kwargs) -> None:
        """Aggiorna le colonne in base ai kwargs forniti."""
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
