"""Tests for the Book domain model getters, setters, and equality."""

from src.models.book.book import Book


def make_book(**kwargs):
    """Return a Book instance with default values overridden by kwargs."""
    defaults = {
        "id": 1,
        "title": "Dune",
        "authors": ["Frank Herbert"],
        "languages": ["eng"],
        "first_publish_year": 1965,
        "cover_url": "https://example.com/cover.jpg",
    }
    defaults.update(kwargs)
    return Book(**defaults)


class TestBookGetters:
    """Tests for Book getter methods."""

    def test_get_id(self):
        """Test that get_id returns the correct book id."""
        assert make_book(id=42).get_id() == 42

    def test_get_title(self):
        """Test that get_title returns the correct title."""
        assert make_book().get_title() == "Dune"

    def test_get_authors(self):
        """Test that get_authors returns the list of authors."""
        assert make_book().get_authors() == ["Frank Herbert"]

    def test_get_languages(self):
        """Test that get_languages returns the list of languages."""
        assert make_book().get_languages() == ["eng"]

    def test_get_first_publish_year(self):
        """Test that get_first_publish_year returns the correct year."""
        assert make_book().get_first_publish_year() == 1965

    def test_get_cover_url(self):
        """Test that get_cover_url returns the correct URL."""
        assert make_book().get_cover_url() == "https://example.com/cover.jpg"

    def test_defaults_empty(self):
        """Test that a Book created with no args has all-None/empty
        defaults."""
        b = Book()
        assert b.get_id() is None
        assert b.get_title() is None
        assert not b.get_authors()
        assert not b.get_languages()
        assert b.get_first_publish_year() is None
        assert b.get_cover_url() is None


class TestBookSetters:
    """Tests for Book setter methods and defensive copy behaviour."""

    def test_set_title(self):
        """Test that set_title updates the book title."""
        b = make_book()
        b.set_title("Foundation")
        assert b.get_title() == "Foundation"

    def test_set_authors_defensive_copy(self):
        """Test that set_authors stores a defensive copy of the list."""
        b = make_book()
        authors = ["Author A"]
        b.set_authors(authors)
        authors.append("Author B")
        assert b.get_authors() == ["Author A"]

    def test_set_languages_defensive_copy(self):
        """Test that set_languages stores a defensive copy of the list."""
        b = make_book()
        langs = ["eng"]
        b.set_languages(langs)
        langs.append("ita")
        assert b.get_languages() == ["eng"]

    def test_set_first_publish_year(self):
        """Test that set_first_publish_year updates the publication year."""
        b = make_book()
        b.set_first_publish_year(2000)
        assert b.get_first_publish_year() == 2000

    def test_set_cover_url(self):
        """Test that set_cover_url updates the cover URL."""
        b = make_book()
        b.set_cover_url("https://new.url/img.jpg")
        assert b.get_cover_url() == "https://new.url/img.jpg"

    def test_get_authors_defensive_copy(self):
        """Test that get_authors returns a defensive copy."""
        b = make_book()
        b.get_authors().append("Fake")
        assert b.get_authors() == ["Frank Herbert"]

    def test_get_languages_defensive_copy(self):
        """Test that get_languages returns a defensive copy."""
        b = make_book()
        b.get_languages().append("ita")
        assert b.get_languages() == ["eng"]


class TestBookEquality:
    """Tests for Book equality and string representation."""

    def test_equal_same_id(self):
        """Test that two books with the same id are equal."""
        assert make_book(id=1) == make_book(id=1)

    def test_not_equal_different_id(self):
        """Test that books with different ids are not equal."""
        assert make_book(id=1) != make_book(id=2)

    def test_not_equal_non_book(self):
        """Test that a Book is not equal to a non-Book object."""
        assert make_book() != "not a book"

    def test_str_contains_key_info(self):
        """Test that str(book) includes title and author information."""
        s = str(make_book())
        assert "Dune" in s
        assert "Frank Herbert" in s
