"""SQLAlchemy ORM model for the members table."""

from datetime import date

from src.models.base import db


class MemberModel(db.Model):
    """ORM model mapping the 'members' table with its loans
    relationship."""

    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True)
    registration_date = db.Column(db.Date, nullable=False, default=date.today)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(255), nullable=True, default="")
    loans = db.relationship("LoanModel", back_populates="member")

    def to_dict(self) -> dict:
        """Return member fields as a dictionary, excluding the password."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "registration_date": self.registration_date.isoformat(),
        }

    def update(self, **kwargs) -> None:
        """Update model columns from keyword arguments, ignoring password
        changes."""
        for key, value in kwargs.items():
            if hasattr(self, key) and key != "password":
                setattr(self, key, value)
