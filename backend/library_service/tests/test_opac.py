from aiohttp import ClientSession

from library_service.opac.api.book import opac_book_retrieve, opac_search
from library_service.opac.api.databases import opac_databases
from library_service.opac.api.scenarios import opac_scenarios
from library_service.opac.api.announces import opac_announces_list
from library_service.tests import opac_mock
from library_service.tests.opac_mock import BookId, books_by_id


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
    for book in [book for book in opac_mock.BOOKS if book.id.startswith("ISTU")]:
        exemplar_id = book.exemplars[0].number
        expression = f"IN={exemplar_id}"
        assert await opac_search(client_session, "ISTU", expression) == [book]


async def test_search_all(client_session: ClientSession):
    assert await opac_search(client_session, "ISTU", "T=$") == books_by_id(
        BookId.ISTU_AAAA_XXXX, BookId.ISTU_BBBB_YYYY, BookId.ISTU_CCCC_ZZZZ
    )


async def test_search_part(client_session: ClientSession):
    assert await opac_search(client_session, "NTD", "A=AAA$") == books_by_id(
        BookId.NTD_AAAA_XXXX, BookId.NTD_BBBB_AAA_YYYY
    )


async def test_search_and(client_session: ClientSession):
    assert await opac_search(client_session, "ISTU", "A=AAAA*T=XXXX") == books_by_id(BookId.ISTU_AAAA_XXXX)


async def test_search_and_none(client_session: ClientSession):
    assert await opac_search(client_session, "ISTU", "A=AAAA*T=YYYY") == []


async def test_search_or(client_session: ClientSession):
    assert await opac_search(client_session, "ISTU", "A=AAAA+T=YYYY") == books_by_id(
        BookId.ISTU_AAAA_XXXX, BookId.ISTU_BBBB_YYYY
    )


async def test_search_and_or(client_session: ClientSession):
    assert await opac_search(client_session, "NTD", "A=AAAA*T=XXXX+A=BBBB*T=YYYY") == books_by_id(
        BookId.NTD_AAAA_XXXX, BookId.NTD_BBBB_AAA_YYYY
    )
