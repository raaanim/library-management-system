"""Blueprint for member authentication: register, login and logout."""

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from src.models.base import db
from src.models.member.member_model import MemberModel
from src.models.wishlist.wishlist_model import WishlistModel

member = Blueprint("member", __name__, url_prefix="/auth")


@member.route("/register", methods=["GET", "POST"])
def register():
    """Handle new member registration via form submission."""
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if not username or not email or not password:
            flash("Tutti i campi sono obbligatori.", "danger")
            return redirect(url_for("member.register"))

        existing_user = MemberModel.query.filter_by(email=email).first()
        if existing_user:
            flash("L'indirizzo email è già in uso.", "danger")
            return redirect(url_for("member.register"))

        hashed_password = generate_password_hash(password)
        new_member_model = MemberModel(
            username=username, email=email, password=hashed_password
        )

        db.session.add(new_member_model)
        db.session.flush()

        wishlist = WishlistModel(member_id=new_member_model.id)
        db.session.add(wishlist)
        db.session.commit()

        flash(
            "Registrazione completata! Puoi ora effettuare il login.",
            "success",
        )
        return redirect(url_for("member.login"))

    return render_template("auth/register.html")


@member.route("/login", methods=["GET", "POST"])
def login():
    """Authenticate a member by email and password and set session."""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        member_model = MemberModel.query.filter_by(email=email).first()
        if member_model and check_password_hash(member_model.password, password):
            session["member_id"] = member_model.id
            flash("Login effettuato con successo.", "success")
            return redirect(url_for("main.index"))
        flash("Email o password errati.", "danger")

    return render_template("login.html")


@member.route("/logout", methods=["POST"])
def logout():
    """Clear the session and log the member out."""
    session.pop("member_id", None)
    flash("Logout effettuato con successo.", "info")
    return redirect(url_for("main.index"))