import requests
from dataclasses import dataclass
from dataclasses_json import dataclass_json, Undefined
from django.conf import settings

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class IrbisScenario:
    prefix: str
    description: str | None

def irbis_scenarios(database: str) -> list[IrbisScenario]:
    r = requests.get(f"{settings.IRBIS_HOSTNAME}/scenarios/${database}")
    r.raise_for_status()
    
    return IrbisScenario.schema().load(r.json(), many=True)