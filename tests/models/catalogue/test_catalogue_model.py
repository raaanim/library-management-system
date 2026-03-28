"""Tests for the CatalogueModel ORM class and Catalogue domain model
operations."""

import pytest

from src.models.book.book import Book
from src.models.catalogue.catalogue import Catalogue


class TestCatalogueModelToDict:
    """Tests for CatalogueModel.to_dict serialisation."""

    def test_to_dict_keys(self, catalogue):
        """Test that to_dict includes id and name keys."""
        d = catalogue.to_dict()
        assert "id" in d
        assert "name" in d

    def test_to_dict_values(self, catalogue):
        """Test that to_dict returns the correct catalogue name."""
        d = catalogue.to_dict()
        assert d["name"] == "Narrativa"


class TestCatalogueModelUpdate:
    """Tests for CatalogueModel.update method."""

    def test_update_name(self, catalogue):
        """Test that update changes the catalogue name."""
        catalogue.update(name="Saggistica")
        assert catalogue.name == "Saggistica"

    def test_update_ignores_unknown_keys(self, catalogue):
        """Test that update silently ignores unknown field names."""
        catalogue.update(nonexistent="value")


class TestCatalogueDomain:
    """Tests for the Catalogue domain singleton book management."""

    def test_add_and_get_book(self):
        """Test that add_book makes the book retrievable via get_booklist."""
        c = Catalogue()
        b = Book(id=1, title="Dune")
        c.add_book(b)
        assert b in c.get_booklist()

    def test_remove_existing_book(self):
        """Test that remove_book removes an existing book from the
        catalogue."""
        c = Catalogue()
        b = Book(id=1, title="Dune")
        c.add_book(b)
        c.remove_book(b)
        assert not c.get_booklist()

    def test_remove_non_existing_raises(self):
        """Test that removing a book not in the catalogue raises ValueError."""
        c = Catalogue()
        b = Book(id=99, title="Ghost")
        with pytest.raises(ValueError):
            c.remove_book(b)
