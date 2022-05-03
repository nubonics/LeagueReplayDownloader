def get_latest_patch_version(session):
    url = 'https://ddragon.leagueoflegends.com/api/versions.json'
    response = session.get(url)
    data = response.json()
    full_version = data[0]
    reduced_version = '_'.join(full_version.split('.')[:2])
    return reduced_version
