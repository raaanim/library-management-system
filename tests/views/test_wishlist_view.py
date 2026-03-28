from src.models.wishlist.wishlist_model import WishlistModel


def test_wishlist_requires_login(client):
    r = client.get("/member/wishlist")
    assert r.status_code == 302


def test_wishlist_page_authenticated(logged_client):
    r = logged_client.get("/member/wishlist")
    assert r.status_code == 200


def test_wishlist_shows_books(logged_client, member, book, db):
    wishlist = WishlistModel.query.filter_by(member_id=member.id).first()
    wishlist.books.append(book)
    db.session.commit()
    r = logged_client.get("/member/wishlist")
    assert book.title.encode() in r.data


def test_add_requires_login(client, book_data):
    r = client.post("/member/wishlist/add", data=book_data)
    assert r.status_code == 302


def test_add_new_book(logged_client, member, book_data):
    r = logged_client.post(
        "/member/wishlist/add", data=book_data, follow_redirects=True
    )
    assert r.status_code == 200
    wishlist = WishlistModel.query.filter_by(member_id=member.id).first()
    assert len(wishlist.books) == 1


def test_add_existing_book_not_duplicated(logged_client, member, book, db, book_data):
    wishlist = WishlistModel.query.filter_by(member_id=member.id).first()
    wishlist.books.append(book)
    db.session.commit()
    r = logged_client.post(
        "/member/wishlist/add", data=book_data, follow_redirects=True
    )
    assert r.status_code == 200
    wishlist = WishlistModel.query.filter_by(member_id=member.id).first()
    assert len(wishlist.books) == 1


def test_remove_requires_login(client, book):
    r = client.post("/member/wishlist/remove", data={"book_id": book.id})
    assert r.status_code == 302


def test_remove_book(logged_client, member, book, db):
    wishlist = WishlistModel.query.filter_by(member_id=member.id).first()
    wishlist.books.append(book)
    db.session.commit()
    r = logged_client.post(
        "/member/wishlist/remove",
        data={"book_id": book.id},
        follow_redirects=True,
    )
    assert r.status_code == 200
    wishlist = WishlistModel.query.filter_by(member_id=member.id).first()
    assert len(wishlist.books) == 0


def test_remove_book_not_in_wishlist(logged_client, book):
    r = logged_client.post(
        "/member/wishlist/remove",
        data={"book_id": book.id},
        follow_redirects=True,
    )
    assert r.status_code == 200
