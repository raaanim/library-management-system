"""Fixtures for wishlist model tests providing a default wishlist instance."""

import pytest

from src.models.wishlist.wishlist_model import WishlistModel


@pytest.fixture
def wishlist(request):
    """Retrieve the wishlist associated with the default member."""
    member_obj = request.getfixturevalue("member")
    return WishlistModel.query.filter_by(member_id=member_obj.id).first()
