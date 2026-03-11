from flask import Flask
from src.models.base import db
from src.views.catalogue_view import catalogue_bp
from src.views.member_view import member_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.register_blueprint(catalogue_bp)
    app.register_blueprint(member_bp)

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)