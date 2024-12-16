import requests
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from django.conf import settings

@dataclass_json
@dataclass
class IrbisBookLink:
    url: str | None
    description: str | None

@dataclass_json
@dataclass
class IrbisBookExemplar:
    number: str | None
    amount: int
    onhand: str | None
    status: str | None
    sigla: str | None

@dataclass_json
@dataclass
class IrbisBook:
    db: str | None
    selected: bool
    mfn: int
    id: str | None
    order: bool
    arrangement: str | None
    brief: str | None
    description: str | None
    agents: list[str] | None
    additional: str | None
    cover: str | None
    links: list[IrbisBookLink] | None
    exemplars: list[IrbisBookExemplar]
    see: list[str] | None
    cards: list[str] | None
    year: int
    electronic: bool

def irbis_search(database: str, expression: str) -> list[IrbisBook]:
    payload = {
        "database": database,
        "expression": expression,
        "format": "@opac"
    }

    r = requests.post(f"{settings.IRBIS_HOSTNAME}/search", json=payload)
    r.raise_for_status()
    
    return IrbisBook.schema().load(r.json(), many=True)