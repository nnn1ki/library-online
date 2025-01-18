import requests
from dataclasses import dataclass
from dataclasses_json import dataclass_json, Undefined
from django.conf import settings

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class IrbisDatabase:
    name: str | None
    description: str | None
    order: bool

def irbis_databases() -> list[IrbisDatabase]:
    r = requests.get(f"{settings.IRBIS_HOSTNAME}/databases")
    r.raise_for_status()
    
    return IrbisDatabase.schema().load(r.json(), many=True)