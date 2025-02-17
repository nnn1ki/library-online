import multiprocessing
from aiohttp import ClientSession
import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from library_service.models.catalog import Library, LibraryDatabase
from library_service.tests.opac_mock import run_server


@pytest.fixture(scope="session", autouse=True)
def run_mock_opac():
    mock_process = multiprocessing.Process(target=run_server)
    mock_process.daemon = True
    mock_process.start()

    yield

    mock_process.terminate()


@pytest.fixture(scope="session", autouse=True)
def setup_database(django_db_setup, django_db_blocker):  # pylint: disable=unused-argument
    with django_db_blocker.unblock():
        library_inrtu = Library.objects.create(description="ISTU_LIB")
        LibraryDatabase.objects.create(library=library_inrtu, database="ISTU")
        LibraryDatabase.objects.create(library=library_inrtu, database="NTD")

        library_zima = Library.objects.create(description="ZIMA_LIB")
        LibraryDatabase.objects.create(library=library_zima, database="ZIMA")

        user = get_user_model().objects.create_user(
            username="user", password="1234", first_name="Alan", last_name="Turing"
        )
        user.groups.add(Group.objects.get(name="Reader"))


@pytest.fixture
async def client_session():
    async with ClientSession() as client:
        yield client
