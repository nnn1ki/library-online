from aiohttp import ClientSession

from library_service.opac.api.book import opac_book_retrieve, opac_search
from library_service.opac.api.databases import opac_databases
from library_service.opac.api.scenarios import opac_scenarios
from library_service.opac.api.announces import opac_announces_list
from library_service.tests import opac_mock


async def test_databases(client_session: ClientSession):
    assert await opac_databases(client_session) == opac_mock.DATABASES


async def test_scenarios(client_session: ClientSession):
    assert await opac_scenarios(client_session, "ISTU") == opac_mock.SCENARIOS


async def test_announces(client_session: ClientSession):
    assert await opac_announces_list(client_session) == opac_mock.ANNOUNCES


async def test_book_retrieve(client_session: ClientSession):
    for book in opac_mock.BOOKS:
        db, mfn = book.id.split("_")
        assert await opac_book_retrieve(client_session, db, int(mfn)) == book


async def test_search_exemplar(client_session: ClientSession):
    expression = "IN=1236"
    books = [
        book
        for book in opac_mock.BOOKS
        if book.id.split("_")[0] == "ISTU"
        if any(exemplar.number == "1236" for exemplar in book.exemplars)
    ]

    assert len(books) == 1
    assert await opac_search(client_session, "ISTU", expression) == books


async def test_search_all(client_session: ClientSession):
    expression = "T=$"
    books = [book for book in opac_mock.BOOKS if book.id.split("_")[0] == "ISTU"]

    assert len(books) == 3
    assert await opac_search(client_session, "ISTU", expression) == books


async def test_search_part(client_session: ClientSession):
    expression = "A=AAA$"
    books = [
        book
        for book in opac_mock.BOOKS
        if book.id.split("_")[0] == "NTD"
        if any(author.startswith("AAA") for author in book.info.author)
    ]

    assert len(books) == 2
    assert await opac_search(client_session, "NTD", expression) == books


async def test_search_and(client_session: ClientSession):
    expression = "A=AAAA*T=XXXX"
    books = [
        book
        for book in opac_mock.BOOKS
        if book.id.split("_")[0] == "ISTU"
        if "AAAA" in book.info.author and "XXXX" in book.info.title
    ]

    assert len(books) == 1
    assert await opac_search(client_session, "ISTU", expression) == books


async def test_search_and_none(client_session: ClientSession):
    expression = "A=AAAA*T=YYYY"
    books = [
        book
        for book in opac_mock.BOOKS
        if book.id.split("_")[0] == "ISTU"
        if "AAAA" in book.info.author and "YYYY" in book.info.title
    ]

    assert len(books) == 0
    assert await opac_search(client_session, "ISTU", expression) == books


async def test_search_or(client_session: ClientSession):
    expression = "A=AAAA+T=YYYY"
    books = [
        book
        for book in opac_mock.BOOKS
        if book.id.split("_")[0] == "ISTU"
        if "AAAA" in book.info.author or "YYYY" in book.info.title
    ]

    assert len(books) == 2
    assert await opac_search(client_session, "ISTU", expression) == books


async def test_search_and_or(client_session: ClientSession):
    expression = "A=AAAA*T=XXXX+A=BBBB*T=YYYY"
    books = [
        book
        for book in opac_mock.BOOKS
        if book.id.split("_")[0] == "NTD"
        if "AAAA" in book.info.author
        and "XXXX" in book.info.title
        or "BBBB" in book.info.author
        and "YYYY" in book.info.title
    ]

    assert len(books) == 2
    assert await opac_search(client_session, "NTD", expression) == books
