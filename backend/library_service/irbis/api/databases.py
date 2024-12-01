import requests
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from django.conf import settings

@dataclass_json
@dataclass
class Database:
    name: str | None
    description: str | None
    order: bool

def databases_list() -> list[Database]:
    r = requests.get(f"{settings.IRBIS_HOSTNAME}/databases")
    r.raise_for_status()
    
    return Database.schema().load(r.json(), many=True)