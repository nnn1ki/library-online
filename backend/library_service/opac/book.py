from dataclasses import dataclass
from typing import Iterable
from library_service.opac.api.announces import opac_announces_list
from library_service.models.catalog import Library, LibraryDatabase
from library_service.opac.api.book import OpacBook, opac_book_retrieve, opac_search

from django.conf import settings

@dataclass
class BookLink:
    url: str
    description: str | None

@dataclass
class Book:
    id: str
    library: int
    description: str
    year: int
    copies: int
    can_be_ordered: bool
    links: list[BookLink]
    author: list[str]
    collective: list[str]
    title: list[str]
    isbn: list[str]
    language: list[str]
    country: list[str]
    city: list[str]
    publisher: list[str]
    subject: list[str]
    keyword: list[str]
    cover: str | None
    brief: str | None
    created: str | None

    def __init__(self, book: OpacBook, library: int):
        self.id = book.id.replace("/", "_")
        self.library = library
        self.description = book.description
        self.year = book.year
        self.copies = len(book.exemplars) 
        self.can_be_ordered = book.order
        self.links = [BookLink(link.url, link.description) for link in (book.links or [])]
        self.author = book.info.author
        self.collective = book.info.collective
        self.title = book.info.title
        self.isbn = book.info.isbn
        self.language = book.info.language
        self.country = book.info.country
        self.city = book.info.city
        self.publisher = book.info.publisher
        self.subject = book.info.subject
        self.keyword = book.info.keyword
        self.cover = settings.OPAC_HOSTNAME + "/" + book.cover if book.cover else None # TODO: по идее, лучше проксировать
        self.brief = book.brief
        self.created = book.created

# Obtain database name and mfn id
def split_book_id(book_id: str) -> tuple[str, str]:
    return book_id.split("_")

def books_list(libraries: Iterable[Library], expression: str) -> list[Book]:
    result = []

    for library in libraries:
        databases: Iterable[LibraryDatabase] = library.databases.all()
        for db in databases:
            search_result = opac_search(db.database, expression)
            result += [Book(book, library.id) for book in search_result]

    return result

def books_announces_list() -> list[Book]:
    announces = opac_announces_list()
    
    istu_library = LibraryDatabase.objects.filter(database="ISTU").first().library # По идее, все анонсы отсылают на ISTU
    
    result = []
    for announce in announces:
        expresssion = announce.link.removeprefix("/opac/index.html?expression=") # Спс за такой удобный апи
        book = opac_search("ISTU", expresssion)[0]
        result.append(Book(book, istu_library.id))

    return result

def book_retrieve(book_id: str) -> Book:
    database, mfn = split_book_id(book_id)
    library = LibraryDatabase.objects.filter(database=database).first().library
    book = opac_book_retrieve(database, mfn)

    return Book(book, library.id)

def book_validate(book_id: str, library: Library | None = None) -> bool:
    try:
        database, _ = split_book_id(book_id)
        if library is not None and not any([database == db.database for db in library.databases.all()]):
            return False
        
        book_retrieve(book_id)
        return True
    except:
        return False