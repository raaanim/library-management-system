import re

from requests import get
from requests.exceptions import ConnectionError, HTTPError, Timeout


class Reader:
    URL = "https://openlibrary.org/"
    __instance = None

    # Rendo la classe reader un singleton
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    # Metodo per la richiesta HTTP
    def __http_request(self, path_variables: str) -> dict:
        try:
            # Per Open Library, se path_variables inizia con 'search.json', usiamo i parametri
            # Altrimenti assumiamo sia un percorso diretto come 'works/OLID.json'
            response = get(self.URL + path_variables, timeout=10)
            response.raise_for_status()
            return response.json()
        except Timeout:
            return {"error": "Request timed out"}
        except ConnectionError:
            return {"error": "Connection error"}
        except HTTPError as e:
            return {"error": "HTTP error", "status_code": e.response.status_code}

    # Metodo per ottenere i dati del libro
    def get_data(self, path_variables: str) -> dict:
        if not path_variables:
            return {"error": "No path variables provided"}

        data = self.__http_request(path_variables)
        if "error" in data:
            return {"error": data["error"], "status_code": data.get("status_code")}

        # Gestione differenziata se è una ricerca o un singolo lavoro
        if "docs" in data:
            # È un risultato di ricerca: prendiamo il primo libro per coerenza con il pattern Pokémon
            if not data["docs"]:
                return {"error": "No books found"}
            book = data["docs"][0]
            return {
                "id": book.get("key", "").replace("/works/", ""),
                "title": book.get("title"),
                "authors": book.get("author_name", []),
                "first_publish_year": book.get("first_publish_year"),
                "languages": book.get("language", []),
                "cover_url": (
                    f"https://covers.openlibrary.org/b/id/{book.get('cover_i')}-L.jpg"
                    if book.get("cover_i")
                    else None
                ),
            }

        cover_id = data.get("covers", [None])[0]

        raw_date = str(data.get("first_publish_date", ""))

        year_match = re.search(r"\d{4}", raw_date)
        year = int(year_match.group()) if year_match else None

        return {
            "id": path_variables.replace("works/", "").replace(".json", ""),
            "title": data.get("title"),
            "first_publish_year": year,
            "cover_url": (
                f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
                if cover_id
                else None
            ),
        }
