import requests
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from django.conf import settings

@dataclass_json
@dataclass
class Announce:
    picture: str | None
    description: str | None
    link: str | None

def announces_list() -> list[Announce]:
    r = requests.get(f"{settings.IRBIS_HOSTNAME}/announces")
    r.raise_for_status()
    
    return Announce.schema().load(r.json(), many=True)