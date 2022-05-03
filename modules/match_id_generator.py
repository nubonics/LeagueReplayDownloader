import json

from settings import match_ids_filepath


def match_id_generator():
    with open(match_ids_filepath, 'r') as reader:
        for match_id in json.load(reader):
            yield match_id
