import json
import requests
import config


def register_user(username):
    """ Register a new username. """
    print('Attempting to register username: {} ...'.format(username))
    path = '/users/register'
    url = config.host + path
    data = {'username': username}
    r = requests.post(url, data=json.dumps(data))
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('Bad response: {}\n{}'.format(r.status_code, e))
        return None

    output = r.json()
    print('\t' + output['message'])
    username, access_token = output['username'], output['access_token']
    if access_token is not None:
        print('\tUsername: {}'.format(username))
        print('\tAccess token: {}'.format(access_token))

    return access_token


def create_game():
    """ Create a new game. """
    print('Attempting to create game...')
    path = '/games/create'
    url = config.host + path
    headers = {
        'username': config.username,
        'access_token': config.access_token
    }
    data = json.dumps({
        'players': ['zora', 'chris', 'mitch'],
        'duration': 1000,
    })
    r = requests.post(url, headers=headers, data=data)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('Bad response: {}\n{}'.format(r.status_code, e))
        return None

    output = r.json()
    print('\t' + output['message'])
    game_id, players = output['id'], output['players']
    if game_id is not None:
        print('\tGame ID: {}'.format(game_id))
        print('\tPlayers: {}'.format(', '.join(players)))
    return game_id


def play_game(game_id):
    """ Get a game ID for an existing game, if you are a listed player. """
    print('Attempting to join game...')
    path = '/games/play'
    url = config.host + path
    headers = {
        'username': config.username,
        'access_token': config.access_token
    }
    data = json.dumps({'game_id': game_id})
    r = requests.post(url, headers=headers, data=data)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('Bad response: {}\n{}'.format(r.status_code, e))
        return None
    output = r.json()
    print('\t' + output['message'])


def main():
    register_user(config.username)
    game_id = create_game()
    play_game(game_id)


if __name__ == '__main__':
    main()

