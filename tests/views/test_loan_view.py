from datetime import date, timedelta

from src.models.book.book_model import BookModel
from src.models.loan.loan_model import LoanModel
from src.models.member.member_model import MemberModel


def test_loans_requires_login(client):
    r = client.get("/member/loans")
    assert r.status_code == 302


def test_loans_page_authenticated(logged_client):
    r = logged_client.get("/member/loans")
    assert r.status_code == 200


def test_loans_page_shows_active_and_history(logged_client, member, book, db):
    today = date.today()
    active = LoanModel(
        member_id=member.id,
        book_id=book.id,
        loan_date=today,
        due_date=today + timedelta(days=30),
    )
    returned = LoanModel(
        member_id=member.id,
        book_id=book.id,
        loan_date=today - timedelta(days=40),
        due_date=today - timedelta(days=10),
        return_date=today - timedelta(days=5),
    )
    db.session.add_all([active, returned])
    db.session.commit()
    r = logged_client.get("/member/loans")
    assert r.status_code == 200
    assert book.title.encode() in r.data


def test_borrow_requires_login(client, book_data):
    r = client.post("/loan/borrow", data=book_data)
    assert r.status_code == 302


def test_borrow_creates_loan(logged_client, member, book_data):
    r = logged_client.post("/loan/borrow", data=book_data, follow_redirects=True)
    assert r.status_code == 200
    loans = LoanModel.query.filter_by(member_id=member.id).all()
    assert len(loans) == 1


def test_borrow_existing_book(logged_client, book_data):
    r = logged_client.post("/loan/borrow", data=book_data, follow_redirects=True)
    assert r.status_code == 200


def test_borrow_limit_reached(logged_client, db, member, book, book_data):
    today = date.today()
    for _ in range(3):
        loan = LoanModel(
            member_id=member.id,
            book_id=book.id,
            loan_date=today,
            due_date=today + timedelta(days=30),
        )
        db.session.add(loan)
    db.session.commit()
    r = logged_client.post("/loan/borrow", data=book_data, follow_redirects=True)
    assert r.status_code == 200
    assert LoanModel.query.filter_by(member_id=member.id).count() == 3


def test_return_requires_login(client, book, member, db):
    today = date.today()
    loan = LoanModel(
        member_id=member.id,
        book_id=book.id,
        loan_date=today,
        due_date=today + timedelta(days=30),
    )
    db.session.add(loan)
    db.session.commit()
    r = client.post(f"/loan/return/{loan.id}")
    assert r.status_code == 302


def test_return_on_time(logged_client, member, book, db):
    today = date.today()
    loan = LoanModel(
        member_id=member.id,
        book_id=book.id,
        loan_date=today - timedelta(days=5),
        due_date=today + timedelta(days=25),
    )
    db.session.add(loan)
    db.session.commit()
    r = logged_client.post(f"/loan/return/{loan.id}", follow_redirects=True)
    assert r.status_code == 200
    db.session.refresh(loan)
    assert loan.return_date == today
    assert loan.fine == 0.0


def test_return_overdue_calculates_fine(logged_client, member, book, db):
    today = date.today()
    loan = LoanModel(
        member_id=member.id,
        book_id=book.id,
        loan_date=today - timedelta(days=40),
        due_date=today - timedelta(days=10),
    )
    db.session.add(loan)
    db.session.commit()
    r = logged_client.post(f"/loan/return/{loan.id}", follow_redirects=True)
    assert r.status_code == 200
    db.session.refresh(loan)
    assert loan.fine == 10.0


def test_return_wrong_member_404(logged_client, db):
    other = MemberModel(username="bob", email="bob@test.com", password="pw")
    db.session.add(other)
    db.session.flush()
    other_book = BookModel(work_id="OL99W", title="X", authors="A", languages="eng")
    db.session.add(other_book)
    db.session.flush()
    today = date.today()
    loan = LoanModel(
        member_id=other.id,
        book_id=other_book.id,
        loan_date=today,
        due_date=today + timedelta(days=30),
    )
    db.session.add(loan)
    db.session.commit()
    r = logged_client.post(f"/loan/return/{loan.id}")
    assert r.status_code == 404
