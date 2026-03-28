"""Flask application factory and main entry point."""

import os

from flask import Flask
from flask_migrate import Migrate

from src.models.base import db
from src.models.book.book_model import BookModel
from src.models.catalogue.catalogue_model import CatalogueModel
from src.models.loan.loan_model import LoanModel
from src.models.member.member_model import MemberModel
from src.models.wishlist.wishlist_model import WishlistModel
from src.populate import populate_books
from src.views.loan_view import loan as loan_blueprint
from src.views.main_view import main as main_blueprint
from src.views.member_view import member as member_blueprint
from src.views.wishlist_view import wishlist_bp as wishlist_blueprint


def create_app(test_config: dict | None = None) -> Flask:
    """Create and configure the Flask application."""

    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
        instance_path=os.path.join(root_path, "instance"),
        instance_relative_config=True,
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "super-secret-key-for-dev"

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(main_blueprint)
    app.register_blueprint(member_blueprint)
    app.register_blueprint(loan_blueprint)
    app.register_blueprint(wishlist_blueprint)

    with app.app_context():

        _ = (BookModel, CatalogueModel, LoanModel, MemberModel, WishlistModel)
        db.create_all()

        if not CatalogueModel.query.first():
            db.session.add(CatalogueModel(name="Biblioteca"))
            db.session.commit()

        if not test_config and BookModel.query.count() == 0:
            print("Database vuoto, avvio popolamento automatico...")
            populate_books()

    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(debug=True)
