import requests
from dataclasses import dataclass
from dataclasses_json import dataclass_json, Undefined
from django.conf import settings

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class IrbisBookLink:
    url: str | None
    description: str | None

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class IrbisBookExemplar:
    number: str | None
    amount: int
    onhand: str | None
    status: str | None
    sigla: str | None

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class IrbisBookSee:
    url: str
    description: str | None

@dataclass_json(undefined=Undefined.EXCLUDE)
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
    see: list[IrbisBookSee] | None
    cards: list[str] | None
    year: int
    created: str | None
    electronic: bool
    language: str | None
    usage: int
    popularity: int
    stamp: str | None
    section: str | None

def irbis_search(database: str, expression: str) -> list[IrbisBook]:
    payload = {
        "database": database,
        "expression": expression,
        "format": "@opac"
    }

    r = requests.post(f"{settings.IRBIS_HOSTNAME}/search", json=payload)
    r.raise_for_status()
    
    return IrbisBook.schema().load(r.json(), many=True)

def irbis_book_retrieve(database: str, mfn: int) -> IrbisBook:
    r = requests.get(f"{settings.IRBIS_HOSTNAME}/books/by/mfn/{database}/{mfn}")
    r.raise_for_status()

    return IrbisBook.schema().load(r.json())