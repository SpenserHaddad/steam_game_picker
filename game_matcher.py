import shutil
from urllib.parse import urljoin
import requests

class InvalidSteamIdException(Exception):
    message = "The given SteamId was not found"

class InvalidAPIKeyException(Exception):
    message = "The API key used was invalid"

with open('steam.key', 'r') as f:
    api_key = f.read()

STEAMUSER_URL = r'https://api.steampowered.com/ISteamUser/'
PLAYERSERVICE_URL = r'https://api.steampowered.com/IPlayerService'

def get_steamid_from_name(steam_name):
    """Finds the id of the player by their Steam username.
    This must be their permament username, NOT their nickname.
    """
    url = urljoin(STEAMUSER_URL, r'ResolveVanityURL/v0001')
    opts = {'key': api_key, 'vanityurl':steam_name}
    resp = requests.get(url, params=opts)
    _validate_api_response(resp)

    resp_json = resp.json()['response']
    if resp_json['success'] == 1:
        return resp_json['steamid']
    else:
        return None

def get_friends(steamid):
    """Returns a dict of the user's friends from their steamid"""
    friend_url = urljoin(STEAMUSER_URL, 'GetFriendList/v0001')
    friend_opts = {'key': api_key, 'steamid': steamid, 'relationship': 'friend'}
    friend_resp = requests.get(friend_url, params=friend_opts)
    _validate_api_response(friend_resp)

    friend_json = friend_resp.json()

    return friend_json['friendslist']['friends']


def get_player_summaries(steamids):
    """Returns a Steam summary of a user from their steamid"""
    summary_url = urljoin(STEAMUSER_URL, r'GetPlayerSummaries/v0002')
    summary_opts = {'key': api_key, 'steamids': ','.join(steamids)}
    summary_resp = requests.get(summary_url, params=summary_opts)
    _validate_api_response(summary_resp)

    summary_json = summary_resp.json()
    return summary_json['response']['players']


def get_player_games(steamids):
    games_url = urljoin(PLAYERSERVICE_URL, r'/GetOwnedGames/v0001/')
    game_opts = {'key': api_key, 'steamid': steamids, 'include_appinfo': 'true'}
    game_resp = requests.get(games_url, params=game_opts)
    _validate_api_response(game_resp)

    game_json = game_resp.json()
    return game_json['response']['games']


def get_game_icon(game_data):
    icon_url =r'http://media.steampowered.com/steamcommunity/public/images/\
    apps/{0}/{1}.jpg'.format(game_data['appid'], game_data['img_icon_url'])
    resp = requests.get(icon_url, stream=True)
    _validate_api_response(resp)

    resp.raw.decode_content = True
    with open('icon.png', 'wb') as f:
        shutil.copyfileobj(resp.raw, f)

def _validate_api_response(response):
    """Checks response and throws appropriate exception if it's an HTML error"""    
    if response.status_code == 403:
        raise InvalidSteamIdException
    elif response.status_code == 500:
        raise InvalidAPIKeyException

if __name__ == "__main__":
    steam_id = '76561198028906273'

    selected = ['remyjette', 'King123', 'Minty']
    selected_ids = [s['steamid'] for s in summaries if s['personaname'] in selected]
