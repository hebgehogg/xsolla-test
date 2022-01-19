import argparse
import asyncio
import json
import aiohttp


parser = argparse.ArgumentParser(description="server")
parser.add_argument('-r', '--api-root', help='select app root', default='localhost:8080/api/')
parser.add_argument('function', nargs='*')
# python client.py —api-root=localhost:8080/api/ select 2

args = parser.parse_args()
# todo comments


async def main():
    if args.api_root:
        base_root = f'http://{args.api_root}{args.function[1]}'
        if args.function[1] == 'create' or args.function[1] == 'update':
            with open(args.function[2]) as json_file:
                file = json.load(json_file)
            async with aiohttp.ClientSession() as client:
                async with client.post(base_root, json=file) as response:
                    print(await response.json())
        else:
            try:
                url = f'{base_root}/{args.function[2]}'
            except: url = base_root

            async with aiohttp.ClientSession() as client:
                async with client.get(url) as response:
                    print(await response.json())


if __name__ == "__main__":
    asyncio.run(main())
