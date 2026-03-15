from src.models.base import SerializerMixin, db


class MemberModel(db.Model, SerializerMixin):
    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(255), nullable=True, default="")
    loans = db.relationship("LoanModel", back_populates="member")

    def update_from_dict(self, data: dict) -> None:
        self.username = data["username"]
        self.email = data["email"]
        self.password = data["password"]
        self.address = data.get("address", "")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "address": self.address,
            "loans": self._get_ids_from_relation("loans"),
        }
