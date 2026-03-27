"""Fixtures for catalogue model tests including singleton reset and a
default catalogue."""

import pytest

from src.models.catalogue.catalogue import Catalogue
from src.models.catalogue.catalogue_model import CatalogueModel


@pytest.fixture(autouse=True)
def reset_catalogue_singleton():
    """Reset the Catalogue singleton before and after each test."""
    Catalogue.reset_instance()
    yield
    Catalogue.reset_instance()


@pytest.fixture
def catalogue(request):
    """Create and persist a default catalogue entry in the database."""
    database = request.getfixturevalue("db")
    c = CatalogueModel(name="Narrativa")
    database.session.add(c)
    database.session.commit()
    return c
