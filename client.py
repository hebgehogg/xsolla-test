import argparse
import asyncio

import aiohttp

parser = argparse.ArgumentParser(description="server")
parser.add_argument('-r', '--api-root', help='select app root', default='localhost:8080')
parser.add_argument('function')
parser.add_argument('file')
args = parser.parse_args()
# print(args.file.readlines())

base_root = args.api_root
print(base_root)


async def requester(url: str, file=None):
    async with aiohttp.ClientSession() as cli:
        async with cli.get(url) as response:
            print(await response.json())


async def main():
    if args.function == 'create':
        url = f'http://{base_root}create'
        await requester(url)


if __name__ == "__main__":
    asyncio.run(main())