import pytest
import multiprocessing

from library_service.tests.opac_mock import run_server

@pytest.fixture(scope="session")
def run_mock_opac(request: pytest.FixtureRequest):
    mock_process = multiprocessing.Process(run_server)
    def finalizer(mock_process=mock_process):
        mock_process.terminate()
    request.addfinalizer(finalizer)