from dataclasses import dataclass
from typing import Iterable
from dataclasses_json import dataclass_json
from library_service.models.catalog import Library, LibraryDatabase
from library_service.irbis.api.search import irbis_search

@dataclass_json
@dataclass
class BookLink:
    url: str
    description: str

@dataclass_json
@dataclass
class Book:
    id: str
    description: str
    year: int
    cover: str | None
    links: list[BookLink]
    library: int
    copies: int
    can_be_ordered: bool

def books_list(libraries: Iterable[Library], name: str | None, author: str | None) -> list[Book]:
    queries = [
        f"T={name}" if name is not None else None,
        f"A={author}" if author is not None else None
    ]
    queries = [q for q in queries if q is not None]

    query = "&".join(queries) + "$"
    
    result = []

    for library in libraries:
        databases: Iterable[LibraryDatabase] = library.databases.all()
        for db in databases:
            search_result = irbis_search(db.database, query)
            result += [Book(
                book.id,
                book.description,
                book.year,
                book.cover,
                [BookLink(link.url, link.description) for link in (book.links or [])],
                library.id,
                len(book.exemplars),
                book.order
            ) for book in search_result]

    return result