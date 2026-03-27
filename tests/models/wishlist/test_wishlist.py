"""Tests for the Wishlist domain model getters and add/remove book
operations."""

from src.models.book.book import Book
from src.models.member.member import Member, MemberData
from src.models.wishlist.wishlist import Wishlist


def make_member():
    """Return a default Member instance for use in wishlist tests."""
    return Member(MemberData(id=1, username="alice", email="a@test.com", password="pw"))


def make_book(book_id=1):
    """Return a Book instance with the given id."""
    return Book(id=book_id, title=f"Book {book_id}")


class TestWishlistGetters:
    """Tests for Wishlist getter methods."""

    def test_get_member(self):
        """Test that get_member returns the associated member."""
        m = make_member()
        w = Wishlist(member=m)
        assert w.get_member() == m

    def test_get_books_initially_empty(self):
        """Test that a new wishlist has no books."""
        assert not Wishlist(member=make_member()).get_books()

    def test_get_books_defensive_copy(self):
        """Test that get_books returns a defensive copy."""
        w = Wishlist(member=make_member())
        w.get_books().append("fake")
        assert not w.get_books()


class TestWishlistAddRemove:
    """Tests for adding and removing books from a Wishlist."""

    def test_add_book(self):
        """Test that add_book places a book into the wishlist."""
        w = Wishlist(member=make_member())
        b = make_book()
        w.add_book(b)
        assert b in w.get_books()

    def test_add_duplicate_ignored(self):
        """Test that adding the same book twice keeps only one entry."""
        w = Wishlist(member=make_member())
        b = make_book()
        w.add_book(b)
        w.add_book(b)
        assert len(w.get_books()) == 1

    def test_remove_book(self):
        """Test that remove_book correctly removes the book from the
        wishlist."""
        w = Wishlist(member=make_member())
        b = make_book()
        w.add_book(b)
        w.remove_book(b)
        assert not w.get_books()

    def test_remove_non_existing_no_error(self):
        """Test that removing a book not in the wishlist does not raise an
        error."""
        w = Wishlist(member=make_member())
        w.remove_book(make_book(99))
