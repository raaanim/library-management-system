from datetime import date

from src.models.base import db


class MemberModel(db.Model):
    """
    Modello SQLAlchemy che mappa la tabella 'members' nel database.
    Definisce l'anagrafica degli iscritti e la loro relazione con i prestiti.
    """

    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True)
    registration_date = db.Column(db.Date, nullable=False, default=date.today)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(255), nullable=True, default="")
    loans = db.relationship("LoanModel", back_populates="member")

    def to_dict(self) -> dict:
        """Ritorna i dettagli dell'utente omettendo la password."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "registration_date": self.registration_date.isoformat(),
        }

    def update(self, **kwargs) -> None:
        """Aggiorna le colonne in base ai kwargs forniti."""
        for key, value in kwargs.items():
            if (
                hasattr(self, key) and key != "password"
            ):  # Previene update password diretto
                setattr(self, key, value)
