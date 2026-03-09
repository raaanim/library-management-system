class Catalogue:
    _instance = None  # type: ignore

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_bookList"):
            self._bookList = []

    def get_bookList(self):
        return self._bookList

    def set_bookList(self, bookList):
        self._bookList = bookList

    def add_book(self, book):
        self._bookList.append(book)

    def remove_book(self, book):
        if book in self._bookList:
            self._bookList.remove(book)
        else:
            print("Book not found.")

    def search_by_title(self, title: str) -> list:
        results = [book for book in self._bookList if book.get_title() == title]
        if not results:
            print("Book not found.")
        return results

    def search_by_author(self, author: str) -> list:
        results = [book for book in self._bookList if book.get_author() == author]
        if not results:
            print("Book not found.")
        return results

    def search_by_language(self, language: str) -> list:
        results = [book for book in self._bookList if book.get_language() == language]
        if not results:
            print("Book not found.")
        return results

    def __str__(self):
        return f"Available books: {[str(book) for book in self._bookList]}"
