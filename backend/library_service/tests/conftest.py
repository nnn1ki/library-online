import pytest
import multiprocessing

from library_service.tests.opac_mock import run_server

@pytest.fixture(scope="session", autouse=True)
def run_mock_opac(request: pytest.FixtureRequest):
    mock_process = multiprocessing.Process(target=run_server)
    mock_process.daemon = True
    mock_process.start()

    def finalizer(mock_process=mock_process):
        mock_process.terminate()
    request.addfinalizer(finalizer)