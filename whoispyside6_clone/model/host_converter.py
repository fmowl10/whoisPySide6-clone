import asyncio
import dataclasses

from whoispyside6_clone.utils.async_socket import AsyncSocket


@dataclasses.dataclass
class HostConverter:
    name: str
    aliases: list
    addresses: list
    __loop = asyncio.get_event_loop()

    def __init__(self, mode: str, value: str):
        """
        :param mode: ADDRESS, NAME
        :param value:
        """
        if mode.upper() == "ADDRESS":
            socket = AsyncSocket()
            __result = self.__loop.run_until_complete(socket.get_host_by_addr(value))
        elif mode.upper() == "NAME":
            socket = AsyncSocket()
            __result = self.__loop.run_until_complete(socket.get_host_by_name(value))
        else:
            __result = None
            raise KeyError("Key Error! Select Mode : [ADDRESS, NAME]")
        self.name = __result.name
        self.aliases = __result.aliases
        self.addresses = __result.addresses


if __name__ == '__main__':
    host = HostConverter(mode="ADDRESS", value="8.8.8.8")
    print(host)
    host = HostConverter(mode="NAME", value="dns.google")
    print(host)

    try:
        host = HostConverter(mode="TEST", value="dns.google")
    except KeyError as e:
        print(e)
