from requests import get
from requests.exceptions import ConnectionError, HTTPError, Timeout

BASE_URL = "https://openlibrary.org/"
FIELDS = "key,title,author_name,cover_i,first_publish_year"


class Reader:
    """
    Client per le API di OpenLibrary.
    Permette di ricercare libri, edizioni specifiche per lingua e scaricare copertine/metadati.
    """

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def search(self, query: str, by: str = "title", limit: int = 20) -> list[dict]:
        params: dict[str, str | int] = {
            by: query,
            "limit": limit,
            "fields": FIELDS,
        }
        try:
            response = get(BASE_URL + "search.json", params=params, timeout=10)
            data = response.json()
        except (Timeout, ConnectionError, HTTPError):
            # In caso di errore di rete restituiamo una lista vuota per evitare il crash del chiamante.
            return []

        results = []
        for doc in data.get("docs", []):
            work_id = doc.get("key", "").replace("/works/", "")
            cover_i = doc.get("cover_i")
            results.append(
                {
                    "work_id": work_id,
                    "title": doc.get("title"),
                    "authors": doc.get("author_name", []),
                    "first_publish_year": doc.get("first_publish_year"),
                    "cover_url": (
                        f"https://covers.openlibrary.org/b/id/{cover_i}-M.jpg"
                        if cover_i
                        else None
                    ),
                }
            )
        return results

    def get_editions_by_language(self, work_id: str) -> dict[str, str]:
        try:
            response = get(
                BASE_URL + f"works/{work_id}/editions.json",
                params={"limit": 50},
                timeout=10,
            )
            data = response.json()
        except (Timeout, ConnectionError, HTTPError):
            # In caso di errore di rete restituiamo un dizionario vuoto per evitare il crash del chiamante.
            return {}

        result = {}
        for entry in data.get("entries", []):
            langs = entry.get("languages", [])
            if not langs:
                continue
            lang_code = langs[0]["key"].split("/")[-1]
            edition_id = entry["key"].replace("/books/", "")
            if lang_code not in result:
                result[lang_code] = edition_id
        return result

    def get_edition(self, edition_id: str) -> dict | None:
        try:
            response = get(BASE_URL + f"books/{edition_id}.json", timeout=10)
        except (Timeout, ConnectionError, HTTPError):
            # In caso di errore di rete restituiamo None per evitare il crash del chiamante.
            return None

        if response.status_code != 200:
            return None

        data = response.json()
        cover_id = data.get("covers", [None])[0]

        langs = data.get("languages", [])
        lang = langs[0].get("key", "").split("/")[-1] if langs else "unknown"

        work_id = None
        works = data.get("works", [])
        if works:
            work_id = works[0]["key"].replace("/works/", "")

        return {
            "edition_id": edition_id,
            "work_id": work_id,
            "title": data.get("title"),
            "language": lang,
            "publishers": data.get("publishers", []),
            "publish_date": data.get("publish_date"),
            "isbn_13": data.get("isbn_13", [None])[0],
            "isbn_10": data.get("isbn_10", [None])[0],
            "number_of_pages": data.get("number_of_pages"),
            "cover_url_large": (
                f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
                if cover_id
                else None
            ),
        }

    def get_work(self, work_id: str) -> dict | None:
        response = get(BASE_URL + f"works/{work_id}.json", timeout=10)
        if response.status_code != 200:
            return None
        data = response.json()

        description = data.get("description")
        if isinstance(description, dict):
            description = description.get("value")

        cover_id = data.get("covers", [None])[0]

        return {
            "title": data.get("title"),
            "description": description,
            "subjects": data.get("subjects", [])[:8],
            "first_publish_date": data.get("first_publish_date"),
            "cover_url_large": (
                f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
                if cover_id
                else None
            ),
        }
