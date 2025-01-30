from dataclasses import dataclass
from typing import Iterable
from library_service.opac.api.announces import opac_announces_list
from library_service.models.catalog import Library, LibraryDatabase
from library_service.opac.api.book import OpacBook, opac_book_retrieve, opac_search

@dataclass
class BookLink:
    url: str
    description: str

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

    def __init__(self, book: OpacBook, library: int):
        self.id = book.id.replace("/", "_")
        self.description = book.description # TODO: opac api возвращает description в отформатированном формате с html тегами, и содержит в себе название книги, автора и т.д. Возможно, стоит это распарсить
        self.year = book.year
        self.cover = book.cover # TODO: тут возвращается ссылка на метод на их сервере ("/api/cover?file=..."). Нужно возвращать на наш (будет проксирование) или приводить к полной ссылке
        self.links = [BookLink(link.url, link.description) for link in (book.links or [])]
        self.library = library
        self.copies = len(book.exemplars)
        self.can_be_ordered = book.order

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

def book_retrieve(id: str) -> Book:
    database, mfn = id.split("_")
    library = LibraryDatabase.objects.filter(database=database).first().library
    book = opac_book_retrieve(database, mfn)

    return Book(book, library.id)