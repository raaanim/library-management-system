"""Blueprint for wishlist management: view, add and remove books."""

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from src.models.base import db
from src.models.book.book_model import BookModel
from src.models.wishlist.wishlist_model import WishlistModel
from src.services.catalogue_service import catalogue_service
from src.views.utils import login_required

wishlist_bp = Blueprint("wishlist", __name__)


@wishlist_bp.route("/member/wishlist")
@login_required
def wishlist():
    """Render the authenticated member's wishlist."""
    member_id = session["member_id"]
    w = WishlistModel.query.filter_by(member_id=member_id).first()
    books = w.books if w else []
    return render_template("member/wishlist.html", books=books)


@wishlist_bp.route("/member/wishlist/add", methods=["POST"])
@login_required
def add_to_wishlist():
    """Add a book to the authenticated member's wishlist (no duplicates)."""
    member_id = session["member_id"]
    book = catalogue_service.get_or_create_book(request.form)
    w = WishlistModel.query.filter_by(member_id=member_id).first()
    if book not in w.books:
        w.books.append(book)
    db.session.commit()
    flash(f'"{book.title}" aggiunto alla wishlist.', "success")
    return redirect(url_for("wishlist.wishlist"))


@wishlist_bp.route("/member/wishlist/remove", methods=["POST"])
@login_required
def remove_from_wishlist():
    """Remove a book from the authenticated member's wishlist."""
    member_id = session["member_id"]
    book_id = request.form.get("book_id", type=int)
    book = db.session.get(BookModel, book_id)
    w = WishlistModel.query.filter_by(member_id=member_id).first()
    if book and book in w.books:
        w.books.remove(book)
    db.session.commit()
    flash("Libro rimosso dalla wishlist.", "info")
    return redirect(url_for("wishlist.wishlist"))
