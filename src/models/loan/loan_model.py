"""SQLAlchemy ORM model for the loans table."""

from datetime import date

from src.models.base import db


class LoanModel(db.Model):
    """ORM model mapping the 'loans' table, associating members with
    borrowed books."""

    __tablename__ = "loans"

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(
        db.Integer,
        db.ForeignKey("members.id", ondelete="CASCADE"),
        nullable=False,
    )
    book_id = db.Column(
        db.Integer,
        db.ForeignKey("books.id", ondelete="CASCADE"),
        nullable=False,
    )
    loan_date = db.Column(db.Date, nullable=False, default=date.today)
    due_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)
    fine = db.Column(db.Float, nullable=False, default=0.0)

    member = db.relationship("MemberModel", back_populates="loans")
    book = db.relationship("BookModel", backref="loans")

    def to_dict(self) -> dict:
        """Return the loan's fields as a dictionary."""
        return {
            "id": self.id,
            "member_id": self.member_id,
            "book_id": self.book_id,
            "loan_date": (self.loan_date.isoformat() if self.loan_date else None),
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "return_date": (self.return_date.isoformat() if self.return_date else None),
            "fine": self.fine,
        }

    def update(self, **kwargs) -> None:
        """Update model columns from keyword arguments, protecting member_id
        and book_id."""
        protected = {"member_id", "book_id"}
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in protected:
                setattr(self, key, value)
