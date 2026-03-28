"""Tests for the LoanModel ORM class serialisation and update methods."""

from datetime import date


class TestLoanModelToDict:
    """Tests for LoanModel.to_dict serialisation."""

    def test_to_dict_keys(self, loan):
        """Test that to_dict includes all expected loan keys."""
        d = loan.to_dict()
        assert "id" in d
        assert "member_id" in d
        assert "book_id" in d
        assert "loan_date" in d
        assert "due_date" in d
        assert "return_date" in d
        assert "fine" in d

    def test_to_dict_values(self, loan, member, book):
        """Test that to_dict returns correct member_id, book_id, and
        return_date."""
        d = loan.to_dict()
        assert d["member_id"] == member.id
        assert d["book_id"] == book.id
        assert d["return_date"] is None


class TestLoanModelUpdate:
    """Tests for LoanModel.update method."""

    def test_update_fine(self, loan):
        """Test that update correctly changes the fine amount."""
        loan.update(fine=5.0)
        assert loan.fine == 5.0

    def test_update_return_date(self, loan):
        """Test that update correctly sets the return date."""
        today = date.today()
        loan.update(return_date=today)
        assert loan.return_date == today

    def test_update_ignores_unknown_keys(self, loan):
        """Test that update silently ignores unknown field names."""
        loan.update(nonexistent="value")

    def test_update_member_id_ignored(self, loan, member):
        """Test that update does not overwrite the member_id field."""
        loan.update(member_id=999)
        assert loan.member_id == member.id
