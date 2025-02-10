from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from aiohttp import ClientSession
from django.conf import settings


@dataclass
class OpacScenario(DataClassJsonMixin):
    prefix: str
    description: str | None = None


async def opac_scenarios(client: ClientSession, database: str) -> list[OpacScenario]:
    r = await client.get(f"{settings.OPAC_HOSTNAME}/api/scenarios/${database}")
    r.raise_for_status()

    return OpacScenario.schema().load(await r.json(), many=True, unknown="exclude")
