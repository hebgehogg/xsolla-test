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
        try:
            with open(self.args.parameter) as json_file:
                file = json.load(json_file)
        except:
            return 'Invalid file path'
        async with aiohttp.ClientSession() as client:
            async with client.post(f'{self.base_root}/{self.args.function}', json=file) as response:
                status_code = response.status
                res = await response.json()
        if status_code == 422:
            return 'Invalid file format or structure'
        else:
            return res

    async def update(self):
        try:
            with open(self.args.parameter) as json_file:
                file = json.load(json_file)
        except:
            return 'Invalid file path'
        async with aiohttp.ClientSession() as client:
            async with client.put(f'{self.base_root}/{self.args.function}', json=file) as response:
                status_code = response.status
                res = await response.json()
            if status_code == 422:
                return 'Invalid file format or structure'
            else:
                return res

    async def select(self):
        if self.args.parameter is not None:
            async with aiohttp.ClientSession() as client:
                async with client.get(f'{self.base_root}/{self.args.function}/{self.args.parameter}') as response:
                    return await response.json()
        else:
            async with aiohttp.ClientSession() as client:
                async with client.get(f'{self.base_root}/{self.args.function}/select_count') as response:
                    count = await response.json()
            # с шагом 10
            for offset in range(0, count['count(*)'], 10):
                async with aiohttp.ClientSession() as client:
                    async with client.get(f'{self.base_root}/{self.args.function}/select_all/{offset}') as response:
                        print(await response.json())
                        return 'Finish'

    async def delete(self):
        async with aiohttp.ClientSession() as client:
            async with client.delete(f'{self.base_root}/{self.args.function}/{self.args.parameter}') as response:
                return await response.json()

    async def create_table(self):
        async with aiohttp.ClientSession() as client:
            async with client.get(f'{self.base_root}/{self.args.function}') as response:
                return await response.json()


async def main():
    args = parser.parse_args()
    base_root = f'http://{args.api_root}'

    console_interface = ConsoleInterface(base_root, args)
    result = await call_method(console_interface, args.function)
    print(result)


async def call_method(o, name):
    return await getattr(o, name)()


if __name__ == "__main__":
    asyncio.run(main())
