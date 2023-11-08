import dataclasses

from whoispyside6_clone.utils.async_socket import AsyncSocket


@dataclasses.dataclass
class HostConverter:
    aliases: list
    addresses: list

    def __init__(self, name: str, aliases: list, addresses: list):
        """
        :param mode: ADDRESS, NAME
        :param value:
        """
        self.name = name
        self.aliases = aliases
        self.addresses = addresses


async def create_hostConverter(mode: str, value: str) -> HostConverter:
    socket = AsyncSocket()

    result = None

    if mode.upper() == "ADDRESS":
        result = await socket.get_host_by_addr(value)
    elif mode.upper() == "NAME":
        result = await socket.get_host_by_name(value)
    else:
        result = None

    return HostConverter(result.name, result.aliases, result.addresses)
