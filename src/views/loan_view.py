"""Blueprint for loan management: list, borrow and return."""

from datetime import date, timedelta

from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from src.models.base import db
from src.models.book.book import Book
from src.models.loan.loan import Loan as LoanDomain
from src.models.loan.loan_model import LoanModel
from src.models.member.member import Member, MemberData
from src.models.member.member_model import MemberModel
from src.services.catalogue_service import catalogue_service
from src.views.utils import login_required

loan = Blueprint("loan", __name__)


@loan.route("/member/loans")
@login_required
def loans():
    """Render the authenticated member's active loans and loan history."""
    member = db.session.get(MemberModel, session["member_id"])
    active = [ln for ln in member.loans if ln.return_date is None]
    history = [ln for ln in member.loans if ln.return_date is not None]
    return render_template("member/loans.html", active=active, history=history)


@loan.route("/loan/borrow", methods=["POST"])
@login_required
def borrow():
    """Create a new loan for the authenticated member if the loan limit is
    not reached."""
    member = db.session.get(MemberModel, session["member_id"])
    active_count = LoanModel.query.filter_by(
        member_id=member.id, return_date=None
    ).count()
    if active_count >= Member.MAX_ACTIVE_LOANS:
        flash("Hai raggiunto il limite massimo di 3 prestiti attivi.", "danger")
        return redirect(url_for("loan.loans"))
    book = catalogue_service.get_or_create_book(request.form)
    today = date.today()
    new_loan = LoanModel(
        member_id=member.id,
        book_id=book.id,
        loan_date=today,
        due_date=today + timedelta(days=30),
    )
    db.session.add(new_loan)
    db.session.commit()
    flash(f'Hai preso in prestito "{book.title}".', "success")
    return redirect(url_for("loan.loans"))


@loan.route("/loan/return/<int:loan_id>", methods=["POST"])
@login_required
def return_loan(loan_id: int):
    """Record a book return and calculate any overdue fine via domain logic."""
    loan_obj = db.get_or_404(LoanModel, loan_id)
    if loan_obj.member_id != session["member_id"]:
        abort(404)

    book_domain = Book(id=loan_obj.book.id, title=loan_obj.book.title)
    member_domain = Member(
        MemberData(
            id=loan_obj.member.id,
            username=loan_obj.member.username,
            email=loan_obj.member.email,
            password=loan_obj.member.password,
        )
    )
    loan_domain = LoanDomain(
        id=loan_obj.id,
        member=member_domain,
        book=book_domain,
        loan_date=loan_obj.loan_date,
        due_date=loan_obj.due_date,
        return_date=loan_obj.return_date,
        fine=loan_obj.fine,
    )
    loan_domain.close_loan(date.today())
    loan_obj.return_date = loan_domain.return_date
    loan_obj.fine = loan_domain.fine

    db.session.commit()
    flash("Libro restituito con successo.", "success")
    return redirect(url_for("loan.loans"))