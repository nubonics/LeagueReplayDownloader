import json
from os.path import exists

from settings import match_ids_filepath, last_match_id_filepath


def match_id_generator():
    find_match_id = False
    if exists(last_match_id_filepath):
        with open(last_match_id_filepath, 'r') as reader:
            find_match_id = True
            last_match_id = int(reader.read())
    else:
        last_match_id = None
    
    with open(match_ids_filepath, 'r') as reader:
        for match_id in json.load(reader):
            if find_match_id and match_id == last_match_id:
                find_match_id = False
                continue 
            else:
                yield match_id
