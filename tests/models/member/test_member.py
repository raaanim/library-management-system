"""Tests for the Member domain model getters, setters, and loan management."""

import pytest

from src.models.member.member import Member, MemberData


def make_member(**kwargs):
    """Return a Member instance with default values overridden by kwargs."""
    defaults = {
        "id": 1,
        "username": "alice",
        "email": "alice@test.com",
        "password": "hashed",
        "address": "",
    }
    defaults.update(kwargs)
    return Member(MemberData(**defaults))


class TestMemberGetters:
    """Tests for Member getter methods."""

    def test_get_id(self):
        """Test that get_id returns the correct member id."""
        assert make_member(id=5).get_id() == 5

    def test_get_username(self):
        """Test that get_username returns the correct username."""
        assert make_member().get_username() == "alice"

    def test_get_email(self):
        """Test that get_email returns the correct email address."""
        assert make_member().get_email() == "alice@test.com"

    def test_get_password(self):
        """Test that get_password returns the stored password hash."""
        assert make_member().get_password() == "hashed"

    def test_get_address(self):
        """Test that get_address returns the correct address."""
        assert make_member(address="Via Garibaldi 5").get_address() == "Via Garibaldi 5"

    def test_get_active_loans_empty(self):
        """Test that a new member starts with no active loans."""
        assert not make_member().get_active_loans()

    def test_get_active_loans_defensive_copy(self):
        """Test that get_active_loans returns a defensive copy."""
        m = make_member()
        m.get_active_loans().append("fake")
        assert not m.get_active_loans()


class TestMemberSetters:
    """Tests for Member setter methods."""

    def test_set_username(self):
        """Test that set_username updates the username."""
        m = make_member()
        m.set_username("bob")
        assert m.get_username() == "bob"

    def test_set_email(self):
        """Test that set_email updates the email address."""
        m = make_member()
        m.set_email("bob@test.com")
        assert m.get_email() == "bob@test.com"

    def test_set_password(self):
        """Test that set_password updates the password."""
        m = make_member()
        m.set_password("newhash")
        assert m.get_password() == "newhash"

    def test_set_address(self):
        """Test that set_address updates the address."""
        m = make_member()
        m.set_address("Via Roma 1")
        assert m.get_address() == "Via Roma 1"


class TestMemberCanBorrow:
    """Tests for the Member.can_borrow borrowing limit logic."""

    def test_can_borrow_initially(self):
        """Test that a new member with no loans can borrow."""
        assert make_member().can_borrow()

    def test_cannot_borrow_after_three(self):
        """Test that a member with three active loans cannot borrow more."""
        m = make_member()
        for i in range(3):
            m.add_active_loan(f"loan{i}")
        assert not m.can_borrow()

    def test_str_contains_username(self):
        """Test that str(member) includes the username."""
        s = str(make_member())
        assert "alice" in s


class TestMemberAddRemoveLoan:
    """Tests for adding and removing active loans on a Member."""

    def test_add_active_loan(self):
        """Test that add_active_loan increases the active loan count."""
        m = make_member()
        m.add_active_loan("loan1")
        assert len(m.get_active_loans()) == 1

    def test_add_raises_at_limit(self):
        """Test that adding a loan beyond the limit raises ValueError."""
        m = make_member()
        for i in range(3):
            m.add_active_loan(f"loan{i}")
        with pytest.raises(ValueError):
            m.add_active_loan("loan4")

    def test_remove_active_loan_success(self):
        """Test that remove_active_loan correctly removes an existing loan."""
        m = make_member()
        m.add_active_loan("loan1")
        m.remove_active_loan("loan1")
        assert not m.get_active_loans()

    def test_remove_active_loan_raises_if_not_found(self):
        """Test that removing a non-existent loan raises ValueError."""
        m = make_member()
        with pytest.raises(ValueError):
            m.remove_active_loan("ghost")
