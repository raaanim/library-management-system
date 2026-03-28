"""Blueprint for public routes: homepage, search, book and edition detail."""

import re
from concurrent.futures import ThreadPoolExecutor

from flask import Blueprint, abort, redirect, render_template, request, url_for

from src.models.book.book_model import BookModel
from src.services.catalogue_service import catalogue_service
from src.services.reader import Reader

main = Blueprint("main", __name__)
reader = Reader()


@main.route("/")
def index():
    """Render the homepage with a random selection of books from the
    catalogue."""
    books = catalogue_service.get_random_books()
    return render_template("home/index.html", books=books)


@main.route("/search")
def search():
    """Search OpenLibrary for books by title or author and render results."""
    q = request.args.get("q", "").strip()
    if not q:
        return redirect(url_for("main.index"))
    by = request.args.get("by", "title")
    if by not in ("title", "author"):
        by = "title"
    results = reader.search(q, by=by)
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {
            r["work_id"]: executor.submit(reader.get_editions_by_language, r["work_id"])
            for r in results
        }
    for r in results:
        r["ita_edition"] = futures[r["work_id"]].result().get("ita")
    return render_template("home/search.html", results=results, query=q, by=by)


def _enrich_from_local(work_id: str, work: dict) -> None:
    """Enrich a work dict with local DB data (authors, year) when available."""
    local = BookModel.query.filter_by(work_id=work_id).first()
    if local:
        work["authors"] = local.authors
        work["first_publish_year"] = local.first_publish_year
    else:
        work["authors"] = ""
        match = re.search(r"\d{4}", work.get("first_publish_date") or "")
        work["first_publish_year"] = int(match.group()) if match else None


@main.route("/book/<work_id>")
def book_detail(work_id: str):
    """Render the detail page for a work with available editions by
    language."""
    work = reader.get_work(work_id)
    if not work:
        abort(404)
    _enrich_from_local(work_id, work)
    editions = reader.get_editions_by_language(work_id)
    return render_template(
        "home/book_detail.html", work=work, work_id=work_id, editions=editions
    )


@main.route("/book/edition/<edition_id>")
def edition_detail(edition_id: str):
    """Render the detail page for a specific book edition."""
    edition = reader.get_edition(edition_id)
    if not edition:
        abort(404)
    work = None
    if edition.get("work_id"):
        work = reader.get_work(edition["work_id"])
        if work:
            _enrich_from_local(edition["work_id"], work)
    return render_template("home/edition_detail.html", edition=edition, work=work)