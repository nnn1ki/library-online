import requests
from dataclasses import dataclass
from dataclasses_json import dataclass_json, Undefined
from django.conf import settings

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class OpacDatabase:
    name: str
    order: bool
    description: str | None = None

def opac_databases() -> list[OpacDatabase]:
    r = requests.get(f"{settings.OPAC_HOSTNAME}/api/databases")
    r.raise_for_status()
    
    return OpacDatabase.schema().load(r.json(), many=True)