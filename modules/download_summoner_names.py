import json
from os.path import exists
from time import sleep

from tqdm import tqdm

from settings import summoners_filepath, last_page_number_filepath, max_page_number


def download_summoner_names(session, ugg_base_url, queueId, region):
    leaderboard_req_body = lambda p: {
        "operationName": "getRankedLeaderboard",
        # The query string has been updated, as the u.gg api has slightly changed.
        "query": "query getRankedLeaderboard($page: Int, $queueType: Int, $regionId: String!) {\n  leaderboardPage(page: $page, queueType: $queueType, regionId: $regionId) {\n    totalPlayerCount\n    topPlayerMostPlayedChamp\n    players {\n      iconId\n      losses\n      lp\n      overallRanking\n      rank\n      summonerLevel\n      summonerName\n      tier\n      wins\n      __typename\n    }\n    __typename\n  }\n}\n",
        "variables": {
            "page": p,
            "queueType": queueId,
            "regionId": region
        }
    }
    # Load the summoners file if it already exists
    if exists(summoners_filepath):
        # Resume downloading summoner names where we last left off

        with open(summoners_filepath, 'r') as reader:
            data = json.load(reader)

        with open(last_page_number_filepath, 'r') as reader:
            last_page_number = int(reader.read())
            # Because of the way python's range function works, add one to the last_page_number so it skips downloading
            # the same data as before
            if last_page_number == max_page_number - 1:
                last_page_number = last_page_number + 1
    else:
        # Does not need to be a set,
        #       because there can't be another player in the same region with the same summoner name.
        data = list()
        last_page_number = 1

    # This will take about an hour to complete
    # Lets pull the summoner names from the first 350 pages of the leaderboard on u.gg
    if last_page_number < max_page_number:
        print('Downloading summoner`s profile data.')
        for n in tqdm(range(last_page_number, max_page_number)):
            # Print the page number in-case of an interruption happens, so that we can manually edit this file and resume downloading
            r = session.post(ugg_base_url, json=leaderboard_req_body(n))
            current_data = r.json()
            data.append(current_data)
            with open(summoners_filepath, 'w') as writer:
                json.dump(data, writer, indent=4)
            with open(last_page_number_filepath, 'w') as writer:
                writer.write(str(n))
            sleep(0.75)

        print('\nDONE: downloading summoner`s profile data.')
