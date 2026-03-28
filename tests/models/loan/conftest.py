"""Fixtures for loan model tests providing a default loan instance."""

from datetime import date, timedelta

import pytest

from src.models.loan.loan_model import LoanModel


@pytest.fixture
def loan(request):
    """Create and persist a default loan linking the default member and
    book."""
    member_obj = request.getfixturevalue("member")
    book_obj = request.getfixturevalue("book")
    database = request.getfixturevalue("db")
    today = date.today()
    loan_obj = LoanModel(
        member_id=member_obj.id,
        book_id=book_obj.id,
        loan_date=today,
        due_date=today + timedelta(days=30),
    )
    database.session.add(loan_obj)
    database.session.commit()
    return loan_obj
