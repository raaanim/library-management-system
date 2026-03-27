"""Tests for the BookModel ORM class serialisation and update methods."""

from src.models.book.book_model import BookModel


class TestBookModelToDict:
    """Tests for BookModel.to_dict serialisation."""

    def test_to_dict_keys(self, book):
        """Test that to_dict returns all expected keys."""
        d = book.to_dict()
        assert set(d.keys()) == {
            "id",
            "work_id",
            "title",
            "authors",
            "languages",
            "first_publish_year",
            "cover_url",
            "catalogue_id",
        }

    def test_to_dict_values(self, book):
        """Test that to_dict returns correct field values."""
        d = book.to_dict()
        assert d["work_id"] == "OL1W"
        assert d["title"] == "Dune"
        assert d["authors"] == "Herbert"

    def test_book_model_is_instance(self, book):
        """Test that the book fixture is an instance of BookModel."""
        assert isinstance(book, BookModel)


class TestBookModelUpdate:
    """Tests for BookModel.update method."""

    def test_update_title(self, book):
        """Test that update changes the title field."""
        book.update(title="Foundation")
        assert book.title == "Foundation"

    def test_update_ignores_unknown_keys(self, book):
        """Test that update silently ignores unknown field names."""
        book.update(nonexistent_field="value")

    def test_update_multiple_fields(self, book):
        """Test that update can modify multiple fields at once."""
        book.update(title="1984", authors="George Orwell")
        assert book.title == "1984"
        assert book.authors == "George Orwell"
