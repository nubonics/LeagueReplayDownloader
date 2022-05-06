champion_s = ['Caitlyn']
region = 'na1'
queueId = 420
seasonId = 18  # Hmm, wasn't able to find a way to get this
ugg_base_url = "https://u.gg/api"
number_of_summoners = 35_000
max_page_number = round(number_of_summoners / 100) + 1


# FILEPATHS
data_directory = 'data'
champion_ids_filepath = f'{data_directory}/champion_ids.txt'
match_ids_filepath = f'{data_directory}/match_ids.json'
last_match_id_filepath = f'{data_directory}/last_match_id.txt'
last_summoner_filepath = f'{data_directory}/last_summoner.txt'
summoners_filepath = f'{data_directory}/summoners.json'
summoner_names_filepath = f'{data_directory}/summoner_names.json'
last_page_number_filepath = f'{data_directory}/last_page_number.txt'
