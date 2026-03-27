"""Script per popolare manualmente il database con libri da OpenLibrary."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.app import create_app  # noqa: E402
from src.populate import populate_books  # noqa: E402

if __name__ == "__main__":
    print("Recupero libri da OpenLibrary...")
    app = create_app()
    with app.app_context():
        populate_books()
