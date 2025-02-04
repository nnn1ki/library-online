from aiohttp import ClientSession
from dataclasses import dataclass
from dataclasses_json import dataclass_json, Undefined
from django.conf import settings

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class OpacScenario:
    prefix: str
    description: str | None = None

async def opac_scenarios(client: ClientSession, database: str) -> list[OpacScenario]:
    r = await client.get(f"{settings.OPAC_HOSTNAME}/api/scenarios/${database}")
    r.raise_for_status()
    
    return OpacScenario.schema().load(await r.json(), many=True)