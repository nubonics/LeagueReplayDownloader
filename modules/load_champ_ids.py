from settings import champion_ids_filepath


def load_champ_ids():
    champ_ids = dict()
    # Didn't feel like converting this into a json data file
    with open(champion_ids_filepath) as f:
        content = f.read()
        lines = content.split("\n")
        for l in lines:
            ln = l.split(":")
            champ = ln[1].strip()
            champ_id = int(ln[0])
            champ_ids[champ] = champ_id
    return champ_ids
