from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin, config, Undefined
from aiohttp import ClientSession
from django.conf import settings

@dataclass
class AuthResponse(DataClassJsonMixin):
    dataclass_json_config = config(undefined=Undefined.EXCLUDE)["dataclasses_json"]
    accessToken = str
    refreshToken = str

async def login_reader(client: ClientSession, username: str, password: str) -> AuthResponse:
    payload = {"username": username, "password": password}

    r = await client.post(f"{settings.OPAC_HOSTNAME}/api/login/reader", json=payload)
    r.raise_for_status()
    return AuthResponse.schema().load(await r.json())

async def login_librarian(client: ClientSession, username: str, password: str) -> AuthResponse:
    payload = {"username": username, "password": password}

    r = await client.post(f"{settings.OPAC_HOSTNAME}/api/login/librarian", json=payload)
    r.raise_for_status()
    return AuthResponse.schema().load(await r.json())

async def login_admin(client: ClientSession, username: str, password: str) -> AuthResponse:
    payload = {"username": username, "password": password}

    r = await client.post(f"{settings.OPAC_HOSTNAME}/api/login/admin", json=payload)
    r.raise_for_status()
    return AuthResponse.schema().load(await r.json())

# async def get_login_info(client: ClientSession, username: str, password: str) -> AuthResponse:
#     payload = {"username": username, "password": password}

#     r = await client.get(f"{settings.OPAC_HOSTNAME}/api/login/info")
#     r.raise_for_status()
#     return AuthResponse.schema().load(await r.json())