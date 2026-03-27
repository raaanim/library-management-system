from unittest.mock import MagicMock, patch

from requests.exceptions import ConnectionError as RequestsConnectionError
from requests.exceptions import Timeout


def mock_response(json_data, status_code=200):
    m = MagicMock()
    m.json.return_value = json_data
    m.status_code = status_code
    return m


def test_search_returns_list(reader):
    data = {
        "docs": [
            {
                "key": "/works/OL18317W",
                "title": "Dune",
                "author_name": ["Frank Herbert"],
                "cover_i": 123,
                "first_publish_year": 1965,
            }
        ]
    }
    with patch("src.services.reader.get", return_value=mock_response(data)):
        results = reader.search("dune")
    assert len(results) == 1
    assert results[0]["work_id"] == "OL18317W"
    assert results[0]["title"] == "Dune"
    assert "cover_url" in results[0]


def test_search_no_cover(reader):
    data = {
        "docs": [
            {
                "key": "/works/OL1W",
                "title": "Test",
                "author_name": [],
                "first_publish_year": 2000,
            }
        ]
    }
    with patch("src.services.reader.get", return_value=mock_response(data)):
        results = reader.search("test")
    assert results[0]["cover_url"] is None


def test_search_network_error_returns_empty(reader):
    with patch("src.services.reader.get", side_effect=Timeout()):
        results = reader.search("dune")
    assert results == []


def test_search_connection_error_returns_empty(reader):
    with patch("src.services.reader.get", side_effect=RequestsConnectionError()):
        results = reader.search("dune")
    assert results == []


def test_search_by_author(reader):
    data = {
        "docs": [{"key": "/works/OL1W", "title": "Test", "author_name": ["Tolkien"]}]
    }
    with patch("src.services.reader.get", return_value=mock_response(data)) as mock_get:
        reader.search("tolkien", by="author")
    assert "author" in mock_get.call_args[1]["params"]


def test_returns_lang_edition_map(reader):
    data = {
        "entries": [
            {"key": "/books/OL1M", "languages": [{"key": "/languages/ita"}]},
            {"key": "/books/OL2M", "languages": [{"key": "/languages/eng"}]},
        ]
    }
    with patch("src.services.reader.get", return_value=mock_response(data)):
        result = reader.get_editions_by_language("OL18317W")
    assert result["ita"] == "OL1M"
    assert result["eng"] == "OL2M"


def test_skips_entries_without_language(reader):
    data = {"entries": [{"key": "/books/OL1M", "languages": []}]}
    with patch("src.services.reader.get", return_value=mock_response(data)):
        result = reader.get_editions_by_language("OL1W")
    assert result == {}


def test_first_edition_per_language_wins(reader):
    data = {
        "entries": [
            {"key": "/books/OL1M", "languages": [{"key": "/languages/eng"}]},
            {"key": "/books/OL2M", "languages": [{"key": "/languages/eng"}]},
        ]
    }
    with patch("src.services.reader.get", return_value=mock_response(data)):
        result = reader.get_editions_by_language("OL1W")
    assert result["eng"] == "OL1M"


def test_network_error_returns_empty_map(reader):
    with patch("src.services.reader.get", side_effect=Timeout()):
        result = reader.get_editions_by_language("OL1W")
    assert result == {}


def test_returns_edition_dict(reader):
    data = {
        "title": "Dune",
        "languages": [{"key": "/languages/ita"}],
        "publishers": ["Mondadori"],
        "publish_date": "2021",
        "isbn_13": ["9788804737490"],
        "isbn_10": ["8804737492"],
        "number_of_pages": 604,
        "covers": [12345],
        "works": [{"key": "/works/OL18317W"}],
    }
    with patch("src.services.reader.get", return_value=mock_response(data)):
        result = reader.get_edition("OL1M")
    assert result["title"] == "Dune"
    assert result["language"] == "ita"
    assert result["work_id"] == "OL18317W"
    assert result["isbn_13"] == "9788804737490"
    assert "cover_url_large" in result


def test_returns_none_on_404_edition(reader):
    with patch(
        "src.services.reader.get",
        return_value=mock_response({}, status_code=404),
    ):
        result = reader.get_edition("OL_BAD")
    assert result is None


def test_returns_none_on_network_error_edition(reader):
    with patch("src.services.reader.get", side_effect=Timeout()):
        result = reader.get_edition("OL1M")
    assert result is None


def test_no_cover_returns_none_url_edition(reader):
    data = {"title": "Test", "languages": [], "works": []}
    with patch("src.services.reader.get", return_value=mock_response(data)):
        result = reader.get_edition("OL1M")
    assert result["cover_url_large"] is None


def test_no_language_defaults_unknown(reader):
    data = {"title": "Test", "languages": [], "works": []}
    with patch("src.services.reader.get", return_value=mock_response(data)):
        result = reader.get_edition("OL1M")
    assert result["language"] == "unknown"


def test_returns_work_dict(reader):
    data = {
        "title": "Dune",
        "description": "A great book",
        "subjects": [
            "sci-fi",
            "desert",
            "politics",
            "ecology",
            "spice",
            "sandworm",
            "Atreides",
            "power",
        ],
        "first_publish_date": "1 August 1965",
        "covers": [8739161],
    }
    with patch("src.services.reader.get", return_value=mock_response(data)):
        result = reader.get_work("OL18317W")
    assert result["title"] == "Dune"
    assert result["description"] == "A great book"
    assert len(result["subjects"]) <= 8


def test_description_as_dict(reader):
    data = {
        "title": "Dune",
        "description": {"type": "/type/text", "value": "A great book"},
        "subjects": [],
        "covers": [],
    }
    with patch("src.services.reader.get", return_value=mock_response(data)):
        result = reader.get_work("OL18317W")
    assert result["description"] == "A great book"


def test_returns_none_on_404_work(reader):
    with patch(
        "src.services.reader.get",
        return_value=mock_response({}, status_code=404),
    ):
        result = reader.get_work("OL_BAD")
    assert result is None


def test_returns_none_on_network_error_work(reader):
    with patch("src.services.reader.get", side_effect=Timeout()):
        result = reader.get_work("OL1W")
    assert result is None


def test_no_cover_returns_none_url_work(reader):
    data = {"title": "Test", "subjects": [], "covers": []}
    with patch("src.services.reader.get", return_value=mock_response(data)):
        result = reader.get_work("OL1W")
    assert result["cover_url_large"] is None
