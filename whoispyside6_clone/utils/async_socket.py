import asyncio
import logging
from socket import AddressFamily

import aiodns


class AsyncSocket:
    def __init__(self):
        self.DNS = aiodns.DNSResolver(loop=asyncio.get_event_loop(), timeout=60)

    async def get_host_by_addr(self, name):
        return await self.DNS.gethostbyaddr(name)

    async def get_host_by_name(self, name, family=AddressFamily.AF_INET):
        return await self.DNS.gethostbyname(name, family)

    async def query(self, name):
        a = cname = None
        try:
            a = await self.DNS.query(name, "A")
        except aiodns.error.DNSError:
            logging.debug("A returned answer with no data")
        try:
            cname = await self.DNS.query(name, "CNAME")
        except aiodns.error.DNSError:
            logging.debug("CNAME returned answer with no data")
        return {"A": a, "CNAME": cname}


if __name__ == '__main__':
    # test code
    test_loop = asyncio.get_event_loop()

    socket = AsyncSocket()
    addr_test = socket.get_host_by_addr("8.8.8.8")
    addr_result = test_loop.run_until_complete(addr_test)
    print(addr_result.name)

    name_test = socket.get_host_by_name("dns.google")
    name_result = test_loop.run_until_complete(name_test)
    print(name_result.addresses)

    record_test = socket.query("google.com")
    query_result = test_loop.run_until_complete(record_test)
    print(query_result)

    record_test = socket.query("quantum-classroom.kookmin.ac.kr")
    query_result = test_loop.run_until_complete(record_test)
    print(query_result)
