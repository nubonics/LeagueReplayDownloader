import asyncio

from requests import Session

from modules.download_match_ids import download_match_ids
# from modules.get_latest_patch_version import get_latest_patch_version
from obsolete_data.download_summoner_names import download_summoner_names
from settings import ugg_base_url, queueId, region, seasonId


async def main():
    """
    Usage:
        - Gather the summoner names for the top 35k League of Legends players in a specific region
        - Search the past 20 games of each summoner/player for the champion that we are looking for
        - Download every replay that includes the champion that we are looking for
    Notes:
        - Downloading the match ids via async or threading gives no significant boost in speed
            - semaphores do not download any faster than one-by-one, when only querying one throttled website
        - A significant speed boost is acquired when using async or threading when downloading via the LCU api

    """
    session = Session()
    # Let's pretend to be a browser, that can't render javascript :D
    session.headers = {
        'authority': 'u.gg',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'dnt': '1',
        'origin': 'https://u.gg',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'x-is-ssr': 'false',
    }

    # This is not needed, as I am not filtering by version
    # current_version = get_latest_patch_version(session=session)
    download_summoner_names(session=session, ugg_base_url=ugg_base_url, queueId=queueId, region=region)
    download_match_ids(session=session, ugg_base_url=ugg_base_url, queueId=queueId, region=region, seasonId=seasonId)


if __name__ == '__main__':
    asyncio.run(main())
