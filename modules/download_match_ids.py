import json
from time import sleep
from tqdm import tqdm

from modules.load_champ_ids import load_champ_ids
from modules.load_summoner_names import load_summoner_names
from settings import match_ids_filepath, champion_s


def download_match_ids(session, ugg_base_url, region, queueId, seasonId):
    champion_ids = load_champ_ids()
    match_ids = set()
    matches_req_body = lambda summoner_name: {
        'operationName': 'FetchMatchSummaries',
        'variables': {
            'regionId': region,
            'summonerName': summoner_name,
            'queueType': [queueId],
            'duoName': '',  # This parameter has been added, as the u.gg api has slightly changed.
            'role': [],
            'seasonIds': [
                seasonId,
            ],
            'championId': [champion_ids[c] for c in champion_s],
        },
        # The query string has been updated, as the u.gg api has slightly changed.
        'query': 'query FetchMatchSummaries($championId: [Int], $page: Int, $queueType: [Int], $duoName: String, $regionId: String!, $role: [Int], $seasonIds: [Int]!, $summonerName: String!) {\n  fetchPlayerMatchSummaries(\n    championId: $championId\n    page: $page\n    queueType: $queueType\n    duoName: $duoName\n    regionId: $regionId\n    role: $role\n    seasonIds: $seasonIds\n    summonerName: $summonerName\n  ) {\n    finishedMatchSummaries\n    totalNumMatches\n    matchSummaries {\n      assists\n      championId\n      cs\n      damage\n      deaths\n      gold\n      items\n      jungleCs\n      killParticipation\n      kills\n      level\n      matchCreationTime\n      matchDuration\n      matchId\n      maximumKillStreak\n      primaryStyle\n      queueType\n      regionId\n      role\n      runes\n      subStyle\n      summonerName\n      summonerSpells\n      psHardCarry\n      psTeamPlay\n      lpInfo {\n        lp\n        placement\n        promoProgress\n        promoTarget\n        promotedTo {\n          tier\n          rank\n          __typename\n        }\n        __typename\n      }\n      teamA {\n        championId\n        summonerName\n        teamId\n        role\n        hardCarry\n        teamplay\n        __typename\n      }\n      teamB {\n        championId\n        summonerName\n        teamId\n        role\n        hardCarry\n        teamplay\n        __typename\n      }\n      version\n      visionScore\n      win\n      __typename\n    }\n    __typename\n  }\n}\n',
    }

    # Ok! fine, we'll tell em we're a bot...
    session.headers = {
        "Content-Type": "application/json"
    }

    print('Downloading match id`s from high ranking summoners who have played our selected champion within the past 20 games.')

    # Ug, how long is this going to take? LMK tqdm
    for sN in tqdm(load_summoner_names()):
        response = session.post(url=ugg_base_url, json=matches_req_body(sN))
        data = response.json()
        try:
            matches = data["data"]["fetchPlayerMatchSummaries"]["matchSummaries"]
        except TypeError:
            continue
        for match in matches:
            # According to data-dragon, match data is stored for 2 years
            # Doesn't make much sense to have a version `key`
            #   if the only version accessible for downloading is the current one
            match_id = match["matchId"]
            match_ids.add(match_id)

        # Re-write the raw_match_ids data for every group / summoner name
        with open(match_ids_filepath, 'w') as writer:
            data = list(match_ids)
            json.dump(data, writer, indent=4)

        sleep(0.75)

    print('DONE: download match id`s.')
