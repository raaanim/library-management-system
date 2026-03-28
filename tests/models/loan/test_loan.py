"""Tests for the Loan domain model getters, active status, and fine
calculation."""

from datetime import date, timedelta

from src.models.book.book import Book
from src.models.loan.loan import Loan
from src.models.member.member import Member, MemberData


def make_member():
    """Return a default Member instance for use in loan tests."""
    return Member(MemberData(id=1, username="alice", email="a@test.com", password="pw"))


def make_book():
    """Return a default Book instance for use in loan tests."""
    return Book(id=1, title="Dune", authors=["Herbert"], languages=["eng"])


def make_loan(**kwargs):
    """Return a Loan instance with default values overridden by kwargs."""
    today = date.today()
    defaults = {
        "id": 1,
        "member": make_member(),
        "book": make_book(),
        "loan_date": today,
        "due_date": today + timedelta(days=30),
        "return_date": None,
        "fine": 0.0,
    }
    defaults.update(kwargs)
    return Loan(**defaults)


class TestLoanGetters:
    """Tests for Loan attribute accessors."""

    def test_get_id(self):
        """Test that the id attribute returns the correct loan id."""
        assert make_loan(id=5).id == 5

    def test_get_member(self):
        """Test that the member attribute returns the associated member."""
        assert make_loan().member.get_username() == "alice"

    def test_get_book(self):
        """Test that the book attribute returns the associated book."""
        assert make_loan().book.get_title() == "Dune"

    def test_get_loan_date(self):
        """Test that loan_date is stored and returned correctly."""
        today = date.today()
        assert make_loan(loan_date=today).loan_date == today

    def test_get_due_date(self):
        """Test that due_date is stored and returned correctly."""
        due = date.today() + timedelta(days=30)
        assert make_loan(due_date=due).due_date == due

    def test_get_return_date_none(self):
        """Test that return_date defaults to None for an active loan."""
        assert make_loan().return_date is None

    def test_get_fine_default(self):
        """Test that fine defaults to 0.0 for a new loan."""
        assert make_loan().fine == 0.0


class TestLoanIsActive:
    """Tests for Loan.is_overdue status checking."""

    def test_active_when_no_return(self):
        """Test that a loan not yet due is not overdue."""
        assert make_loan(return_date=None).is_overdue() is False

    def test_overdue_when_past_due(self):
        """Test that a loan past its due date is overdue."""
        today = date.today()
        loan = make_loan(due_date=today - timedelta(days=5))
        assert loan.is_overdue() is True


class TestLoanCalculateFine:
    """Tests for Loan.calculate_fine fine computation."""

    def test_no_fine_when_on_time(self):
        """Test that no fine is calculated when the loan is not overdue."""
        today = date.today()
        loan = make_loan(due_date=today + timedelta(days=5))
        assert loan.calculate_fine() == 0.0

    def test_fine_when_overdue(self):
        """Test that a fine is calculated for overdue days."""
        today = date.today()
        loan = make_loan(due_date=today - timedelta(days=10))
        assert loan.calculate_fine() == 10.0

    def test_no_fine_on_due_date(self):
        """Test that no fine is calculated when returned exactly on the due
        date."""
        today = date.today()
        loan = make_loan(due_date=today)
        assert loan.calculate_fine() == 0.0

    def test_str_contains_info(self):
        """Test that str(loan) includes member and book information."""
        s = str(make_loan())
        assert "alice" in s
        assert "Dune" in s
