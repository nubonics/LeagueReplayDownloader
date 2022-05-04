import json

from settings import summoners_filepath, summoner_names_filepath


def extract_summoner_names():
    with open(summoners_filepath, 'r') as reader:
        data = json.load(reader)

    summoner_names = list()
    for column in data:
        for row in column['data']['leaderboardPage']['players']:
            summoner_name = row['summonerName']
            summoner_names.append(summoner_name)

    with open(summoner_names_filepath, 'w') as writer:
        json.dump(summoner_names, writer, indent=4)
