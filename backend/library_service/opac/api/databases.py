from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin, config, Undefined
from aiohttp import ClientSession
from django.conf import settings


@dataclass
class OpacDatabase(DataClassJsonMixin):
    dataclass_json_config = config(undefined=Undefined.EXCLUDE)["dataclasses_json"]
    name: str
    order: bool
    description: str | None = None


async def opac_databases(client: ClientSession) -> list[OpacDatabase]:
    r = await client.get(f"{settings.OPAC_HOSTNAME}/api/databases")
    r.raise_for_status()

    return OpacDatabase.schema().load(await r.json(), many=True)
