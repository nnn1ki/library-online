import requests
from dataclasses import dataclass
from dataclasses_json import dataclass_json, Undefined
from django.conf import settings

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class IrbisAnnounce:
    picture: str | None
    link: str | None
    description: str | None = None

def irbis_announces_list() -> list[IrbisAnnounce]:
    r = requests.get(f"{settings.IRBIS_HOSTNAME}/announces")
    r.raise_for_status()

    return IrbisAnnounce.schema().load(r.json(), many=True)