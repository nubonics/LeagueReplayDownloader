import json

from settings import summoner_names_filepath


def load_summoner_names():
    with open(summoner_names_filepath, 'r') as reader:
        return json.load(reader)
