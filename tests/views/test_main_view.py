from unittest.mock import patch

FAKE_WORK = {
    "title": "Dune",
    "description": "Great book",
    "subjects": ["sci-fi"],
    "first_publish_date": "1965",
    "cover_url_large": "https://img.com/large.jpg",
}

FAKE_EDITION = {
    "edition_id": "OL1M",
    "work_id": "OL18317W",
    "title": "Dune",
    "language": "ita",
    "publishers": ["Mondadori"],
    "publish_date": "2021",
    "isbn_13": "9788804737490",
    "isbn_10": None,
    "number_of_pages": 604,
    "cover_url_large": "https://img.com/large.jpg",
}


def test_index_empty_db(client):
    r = client.get("/")
    assert r.status_code == 200


def test_index_with_book(client, book):
    r = client.get("/")
    assert r.status_code == 200
    assert book.title.encode() in r.data


def test_search_no_query_redirects(client):
    r = client.get("/search")
    assert r.status_code == 302


def test_search_with_results(client):
    fake_results = [
        {
            "work_id": "OL18317W",
            "title": "Dune",
            "authors": ["Herbert"],
            "first_publish_year": 1965,
            "cover_url": None,
        }
    ]
    with (
        patch("src.views.main_view.reader.search", return_value=fake_results),
        patch(
            "src.views.main_view.reader.get_editions_by_language",
            return_value={"ita": "OL1M"},
        ),
    ):
        r = client.get("/search?q=dune")
    assert r.status_code == 200
    assert b"Dune" in r.data


def test_search_by_author(client):
    with (
        patch("src.views.main_view.reader.search", return_value=[]),
        patch(
            "src.views.main_view.reader.get_editions_by_language",
            return_value={},
        ),
    ):
        r = client.get("/search?q=tolkien&by=author")
    assert r.status_code == 200


def test_search_invalid_by_defaults_to_title(client):
    with (
        patch("src.views.main_view.reader.search", return_value=[]) as mock_search,
        patch(
            "src.views.main_view.reader.get_editions_by_language",
            return_value={},
        ),
    ):
        client.get("/search?q=test&by=invalid")
    mock_search.assert_called_once()
    assert mock_search.call_args[1]["by"] == "title"


def test_search_empty_results(client):
    with (
        patch("src.views.main_view.reader.search", return_value=[]),
        patch(
            "src.views.main_view.reader.get_editions_by_language",
            return_value={},
        ),
    ):
        r = client.get("/search?q=xyz")
    assert r.status_code == 200


def test_book_detail_found(client):
    with (
        patch("src.views.main_view.reader.get_work", return_value=FAKE_WORK),
        patch(
            "src.views.main_view.reader.get_editions_by_language",
            return_value={"ita": "OL1M"},
        ),
    ):
        r = client.get("/book/OL18317W")
    assert r.status_code == 200
    assert b"Dune" in r.data


def test_book_detail_not_found(client):
    with patch("src.views.main_view.reader.get_work", return_value=None):
        r = client.get("/book/INVALID")
    assert r.status_code == 404


def test_edition_detail_found(client):
    with (
        patch("src.views.main_view.reader.get_edition", return_value=FAKE_EDITION),
        patch("src.views.main_view.reader.get_work", return_value=FAKE_WORK),
    ):
        r = client.get("/book/edition/OL1M")
    assert r.status_code == 200
    assert b"Dune" in r.data


def test_edition_detail_not_found(client):
    with patch("src.views.main_view.reader.get_edition", return_value=None):
        r = client.get("/book/edition/INVALID")
    assert r.status_code == 404


def test_edition_detail_no_work_id(client):
    edition_no_work = {**FAKE_EDITION, "work_id": None}
    with patch("src.views.main_view.reader.get_edition", return_value=edition_no_work):
        r = client.get("/book/edition/OL1M")
    assert r.status_code == 200
