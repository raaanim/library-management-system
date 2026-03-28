"""Shared pytest fixtures for the entire test suite."""

import pytest
from sqlalchemy.pool import StaticPool
from werkzeug.security import generate_password_hash

from src.app import create_app
from src.models.base import db as _db
from src.models.book.book_model import BookModel
from src.models.member.member_model import MemberModel
from src.models.wishlist.wishlist_model import WishlistModel


@pytest.fixture(scope="session")
def app():
    """Create and configure the Flask application for the test session."""
    flask_app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_ENGINE_OPTIONS": {
                "connect_args": {"check_same_thread": False},
                "poolclass": StaticPool,
            },
            "SECRET_KEY": "test-secret",
        }
    )
    return flask_app


@pytest.fixture(autouse=True)
def clean_db(request):
    """Create all tables before each test and drop them afterwards."""
    flask_app = request.getfixturevalue("app")
    with flask_app.app_context():
        _db.create_all()
        yield
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def db(request):
    """Provide the SQLAlchemy database instance within the application
    context."""
    flask_app = request.getfixturevalue("app")
    with flask_app.app_context():
        yield _db


@pytest.fixture
def client(request):
    """Provide a Flask test client for HTTP request simulation."""
    flask_app = request.getfixturevalue("app")
    with flask_app.test_client() as c:
        yield c


@pytest.fixture
def member(request):
    """Create and persist a default member with an associated wishlist."""
    database = request.getfixturevalue("db")
    m = MemberModel(
        username="alice",
        email="alice@test.com",
        password=generate_password_hash("password123"),
    )
    database.session.add(m)
    database.session.flush()
    database.session.add(WishlistModel(member_id=m.id))
    database.session.commit()
    return m


@pytest.fixture
def book(request):
    """Create and persist a default book in the database."""
    database = request.getfixturevalue("db")
    b = BookModel(
        work_id="OL1W",
        title="Dune",
        authors="Herbert",
        languages="eng",
        first_publish_year=1965,
        cover_url="https://example.com/cover.jpg",
    )
    database.session.add(b)
    database.session.commit()
    return b


@pytest.fixture
def book_data():
    """Provide a common dictionary of book data for form submissions in
    tests."""
    return {
        "work_id": "OL1W",
        "title": "Dune",
        "authors": "Herbert",
        "languages": "eng",
        "cover_url": "",
        "first_publish_year": "1965",
    }
