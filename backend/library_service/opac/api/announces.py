from aiohttp import ClientSession
from dataclasses import dataclass
from dataclasses_json import dataclass_json, Undefined
from django.conf import settings


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class OpacAnnounce:
    link: str


async def opac_announces_list(client: ClientSession) -> list[OpacAnnounce]:
    r = await client.get(f"{settings.OPAC_HOSTNAME}/api/announces")
    r.raise_for_status()

    return OpacAnnounce.schema().load(await r.json(), many=True)
