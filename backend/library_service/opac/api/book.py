import requests
from dataclasses import dataclass
from dataclasses_json import dataclass_json, Undefined
from django.conf import settings

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class OpacBookLink:
    url: str
    description: str | None = None

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class OpacBookExemplar:
    number: str
    amount: int
    status: str
    onhand: str | None = None
    sigla: str | None = None

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class OpacBookSee:
    url: str
    description: str | None

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class OpacBook:
    db: str
    selected: bool
    mfn: int
    id: str
    description: str
    order: bool
    year: int
    electronic: bool
    usage: int
    exemplars: list[OpacBookExemplar]
    popularity: int
    arrangement: str | None = None
    brief: str | None = None
    agents: list[str] | None = None
    additional: str | None = None
    cover: str | None = None
    links: list[OpacBookLink] | None = None
    see: list[OpacBookSee] | None = None
    cards: list[str] | None = None
    created: str | None = None
    language: str | None = None
    stamp: str | None = None
    section: str | None = None

def opac_search(database: str, expression: str) -> list[OpacBook]:
    payload = {
        "database": database,
        "expression": expression,
        "format": "@opac_plain"
    }

    r = requests.post(f"{settings.OPAC_HOSTNAME}/search", json=payload)
    r.raise_for_status()
    
    return OpacBook.schema().load(r.json(), many=True)

def opac_book_retrieve(database: str, mfn: int) -> OpacBook:
    params = {
        "format": "@opac_plain"
    }

    r = requests.get(f"{settings.OPAC_HOSTNAME}/books/by/mfn/{database}/{mfn}", params=params)
    r.raise_for_status()

    return OpacBook.schema().load(r.json())