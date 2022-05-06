import json
from os.path import exists

from settings import summoner_names_filepath, last_summoner_filepath


def summoner_name_generator():
    find_summoner = False
    if exists(last_summoner_filepath):
        with open(last_summoner_filepath, 'r') as reader:
            find_summoner = True
            last_match_id = int(reader.read())
    else:
        last_match_id = None

    with open(summoner_names_filepath, 'r') as reader:
        for summoner_name in json.load(reader):
            if summoner_name and find_summoner == last_match_id:
                find_summoner = False
                continue
            else:
                yield summoner_name
