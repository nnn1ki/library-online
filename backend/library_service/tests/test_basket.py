from django.test import Client
import pytest

from library_service.tests import opac_mock
from library_service.tests.opac_mock import BookId
from library_service.tests.test_auth import authorize


def get_basket_books(client: Client) -> list[str]:
    response = client.get("/api/basket/")
    return [book["id"] for book in response.json()]


def sorted_assert(left: list, right: list):
    assert sorted(left) == sorted(right)


@pytest.mark.django_db
def test_initial_basket(client: Client):
    authorize(client)
    assert get_basket_books(client) == []


@pytest.mark.django_db
def test_basket_add_remove_single(client: Client):
    authorize(client)

    client.post("/api/basket/", {"books": [BookId.ISTU_AAAA_XXXX.value]})
    assert get_basket_books(client) == [BookId.ISTU_AAAA_XXXX.value]

    client.delete(f"/api/basket/{BookId.ISTU_AAAA_XXXX.value}/")
    assert get_basket_books(client) == []

    client.post("/api/basket/", {"books": []}, content_type="application/json")
    assert get_basket_books(client) == []


@pytest.mark.django_db
def test_basket_add_multiple(client: Client):
    authorize(client)

    client.post("/api/basket/", {"books": [BookId.ISTU_AAAA_XXXX.value, BookId.ZIMA_AAAA_XXXX.value]})
    client.post("/api/basket/", {"books": [BookId.NTD_AAAA_XXXX.value]})

    sorted_assert(
        get_basket_books(client),
        [
            BookId.ISTU_AAAA_XXXX.value,
            BookId.ZIMA_AAAA_XXXX.value,
            BookId.NTD_AAAA_XXXX.value,
        ],
    )


@pytest.mark.django_db
def test_basket_add_collision(client: Client):
    authorize(client)

    client.post(
        "/api/basket/",
        {"books": [BookId.ISTU_AAAA_XXXX.value, BookId.ISTU_AAAA_XXXX.value]},
    )
    client.post(
        "/api/basket/",
        {"books": [BookId.NTD_BBBB_AAA_YYYY.value, BookId.ISTU_AAAA_XXXX.value, BookId.NTD_BBBB_AAA_YYYY.value]},
    )

    sorted_assert(get_basket_books(client), [BookId.ISTU_AAAA_XXXX.value, BookId.NTD_BBBB_AAA_YYYY.value])


@pytest.mark.django_db
def test_basket_add_invalid(client: Client):
    authorize(client)
    response = client.post("/api/basket/", {"books": ["ISU_1"]})
    assert response.status_code == 400


@pytest.mark.django_db
def test_basket_remove_invalid(client: Client):
    authorize(client)
    response = client.delete(f"/api/basket/{BookId.ISTU_AAAA_XXXX.value}/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_basket_replace(client: Client):
    authorize(client)

    client.post("/api/basket/", {"books": [BookId.NTD_AAAA_XXXX.value]})
    client.put(
        "/api/basket/replace/",
        {"books": [BookId.ISTU_AAAA_XXXX.value, BookId.ISTU_AAAA_XXXX.value, BookId.ZIMA_AAAA_XXXX.value]},
        content_type="application/json",
    )

    sorted_assert(
        get_basket_books(client),
        [
            BookId.ISTU_AAAA_XXXX.value,
            BookId.ZIMA_AAAA_XXXX.value,
        ],
    )

    client.put(
        "/api/basket/replace/",
        {"books": []},
        content_type="application/json",
    )
    assert get_basket_books(client) == []


@pytest.mark.django_db
def test_basket_replace_invalid(client: Client):
    authorize(client)
    response = client.put("/api/basket/replace/", {"books": ["ISU_1"]}, content_type="application/json")
    assert response.status_code == 400
