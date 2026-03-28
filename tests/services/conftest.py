import pytest

from src.services.catalogue_service import CatalogueService
from src.services.reader import Reader


@pytest.fixture
def service():
    return CatalogueService()


@pytest.fixture
def reader():
    return Reader()
