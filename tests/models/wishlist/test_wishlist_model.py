"""Tests for the WishlistModel ORM class serialisation and book
relationship."""


class TestWishlistModelToDict:
    """Tests for WishlistModel.to_dict serialisation."""

    def test_to_dict_keys(self, wishlist):
        """Test that to_dict includes id and member_id keys."""
        d = wishlist.to_dict()
        assert "id" in d
        assert "member_id" in d

    def test_to_dict_values(self, wishlist, member):
        """Test that to_dict returns the correct member_id."""
        assert wishlist.to_dict()["member_id"] == member.id


class TestWishlistModelUpdate:
    """Tests for WishlistModel.update method and books relationship."""

    def test_update_member_id(self, wishlist):
        """Test that update with member_id does not raise an error."""
        wishlist.update(member_id=999)

    def test_books_relationship(self, wishlist, book, db):
        """Test that a book can be added to the wishlist via the
        relationship."""
        wishlist.books.append(book)
        db.session.commit()
        assert book in wishlist.books
