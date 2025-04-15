from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin, config, Undefined
from aiohttp import ClientSession
import app.local_settings as settings

headers={"X-ISTU-Request": settings.OPAC_INTERNAL_TOKEN}

@dataclass
class OpacReader(DataClassJsonMixin):
    dataclass_json_config = config(undefined=Undefined.EXCLUDE)["dataclasses_json"]
    ticket: str
    name: str
    allowed: bool
    debtor : bool
    gone: bool
    academ: bool
    everlasting: bool
    category: str | None = None
    departemnt: str | None = None
    mail: str | None = None

@dataclass
class OpacLoan(DataClassJsonMixin):
    dataclass_json_config = config(undefined=Undefined.EXCLUDE)["dataclasses_json"]
    type: str
    overdue: bool
    can: bool
    db: str
    book: str
    number: str
    date: str
    deadline: str
    prolongation: int
    description: str | None = None
#Тут проблема, добавил лишние None из-за постоянной ошибки "non-default argument 'prolongation' follows default argument"

async def opac_reader_info_by_mira(client: ClientSession, mira_id) -> OpacReader:
    r = await client.get(f"{settings.OPAC_HOSTNAME}/api/readers/mira/internal/{mira_id}", headers=headers)
    r.raise_for_status()

    return OpacReader.schema().load(await r.json())

async def opac_reader_info_by_ticket(client: ClientSession, ticket_id) -> OpacReader:
    r = await client.get(f"{settings.OPAC_HOSTNAME}/api/readers/internal/{ticket_id}", headers=headers)
    r.raise_for_status()

    return OpacReader.schema().load(await r.json())

async def opac_reader_loans(client: ClientSession, ticket_id) -> list[OpacLoan]:
    r = await client.get(f"{settings.OPAC_HOSTNAME}/api/readers/loans/internal/{ticket_id}", headers=headers)
    r.raise_for_status()

    return OpacLoan.schema().load(await r.json(), many=True)