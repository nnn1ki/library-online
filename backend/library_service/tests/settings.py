from app.settings import *  # pylint: disable=wildcard-import,unused-wildcard-import
from library_service.tests import opac_mock

OPAC_HOSTNAME = f"http://localhost:{opac_mock.PORT}"
