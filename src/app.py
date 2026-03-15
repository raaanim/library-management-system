from flask import Flask
from flask_migrate import Migrate

from src.models.base import db


def create_app() -> Flask:
    """
    Funzione factory per creare e configurare l'applicazione Flask.
    """
    # Inizializza l'applicazione Flask
    app = Flask(__name__)

    # Configura l'URI del database SQLite (il file verrà creato locale come library.db)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"

    # Disabilita il tracciamento delle modifiche di SQLAlchemy per risparmiare risorse
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Chiave segreta necessaria per la gestione delle sessioni (es. login, flash messages)
    app.config["SECRET_KEY"] = "super-secret-key-for-dev"

    # Collega l'istanza del database (db) all'app appena creata
    db.init_app(app)

    # Inizializza Flask-Migrate per gestire le migrazioni dello schema del database
    Migrate(app, db)

    # Nota: Le registrazioni dei Blueprint sono state temporaneamente rimosse
    # poiché i file delle viste sono attualmente solo scaffold descrittivi.

    # All'interno del contesto dell'applicazione, crea tutte le tabelle nel database
    # basandosi sui modelli definiti (se non esistono già)
    with app.app_context():
        db.create_all()

    # Ritorna l'applicazione configurata pronta per essere eseguita
    return app


if __name__ == "__main__":
    # Crea l'istanza dell'applicazione
    flask_app = create_app()

    # Avvia il server di sviluppo di Flask (debug=True permette il ricaricamento automatico ad ogni modifica)
    flask_app.run(debug=True)
