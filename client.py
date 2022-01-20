import argparse
import asyncio
import json
import aiohttp

parser = argparse.ArgumentParser(description="server")
parser.add_argument('--api-root', help='select app root', default='localhost:8080/api', nargs='?')
parser.add_argument('function', choices=['create', 'select', 'update', 'delete', 'create_table'])
parser.add_argument('parameter', nargs='?')


args = parser.parse_args()


async def main():
    base_root = f'http://{args.api_root}'

    if args.function == 'select':
        if args.parameter is not None:
            item = await get_request(f'{base_root}/{args.function}/{args.parameter}')
            print(item)
        else:
            count = await get_request(f'{base_root}/{args.function}/select_count')
            print(count)
            for offset in range(0, count['count(*)'], 10):
                meetings = await get_request(f'{base_root}/{args.function}/select_all/{offset}')
                print(meetings)

    elif args.function == 'create' or args.function == 'update':
        with open(args.parameter) as json_file:
            file = json.load(json_file)
        item = await post_request(f'{base_root}/{args.function}', file)
        print(item)

    elif args.function == 'delete':
        result = await get_request(f'{base_root}/{args.function}/{args.parameter}')
        print(result)
    else:
        result = await get_request(f'{base_root}/{args.function}')
        print(result)


async def post_request(url, file):
    async with aiohttp.ClientSession() as client:
        async with client.post(url, json=file) as response:
            return await response.json()


async def get_request(url):
    async with aiohttp.ClientSession() as client:
        async with client.get(url) as response:
            return await response.json()


if __name__ == "__main__":
    asyncio.run(main())
