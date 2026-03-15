# src/models/loan/loan_model.py
from datetime import date

from src.models.base import db


class LoanModel(db.Model):
    __tablename__ = "loans"

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(
        db.Integer, db.ForeignKey("members.id", ondelete="CASCADE"), nullable=False
    )
    book_id = db.Column(
        db.Integer, db.ForeignKey("books.id", ondelete="CASCADE"), nullable=False
    )
    loan_date = db.Column(db.Date, nullable=False, default=date.today)
    due_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)
    fine = db.Column(db.Float, nullable=False, default=0.0)

    member = db.relationship("MemberModel", back_populates="loans")
    book = db.relationship("BookModel", backref="loans")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "member_id": self.member_id,
            "book_id": self.book_id,
            "loan_date": self.loan_date.isoformat(),
            "due_date": self.due_date.isoformat(),
            "return_date": self.return_date.isoformat() if self.return_date else None,
            "fine": self.fine,
        }

    def update_from_dict(self, data: dict) -> None:
        self.due_date = data["due_date"]
        self.return_date = data.get("return_date")
        self.fine = data.get("fine", 0.0)
