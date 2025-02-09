from aiohttp import ClientSession
import pytest

from library_service.opac.api.databases import opac_databases
from library_service.opac.api.scenarios import opac_scenarios
from library_service.tests import opac_mock

@pytest.mark.asyncio
async def test_databases():
    async with ClientSession() as client:
        databases = await opac_databases(client)
        assert databases == opac_mock.DATABASES

@pytest.mark.asyncio
async def test_scenarios():
    async with ClientSession() as client:
        scenarios = await opac_scenarios(client, "ISTU")
        assert scenarios == opac_mock.SCENARIOS