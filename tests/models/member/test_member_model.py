def test_to_dict_keys(member):
    d = member.to_dict()
    assert set(d.keys()) == {"id", "username", "email", "registration_date"}


def test_no_password_in_dict(member):
    assert "password" not in member.to_dict()


def test_update_username(member):
    member.update(username="bob")
    assert member.username == "bob"


def test_update_password_ignored(member):
    orig_pw = member.password
    member.update(password="newpass")
    assert member.password == orig_pw


def test_update_ignores_unknown_keys(member):
    member.update(nonexistent="value")
