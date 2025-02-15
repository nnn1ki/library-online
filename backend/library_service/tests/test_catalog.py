from django.test import Client
import pytest

from library_service.opac.api.scenarios import OpacScenario
from library_service.tests import opac_mock
from library_service.tests.opac_mock import BookId


@pytest.mark.django_db
def test_libraries(client: Client):
    response = client.get("/api/library/")
    json = response.json()

    assert len(json) == 1
    assert json[0]["description"] == "INRTU"

    library_id = json[0]["id"]
    response = client.get(f"/api/library/{library_id}/")
    json = response.json()
    assert json["description"] == "INRTU"


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


# TODO: search tests
