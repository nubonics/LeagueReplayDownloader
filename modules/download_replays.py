import asyncio
import httpx

from requests.auth import HTTPBasicAuth

from modules.get_lockfile_data import get_lockfile_data
from modules.leaky_bucket import AsyncLeakyBucket
from modules.match_id_generator import match_id_generator

bucket = AsyncLeakyBucket(1, 0.015)
client = httpx.AsyncClient(verify=False)


async def get_metadata(base_url, gameId):
    response = await client.get(f'{base_url}/v1/metadata/{gameId}')
    return response.json()


async def create_metadata(base_url, gameId):
    await client.post(f'{base_url}/v2/metadata/{gameId}/create', json={})


async def download_rp(base_url, gameId):
    await client.post(f'{base_url}/v1/rofls/{gameId}/download/graceful', json={})


async def download(base_url, gameId):
    while True:
        await bucket.acquire()
        data = await get_metadata(base_url=base_url, gameId=gameId)
        keys = data.keys()

        if 'errorCode' in keys:
            await bucket.acquire()
            await create_metadata(base_url=base_url, gameId=gameId)
        elif 'state' in keys:
            state = data['state']
            if state == 'download':
                await bucket.acquire()
                await download_rp(base_url=base_url, gameId=gameId)
            elif state == 'lost' or state == 'incompatible' or state == 'watch':
                break

    print(f'DONE: gameId: {str(gameId)}')


async def download_replays():
    lock_data = await get_lockfile_data()
    client.auth = HTTPBasicAuth('riot', lock_data['remoting-auth-token'])

    base_url = f'https://127.0.0.1:{str(lock_data["app-port"])}/lol-replays'

    game_ids = match_id_generator()

    tasks = list()
    try:
        while True:
            gameId = next(game_ids)
            tasks.append(asyncio.create_task(download(base_url=base_url, gameId=gameId)))
    except:
        pass

    await asyncio.gather(*tasks)
    await client.aclose()