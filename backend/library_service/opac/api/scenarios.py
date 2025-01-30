import requests
from dataclasses import dataclass
from dataclasses_json import dataclass_json, Undefined
from django.conf import settings

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class OpacScenario:
    prefix: str
    description: str | None = None

def opac_scenarios(database: str) -> list[OpacScenario]:
    r = requests.get(f"{settings.OPAC_HOSTNAME}/api/scenarios/${database}")
    r.raise_for_status()
    
    return OpacScenario.schema().load(r.json(), many=True)