"""Script per popolare manualmente il database con libri da OpenLibrary."""

import os
import sys

from src.app import create_app
from src.populate import populate_books

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


if __name__ == "__main__":
    print("Recupero libri da OpenLibrary...")
    app = create_app()
    with app.app_context():
        populate_books()
