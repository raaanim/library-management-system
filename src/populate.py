"""Database population logic: fetches random books from OpenLibrary."""

import random

import requests

from src.models.base import db
from src.models.book.book_model import BookModel
from src.models.catalogue.catalogue_model import CatalogueModel

SUBJECTS = [
    "fiction",
    "science_fiction",
    "mystery",
    "fantasy",
    "biography",
    "history",
    "romance",
    "thriller",
    "philosophy",
    "poetry",
    "adventure",
    "horror",
    "science",
    "classic_literature",
    "historical_fiction",
    "detective_fiction",
    "dystopian_fiction",
    "literary_fiction",
    "crime_fiction",
    "drama",
]

COVER_BASE = "https://covers.openlibrary.org/b/id/{}-M.jpg"
TARGET = 200
PER_SUBJECT = 20


def fetch_books_for_subject(subject: str, offset: int) -> list[dict]:
    """Fetch books for a given subject from the OpenLibrary subjects API."""
    url = f"https://openlibrary.org/subjects/{subject}.json"
    try:
        resp = requests.get(
            url, params={"limit": PER_SUBJECT, "offset": offset}, timeout=10
        )
    except requests.RequestException:
        return []
    if resp.status_code != 200:
        return []
    works = resp.json().get("works", [])
    books = []
    for w in works:
        work_key = w.get("key", "")
        work_id = work_key.split("/")[-1] if work_key else None
        if not work_id:
            continue
        authors_list = w.get("authors", [])
        authors = (
            ", ".join(a.get("name", "") for a in authors_list) or "Autore sconosciuto"
        )
        cover_id = w.get("cover_id")
        cover_url = COVER_BASE.format(cover_id) if cover_id else None
        books.append(
            {
                "work_id": work_id,
                "title": w.get("title", ""),
                "authors": authors,
                "languages": "eng",
                "first_publish_year": w.get("first_publish_year"),
                "cover_url": cover_url,
            }
        )
    return books


def populate_books() -> int:
    """Populate the database with up to 200 random books linked to the
    catalogue."""
    catalogue = CatalogueModel.query.first()
    if not catalogue:
        catalogue = CatalogueModel(name="Biblioteca")
        db.session.add(catalogue)
        db.session.commit()

    existing_ids = {
        b.work_id for b in BookModel.query.with_entities(BookModel.work_id).all()
    }
    collected: dict[str, dict] = {}

    subjects = SUBJECTS.copy()
    random.shuffle(subjects)

    for subject in subjects:
        if len(collected) >= TARGET:
            break
        offset = random.randint(0, 300)
        print(f"  Fetching '{subject}' offset={offset}...")
        for book in fetch_books_for_subject(subject, offset):
            if book["work_id"] not in existing_ids and book["work_id"] not in collected:
                collected[book["work_id"]] = book
        print(f"  Totale raccolti: {len(collected)}")

    inserted = 0
    for book_data in collected.values():
        b = BookModel(
            work_id=book_data["work_id"],
            title=book_data["title"],
            authors=book_data["authors"],
            languages=book_data["languages"],
            first_publish_year=book_data["first_publish_year"],
            cover_url=book_data["cover_url"],
            catalogue_id=catalogue.id,
        )
        db.session.add(b)
        inserted += 1

    db.session.commit()
    print(f"Inseriti {inserted} libri nel catalogo '{catalogue.name}'.")
    return inserted
