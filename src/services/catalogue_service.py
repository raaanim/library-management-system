from src.models.book.book_model import BookModel


class CatalogueService:
    """
    Servizio core per la gestione logica dei libri nel catalogo.
    Si occupa di recuperare dati dal database o da sorgenti esterne (es. OpenLibrary).
    """

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def get_or_create_book(
        self,  # form_data: dict
    ) -> BookModel:  # pylint: disable=unused-argument
        """
        Controlla se un libro preso da OpenLibrary esiste già nel DB locale usando il work_id.
        Se esiste, lo restituisce. Altrimenti ne crea una copia in locale senza associarlo al catalogo fisico.
        """
        # pylint: disable=fixme
        # TODO: Cerca db.session per BookModel con work_id = form_data["work_id"]
        # Se c'è lo ritorna
        # Se non c'è, crea il BookModel, lo aggiunge a db.session e fa il flush/commit.
        return BookModel()

    def get_random_books(
        self,  # limit: int = 20
    ) -> list[BookModel]:  # pylint: disable=unused-argument
        """Estrae libri casuali per la Homepage."""
        # pylint: disable=fixme
        # TODO: Query randomica su BookModel ignorando OpenLibrary
        return []

    def get_book_by_id(self, book_id: int) -> BookModel | None:
        """Fetch book from local DB."""
        return BookModel.query.get(book_id)


# Singleton export
catalogue_service = CatalogueService()
