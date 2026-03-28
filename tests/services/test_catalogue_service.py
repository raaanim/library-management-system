from src.models.book.book_model import BookModel


def test_creates_new_book(service, db):
    form = {
        "work_id": "OL999W",
        "title": "New Book",
        "authors": "Author",
        "languages": "eng",
        "first_publish_year": "2020",
        "cover_url": "https://img.com/c.jpg",
    }
    book = service.get_or_create_book(form)
    db.session.commit()
    assert book.work_id == "OL999W"
    assert book.title == "New Book"
    assert book.first_publish_year == 2020


def test_returns_existing_book(service, db):
    b = BookModel(work_id="OL1W", title="Existing", authors="A", languages="eng")
    db.session.add(b)
    db.session.commit()
    result = service.get_or_create_book({"work_id": "OL1W"})
    assert result.id == b.id


def test_invalid_year_becomes_none(service, db):
    form = {
        "work_id": "OL2W",
        "title": "Test",
        "authors": "A",
        "languages": "eng",
        "first_publish_year": "not_a_year",
    }
    book = service.get_or_create_book(form)
    db.session.commit()
    assert book.first_publish_year is None


def test_empty_title_uses_empty_string(service, db):
    form = {"work_id": "OL3W", "authors": "A", "languages": "eng"}
    book = service.get_or_create_book(form)
    db.session.commit()
    assert book.title == ""


def test_returns_list(service, db):
    b = BookModel(work_id="OL1W", title="Dune", authors="Herbert", languages="eng")
    db.session.add(b)
    db.session.commit()
    result = service.get_random_books(limit=5)
    assert isinstance(result, list)
    assert len(result) <= 5


def test_empty_db_returns_empty(service):
    assert service.get_random_books() == []


def test_returns_existing_book_by_id(service, db):
    b = BookModel(work_id="OL1W", title="Dune", authors="Herbert", languages="eng")
    db.session.add(b)
    db.session.commit()
    assert service.get_book_by_id(b.id) is not None


def test_returns_none_for_missing(service):
    assert service.get_book_by_id(9999) is None
