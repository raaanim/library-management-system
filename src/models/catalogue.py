# Classe Singleton "Catalogue" per gestire aggregazione e ricerche di libri nel db.
# Gestisce il catalogo dei libri.


class Catalogue:
    _instance = None  # type: ignore

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__bookList = []
        return cls._instance

    def get_bookList(self):
        return self.__bookList

    def set_bookList(self, bookList):
        self.__bookList = bookList

    def add_book(self, book):
        self.__bookList.append(book)

    def remove_book(self, book):
        if book in self.__bookList:
            self.__bookList.remove(book)
        else:
            print("Book not found.")

    def search_by_title(self, title: str) -> list:
        results = [book for book in self.__bookList if book.get_title() == title]
        if not results:
            print("Book not found.")
        return results

    def search_by_author(self, author: str) -> list:
        results = [book for book in self.__bookList if book.get_author() == author]
        if not results:
            print("Book not found.")
        return results

    def search_by_language(self, language: str) -> list:
        results = [book for book in self.__bookList if book.get_language() == language]
        if not results:
            print("Book not found.")
        return results

    def __str__(self):
        return f"Available books: {[str(book) for book in self.__bookList]}"


# def main():
#     catalogue = Catalogue()
#     catalogue.add_book("Book1")

#     catalogue2 = Catalogue()
#     catalogue2.add_book("Book2")

#     print(f"List: {catalogue.get_bookList()}")
#     print(catalogue is catalogue2)  # True


# if __name__ == "__main__":
#     main()
