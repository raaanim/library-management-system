from src.models.member.member_model import MemberModel
from src.models.wishlist.wishlist_model import WishlistModel


def test_get_register_page(client):
    r = client.get("/auth/register")
    assert r.status_code == 200


def test_register_success(client):
    r = client.post(
        "/auth/register",
        data={
            "username": "bob",
            "email": "bob@test.com",
            "password": "secret123",
        },
        follow_redirects=True,
    )
    assert r.status_code == 200
    m = MemberModel.query.filter_by(email="bob@test.com").first()
    assert m is not None
    assert WishlistModel.query.filter_by(member_id=m.id).first() is not None


def test_register_missing_fields(client):
    r = client.post(
        "/auth/register",
        data={"username": "", "email": "x@test.com", "password": ""},
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert MemberModel.query.filter_by(email="x@test.com").first() is None


def test_register_duplicate_email(client, member):
    r = client.post(
        "/auth/register",
        data={
            "username": "other",
            "email": member.email,
            "password": "pw",
        },
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert MemberModel.query.filter_by(email=member.email).count() == 1


def test_get_login_page(client):
    r = client.get("/auth/login")
    assert r.status_code == 200


def test_login_success(client, member):
    r = client.post(
        "/auth/login",
        data={"email": member.email, "password": "password123"},
        follow_redirects=True,
    )
    assert r.status_code == 200


def test_login_wrong_password(client, member):
    r = client.post(
        "/auth/login",
        data={"email": member.email, "password": "wrongpw"},
        follow_redirects=True,
    )
    assert r.status_code == 200


def test_login_unknown_email(client):
    r = client.post(
        "/auth/login",
        data={"email": "nobody@test.com", "password": "pw"},
        follow_redirects=True,
    )
    assert r.status_code == 200


def test_logout_clears_session(client, member):
    client.post(
        "/auth/login",
        data={"email": member.email, "password": "password123"},
    )
    r = client.post("/auth/logout", follow_redirects=True)
    assert r.status_code == 200
    with client.session_transaction() as sess:
        assert "member_id" not in sess
