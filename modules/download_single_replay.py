import asyncio

import httpx


async def download_single_replay(gameId, port, remote_auth_token):
    base_url = f'https://127.0.0.1:{port}/lol-replays'
    headers = {'Content-Type': 'application/json'}
    async with httpx.AsyncClient(headers=headers, auth=("riot", remote_auth_token), verify=False) as client:
        # verify=False because I am lazy and don't care about the security at a lan level
        # not sure what happens when riot is being called via the localhost, but I still don't really care
        check_replay_status_response = await check_replay_status(client=client, base_url=base_url, gameId=gameId)
        check_replay_status_response_data = check_replay_status_response.json()
        check_replay_status_response_keys = check_replay_status_response_data.keys()
        if 'state' in check_replay_status_response_keys:
            if check_replay_status_response_data['state'] == 'lost':
                return False
        elif 'errorCode' in check_replay_status_response_keys:
            await add_metadata(client=client, base_url=base_url, gameId=gameId)
            await wait_for_state(client=client, base_url=base_url, gameId=gameId, state1='download', state2=None)
            await graceful_download(client=client, base_url=base_url, gameId=gameId)
            await wait_for_state(client=client, base_url=base_url, gameId=gameId, state1='lost', state2='watch')


async def wait_for_state(client, base_url, gameId, state1, state2):
    while True:
        response = await check_replay_status(client=client, base_url=base_url, gameId=gameId)
        response_data = response.json()
        if 'state' in response_data.keys():
            if response_data['state'] == state1:
                return False
            elif state2 is not None:
                if response_data['state'] == state2:
                    return True
        await asyncio.sleep(1)


async def check_replay_status(client, base_url, gameId):
    return await client.get(f'{base_url}/v1/metadata/{gameId}')


async def graceful_download(client, base_url, gameId):
    await client.post(f'{base_url}/v1/rofls/{gameId}/download/graceful', json={})


async def add_metadata(client, base_url, gameId):
    await client.post(f'{base_url}/v2/metadata/{gameId}/create', json={})
