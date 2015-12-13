import argparse
import json
import pprint
import requests
import config


def setup_args():
    parser = argparse.ArgumentParser('Mech-AI Client')
    parser.add_argument('-u', '--username', nargs=1)
    parser.add_argument('-t', '--token', nargs=1)
    args = parser.parse_args()
    args.username = None if args.username is None else args.username[0]
    args.token = None if args.token is None else args.token[0]
    return args


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


def create_game(username, access_token, name, players, rounds):
    """ Create a new game. """
    print('Attempting to create game...')
    path = '/games/create'
    url = config.host + path
    headers = {
        'username': username,
        'access_token': access_token
    }
    data = json.dumps({
        'name': name,
        'players': players,
        'duration': rounds * len(players),
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


def play_game(game_id, username, access_token):
    """ Get a game ID for an existing game, if you are a listed player. """
    print('Attempting to play game...')
    path = '/games/play'
    url = config.host + path
    headers = {
        'username': username,
        'access_token': access_token
    }
    while True:
        data = {
            'game_id': game_id,
            'message': 'join',
        }
        print('data:\n{}'.format(data))
        ans = raw_input('Send data? (y/n)')
        if ans.lower() == 'y':
            pass
        else:
            return
        r = requests.post(url, headers=headers, data=json.dumps(data))
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print('Bad response: {}\n{}'.format(r.text, e))
            return None
        output = r.json()
        print('\tMessage:' + output['message'])
        print('\tOutput:')
        pprint.pprint(output, indent=2)


def main():
    args = setup_args()
    username = args.username if args.username else config.username
    access_token = args.token if args.token else config.access_token
    register_user(username)
    game_id = create_game(username, access_token, name='Test game', players=['mitch', 'nigel'], rounds=20)
    play_game(game_id, username, access_token)


if __name__ == '__main__':
    main()

