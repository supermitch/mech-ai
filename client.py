import json
import requests

USERNAME = 'mitch'
ACCESS_TOKEN = '1bxgfcel'

host = 'http://mech-ai.appspot.com'
host = 'http://127.0.0.1:8080'


def join_game(game_id):
    """ Join an existing game. """
    path = '/games/play'
    url = host + path
    headers = {
        'username': USERNAME,
        'access_token': ACCESS_TOKEN
    }
    r = requests.get(url, headers=headers)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('Bad response: {}\n{}'.format(r.status_code, e.message))
        return None
    output = r.json()


def create_game():
    """ Create a new game. """
    print('Attempting to create game...')
    path = '/games/create'
    url = host + path
    headers = {
        'username': USERNAME,
        'access_token': ACCESS_TOKEN
    }
    data = {
        'players': ['zora', 'chris', 'mitch'],
        'duration': 1000,
    }
    r = requests.post(url, headers=headers, data=json.dumps(data))
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('Bad response: {}\n{}'.format(r.status_code, e.message))
        return None

    output = r.json()
    print('\t' + output['message'])
    game_id, players = output['id'], output['players']
    if game_id is not None:
        print('\tGame ID: {}'.format(game_id))
        print('\tPlayers: {}'.format(', '.join(players)))
    return game_id


def register_user(username):
    """ Register a new username. """
    print('Attempting to register username: {} ...'.format(username))
    path = '/register'
    url = host + path
    data = {'username': username}
    r = requests.post(url, data=json.dumps(data))
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('Bad response: {}\n{}'.format(r.status_code, e.message))
        return None

    output = r.json()
    print('\t' + output['message'])
    username, access_token = output['username'], output['access_token']
    if access_token is not None:
        print('\tUsername: {}'.format(username))
        print('\tAccess token: {}'.format(access_token))

    return access_token


def main():
    register_user('mitch')
    game_id = create_game()
    join_game(game_id)



if __name__ == '__main__':
    main()

