from modules.download_single_replay import download_single_replay
from modules.get_lockfile_data import get_lockfile_data
from modules.match_id_generator import match_id_generator
from modules.tps_bucket import TPSBucket


async def download_replays():
    # Datadragon claims that LCU api is limited to 100 calls per second
    # download_single_replay can take up to 4 calls
    # 100 / 4 = 20 calls per second, lets use 16 calls per second to error on the side of caution
    tps_bucket = TPSBucket(expected_tps=16)
    tps_bucket.start()

    lockfile_data = get_lockfile_data()
    port = lockfile_data['app-port']
    remote_auth_token = lockfile_data['remoting-auth-token']

    match_ids = match_id_generator()

    # This needs some serious work... but should work for now...
    try:
        while True:
            if tps_bucket.get_token():
                await download_single_replay(gameId=next(match_ids), port=port, remote_auth_token=remote_auth_token)
    except:
        pass
