from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin, config, Undefined
from aiohttp import ClientSession
from django.conf import settings


@dataclass
class OpacAnnounce(DataClassJsonMixin):
    dataclass_json_config = config(undefined=Undefined.EXCLUDE)["dataclasses_json"]
    link: str


async def opac_announces_list(client: ClientSession) -> list[OpacAnnounce]:
    r = await client.get(f"{settings.OPAC_HOSTNAME}/api/announces")
    r.raise_for_status()

    return OpacAnnounce.schema().load(await r.json(), many=True)
