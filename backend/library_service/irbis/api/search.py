import requests
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from django.conf import settings

@dataclass_json
@dataclass
class BookLink:
    url: str | None
    description: str | None

@dataclass_json
@dataclass
class BookExemplar:
    number: str | None
    amount: int
    onhand: str | None
    status: str | None
    sigla: str | None

@dataclass_json
@dataclass
class Book:
    selected: bool
    mfn: int
    id: str | None
    order: bool
    arrangement: str | None
    agents: list[str]
    additional: str | None
    cover: str | None
    links: list[BookLink]
    exemplars: list[BookExemplar]
    see: list[str]
    cards: list[str]
    year: int
    electronic: bool

# TODO: описать остальные параметры; это низкоуровневая функция, поверх которой будет реализована аггрегирующая функция на все БД
# с полноценными фильтрами вместо строки expression
def search(database: str, expression: str) -> list[Book]:
    payload = {
        "database": database,
        "expression": expression
    }

    r = requests.post(f"{settings.IRBIS_HOSTNAME}/search", json=payload)
    r.raise_for_status()
    
    return Book.schema().load(r.json(), many=True)