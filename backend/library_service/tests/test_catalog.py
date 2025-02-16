from typing import Literal
from django.test import Client
import pytest

from library_service.opac.api.scenarios import OpacScenario
from library_service.tests import opac_mock
from library_service.tests.opac_mock import BookId


def get_library_id(client: Client, library: Literal["ISTU_LIB"] | Literal["ZIMA_LIB"]):
    response = client.get("/api/library/")
    json = response.json()
    return [i["id"] for i in json if i["description"] == library][0]


@pytest.mark.django_db
def test_libraries(client: Client):
    response = client.get("/api/library/")
    json = response.json()

    assert len(json) == 2

    libraries = [i["description"] for i in json]
    assert "ISTU_LIB" in libraries
    assert "ZIMA_LIB" in libraries

    for library in ["ISTU_LIB", "ZIMA_LIB"]:
        library_id = get_library_id(client, library)
        response = client.get(f"/api/library/{library_id}/")
        json = response.json()
        assert json["description"] == library


def test_scenarios(client: Client):
    response = client.get("/api/scenario/")
    json = response.json()

    assert json == OpacScenario.schema().dump(opac_mock.SCENARIOS, many=True)


@pytest.mark.django_db
def test_announcements(client: Client):
    response = client.get("/api/book/announcement/")
    json = response.json()

    assert [book["id"] for book in json] == [BookId.ISTU_BBBB_YYYY.value, BookId.ISTU_CCCC_ZZZZ.value]


@pytest.mark.django_db
def test_book_retrieve(client: Client):
    for book in opac_mock.BOOKS:
        response = client.get(f"/api/book/{book.id}/")
        json = response.json()
        assert json["id"] == book.id


@pytest.mark.django_db
def test_search_all(client: Client):
    response = client.get("/api/book/", {"expression": "T=$"})
    json = response.json()

    assert [book["id"] for book in json] == [book.id for book in opac_mock.BOOKS]


@pytest.mark.django_db
def test_search_library(client: Client):
    response = client.get("/api/book/", {"expression": "T=$", "library": get_library_id(client, "ISTU_LIB")})
    json = response.json()

    assert [book["id"] for book in json] == [
        book.id for book in opac_mock.BOOKS if book.id.startswith("ISTU") or book.id.startswith("NTD")
    ]


@pytest.mark.django_db
def test_search_and_none(client: Client):
    response = client.get("/api/book/", {"expression": "A=AAAA*T=YYYY"})
    json = response.json()
    assert json == []


@pytest.mark.django_db
def test_search_and_or(client: Client):
    response = client.get("/api/book/", {"expression": "A=AAAA*T=XXXX+A=BBBB*T=YYYY"})
    json = response.json()
    assert [book["id"] for book in json] == [
        BookId.ISTU_AAAA_XXXX.value,
        BookId.ISTU_BBBB_YYYY.value,
        BookId.NTD_AAAA_XXXX.value,
        BookId.NTD_BBBB_AAA_YYYY.value,
        BookId.ZIMA_AAAA_XXXX.value,
    ]


def test_search_no_expression(client: Client):
    response = client.get("/api/book/")
    assert response.status_code == 400
