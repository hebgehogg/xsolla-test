import argparse
import asyncio
import json

import aiohttp

parser = argparse.ArgumentParser(description="server")
parser.add_argument('-r', '--api-root', help='select app root', default='localhost:8080/api/')
parser.add_argument('function')
parser.add_argument('file')
# parser.add_argument('id', required=False)
args = parser.parse_args()
# print(args.file.readlines())
# todo comments

base_root = args.api_root


async def requester(url: str, body=None):
    if args.function == 'create':
        async with aiohttp.ClientSession() as client:
            async with client.post(url, json=body) as response:
                print(await response.json())
    else:
        async with aiohttp.ClientSession() as client:
            async with client.get(url) as response:
                print(await response.json())


async def main():
    url = f'http://{base_root}{args.function}'

    with open(args.file) as json_file:
        data = json.load(json_file)
    if args.function == 'create':
        await requester(url, data)


if __name__ == "__main__":
    asyncio.run(main())
