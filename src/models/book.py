# Gestisce i dati dei libri nel database.


from dataclasses import dataclass
from typing import List


@dataclass
class Book:
    id: int
    title: str
    authors: List[str]
    language: List[str]
    first_publish_year: int

    def __str__(self) -> str:
        authors = ", ".join(self.authors)
        languages = ", ".join(self.language)
        return f"{self.title} ({self.first_publish_year}) - {authors} [{languages}]"
