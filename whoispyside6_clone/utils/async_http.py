import asyncio

import aiohttp


class AsyncHTTP:
    def __init__(self, url, time_out=60):
        self.url = url
        self.time_out = aiohttp.ClientTimeout(total=time_out)

    async def get_json_contents(self):
        async with aiohttp.ClientSession(timeout=self.time_out) as session:
            async with session.get(url=self.url) as resp:
                result = await resp.json()
                return result


if __name__ == '__main__':
    # test code
    test = AsyncHTTP(url='https://api.github.com/events')
    asyncio.get_event_loop().run_until_complete(test.get_json_contents())
