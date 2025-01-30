import requests
from dataclasses import dataclass
from dataclasses_json import dataclass_json, Undefined
from django.conf import settings

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class OpacAnnounce:
    link: str

def opac_announces_list() -> list[OpacAnnounce]:
    r = requests.get(f"{settings.OPAC_HOSTNAME}/api/announces")
    r.raise_for_status()

    return OpacAnnounce.schema().load(r.json(), many=True)