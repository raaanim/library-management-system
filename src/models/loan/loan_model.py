from datetime import date

from src.models.base import db


class LoanModel(db.Model):
    """
    Modello SQLAlchemy che riflette la tabella 'loans' nel database.
    Mantiene i dati storici e attuali dei prestiti associando utenti e libri.
    """

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
        """Restituisce le proprietà del prestito a dizionario."""
        return {
            "id": self.id,
            "member_id": self.member_id,
            "book_id": self.book_id,
            "loan_date": self.loan_date.isoformat() if self.loan_date else None,
            "return_date": self.return_date.isoformat() if self.return_date else None,
        }

    def update(self, **kwargs) -> None:
        """Aggiorna le colonne in base ai kwargs forniti."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
