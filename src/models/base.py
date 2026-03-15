from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class SerializerMixin:

    def _get_ids_from_relation(self, relation_name: str) -> list[int]:
        relation = getattr(self, relation_name, None)
        if relation and hasattr(relation, "__iter__"):
            return [item.id for item in relation]
        return []

    def to_dict(self) -> dict:
        raise NotImplementedError("Subclasses must implement to_dict method")

    def update_from_dict(self, data: dict) -> None:
        raise NotImplementedError("Subclasses must implement update_from_dict method")
