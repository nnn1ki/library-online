from enum import Enum
from aiohttp import web

from library_service.opac.api.announces import OpacAnnounce
from library_service.opac.api.book import OpacBook, OpacBookExemplar, OpacBookInfo
from library_service.opac.api.databases import OpacDatabase
from library_service.opac.api.scenarios import OpacScenario

PORT = 3740

DATABASES: list[OpacDatabase] = [OpacDatabase("ISTU", True), OpacDatabase("NTD", True), OpacDatabase("ZIMA", True)]
SCENARIOS: list[OpacScenario] = [
    OpacScenario("A=", "author"),
    OpacScenario("T=", "title"),
    OpacScenario("IN=", "exemplar id"),
]


class BookId(Enum):
    ISTU_AAAA_XXXX = "ISTU_1"
    ISTU_BBBB_YYYY = "ISTU_2"
    ISTU_CCCC_ZZZZ = "ISTU_3"
    NTD_AAAA_XXXX = "NTD_1"
    NTD_BBBB_AAA_YYYY = "NTD_2"
    ZIMA_AAAA_XXXX = "ZIMA_1"
    ZIMA_BBBB_XXXX = "ZIMA_2"


BOOKS: list[OpacBook] = [
    OpacBook(
        BookId.ISTU_AAAA_XXXX.value,
        "",
        OpacBookInfo(["AAAA"], [], ["XXXX"], [], ["eng"], [], [], [], [], []),
        True,
        2025,
        [OpacBookExemplar("1234", 1, "ok")],
    ),
    OpacBook(
        BookId.ISTU_BBBB_YYYY.value,
        "",
        OpacBookInfo(["BBBB"], [], ["YYYY"], [], ["eng"], [], [], [], [], []),
        True,
        2025,
        [OpacBookExemplar("1235", 1, "ok")],
    ),
    OpacBook(
        BookId.ISTU_CCCC_ZZZZ.value,
        "",
        OpacBookInfo(["CCCC"], [], ["ZZZZ"], [], ["eng"], [], [], [], [], []),
        True,
        2025,
        [OpacBookExemplar("1236", 1, "ok")],
    ),
    OpacBook(
        BookId.NTD_AAAA_XXXX.value,
        "",
        OpacBookInfo(["AAAA"], [], ["XXXX"], [], ["eng"], [], [], [], [], []),
        True,
        2025,
        [OpacBookExemplar("1234", 1, "ok")],
    ),
    OpacBook(
        BookId.NTD_BBBB_AAA_YYYY.value,
        "",
        OpacBookInfo(["BBBB", "AAA"], [], ["YYYY"], [], ["eng"], [], [], [], [], []),
        True,
        2025,
        [OpacBookExemplar("1235", 1, "ok")],
    ),
    OpacBook(
        BookId.ZIMA_AAAA_XXXX.value,
        "",
        OpacBookInfo(["AAAA"], [], ["XXXX"], [], ["eng"], [], [], [], [], []),
        True,
        2025,
        [OpacBookExemplar("1234", 1, "ok")],
    ),
    OpacBook(
        BookId.ZIMA_BBBB_XXXX.value,
        "",
        OpacBookInfo(["BBBB"], [], ["XXXX"], [], ["eng"], [], [], [], [], []),
        True,
        2025,
        [OpacBookExemplar("1235", 1, "ok")],
    ),
]

ANNOUNCES = [
    OpacAnnounce("/opac/index.html?db=ISTU&expression=IN=1235"),
    OpacAnnounce("/opac/index.html?db=ISTU&expression=IN=1236"),
]


def books_by_id(*ids: BookId) -> list[OpacBook]:
    return [book for book in BOOKS if book.id in [id.value for id in ids]]


def databases(request: web.Request):
    return web.json_response(OpacDatabase.schema().dump(DATABASES, many=True))


def scenarios(request: web.Request):
    return web.json_response(OpacScenario.schema().dump(SCENARIOS, many=True))


def announces(request: web.Request):
    return web.json_response(OpacAnnounce.schema().dump(ANNOUNCES, many=True))


def book_retrieve(request: web.Request):
    database = request.match_info["database"]
    mfn = request.match_info["mfn"]
    book_id = f"{database}_{mfn}"
    book = [book for book in BOOKS if book.id == book_id][0]
    return web.json_response(book.to_dict())


async def search(request: web.Request):
    json = await request.json()
    database: str = json["database"]
    expression: str = json["expression"]

    expression = expression.replace("(", "").replace(")", "")

    # NOTE: this is technically an incorrect type hint
    # (it's a list of lists, not a list of tuples)
    possible_books: list[tuple[OpacBook, bool, bool]] = [
        [book, False, True] for book in BOOKS if book.id.split("_")[0] == database
    ]

    # pylint: disable-next=too-many-nested-blocks
    for or_statement in expression.split("+"):
        for and_statement in or_statement.split("*"):
            if and_statement != "":
                scenario, expression = and_statement.split("=")
                for book in possible_books:
                    if scenario == "A":
                        if expression.endswith("$"):
                            book[2] &= any(author.startswith(expression[:-1]) for author in book[0].info.author)
                        else:
                            book[2] &= expression in book[0].info.author
                    elif scenario == "T":
                        if expression.endswith("$"):
                            book[2] &= any(title.startswith(expression[:-1]) for title in book[0].info.title)
                        else:
                            book[2] &= expression in book[0].info.title
                    elif scenario == "IN":
                        book[2] &= any(exemplar.number == expression for exemplar in book[0].exemplars)

        for book in possible_books:
            book[1] |= book[2]
            book[2] = True

    return web.json_response(OpacBook.schema().dump([book[0] for book in possible_books if book[1]], many=True))


def run_server():
    app = web.Application()
    app.add_routes(
        [
            web.get("/api/databases", databases),
            web.get("/api/scenarios/{database}", scenarios),
            web.get("/api/announces", announces),
            web.get("/api/books/by/mfn/{database}/{mfn}", book_retrieve),
            web.post("/api/search", search),
        ]
    )
    web.run_app(app=app, port=PORT)


if __name__ == "__main__":
    run_server()
