import multiprocessing
from aiohttp import ClientSession
import pytest

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
        library = Library.objects.create(description="INRTU")
        LibraryDatabase.objects.create(library=library, database="ISTU")
        LibraryDatabase.objects.create(library=library, database="NTD")


@pytest.fixture
async def client_session():
    async with ClientSession() as client:
        yield client
