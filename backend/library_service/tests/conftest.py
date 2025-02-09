from aiohttp import ClientSession
import pytest
import multiprocessing

from library_service.tests.opac_mock import run_server

@pytest.fixture(scope="session", autouse=True)
def run_mock_opac():
    mock_process = multiprocessing.Process(target=run_server)
    mock_process.daemon = True
    mock_process.start()
    
    yield
    
    mock_process.terminate()

@pytest.fixture
async def client_session():
    async with ClientSession() as client:
        yield client