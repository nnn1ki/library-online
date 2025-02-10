from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from aiohttp import ClientSession
from django.conf import settings


@dataclass
class OpacDatabase(DataClassJsonMixin):
    name: str
    order: bool
    description: str | None = None


async def opac_databases(client: ClientSession) -> list[OpacDatabase]:
    r = await client.get(f"{settings.OPAC_HOSTNAME}/api/databases")
    r.raise_for_status()

    return OpacDatabase.schema().load(await r.json(), many=True, unknown="exclude")
