import argparse
import asyncio
import json
import aiohttp

parser = argparse.ArgumentParser(description="server")
parser.add_argument('--api-root', help='select app root', default='localhost:8080/api', nargs='?')
parser.add_argument('function', choices=['create', 'select', 'update', 'delete', 'create_table'])
parser.add_argument('parameter', nargs='?')


class ConsoleInterface:
    def __init__(self, base_root, args):
        self.base_root = base_root
        self.args = args

    async def create(self):
        with open(self.args.parameter) as json_file:
            file = json.load(json_file)
        item = await self.post_request(f'{self.base_root}/{self.args.function}', file)
        print(item)

    async def select(self):
        if self.args.parameter is not None:
            item = await self.get_request(f'{self.base_root}/{self.args.function}/{self.args.parameter}')
            print(item)
        else:
            count = await self.get_request(f'{self.base_root}/{self.args.function}/select_count')
            for offset in range(0, count['count(*)'], 10):
                meetings = await self.get_request(f'{self.base_root}/{self.args.function}/select_all/{offset}')
                print(meetings)

    async def update(self):
        with open(self.args.parameter) as json_file:
            file = json.load(json_file)
        item = await self.post_request(f'{self.base_root}/{self.args.function}', file)
        print(item)

    async def delete(self):
        result = await self.get_request(f'{self.base_root}/{self.args.function}/{args.parameter}')
        print(result)

    async def create_table(self):
        result = await self.get_request(f'{self.base_root}/{self.args.function}')
        print(result)

    async def post_request(self, url, file):
        async with aiohttp.ClientSession() as client:
            async with client.post(url, json=file) as response:
                return await response.json()

    async def get_request(self, url):
        async with aiohttp.ClientSession() as client:
            async with client.get(url) as response:
                return await response.json()


async def main():
    args = parser.parse_args()
    base_root = f'http://{args.api_root}'

    console_interface = ConsoleInterface(base_root, args)
    await call_method(console_interface, args.function)


async def call_method(o, name):
    return await getattr(o, name)()


if __name__ == "__main__":
    asyncio.run(main())
