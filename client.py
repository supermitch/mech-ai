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


def prompt_username():
    """ Prompt user to enter a new username. """
    while True:
        ans = raw_input('Enter new username: ')
        if ans == '':
            print('Please enter a valid username')
        else:
            return ans


def prompt_game_id():
    """ Get input game ID. """
    while True:
        ans = raw_input('Enter game ID: ')
        try:
            game_id = str(int(ans))  # TODO: Are all game ID's ints?
            break
        except:
            print('Please enter a valid integer game ID')
    return game_id


def prompt_create_game():
    """ Get inputs required to create a game. """
    while True:
        ans = raw_input('Enter name: ')
        if ans == '':
            print('Please enter a game name')
        else:
            name = ans
            break

    while True:
        ans = raw_input('Enter number of rounds: ')
        if ans == '':
            rounds = 100
            break
        else:
            try:
                rounds = int(ans)
                break
            except:
                print('Please enter a valid integer')

    while True:
        ans = raw_input('Enter list of player usernames: ')
        if ans == '':
            print('Please enter a valid list of players')
        else:
            players = [x.strip() for x in ans.split()]
            break

    return name, rounds, players


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


def post_to_game(url, headers, data):
    """ Post data to our game and get JSON response. """
    r = requests.post(url, headers=headers, data=json.dumps(data))
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('Bad response: {}\n{}'.format(r.text, e))
        return None
    else:
        return r.json()


def play_game(game_id, username, access_token):
    """ Get a game ID for an existing game, if you are a listed player. """
    print('Attempting to play game...')
    path = '/games/play'
    url = config.host + path
    headers = {
        'username': username,
        'access_token': access_token
    }
    data = {'game_id': game_id}
    while True:  # Loop until game starts
        data['message'] = 'join'
        output = post_to_game(url, headers, data)
        message = output['message']
        print('\tMessage: ' + message)
        if message == 'Game started':
            break
        else:
            print('\tMessage:' + message)
            sleep(0.5)

    while True:  # Play until game ends
        data['message'] = 'move'
        print('data:\n{}'.format(data))
        output = post_to_game(url, headers, data)
        pprint.pprint(output, indent=2)
        message = output['message']
        print('\tMessage: ' + message)
        if message == 'Game ended':
            break
        elif message == 'Not your turn':
            print('\tMessage:' + message)
            sleep(0.25)


def main():
    args = setup_args()
    username = args.username if args.username else config.username
    access_token = args.token if args.token else config.access_token
    while True:
        print('Choose an option:')
        print('\t1. Register new username')
        print('\t2. Create new game')
        print('\t3. Join existing game')
        print('\t4. Quit')
        ans = raw_input('> ')
        if ans == '1':
            username = prompt_username()
            register_user(username)
        elif ans == '2':
            name, rounds, players = prompt_create_game()
            game_id = create_game(username, access_token, name=name, players=players, rounds=rounds)
        elif ans == '3':
            game_id = prompt_game_id()
            play_game(game_id, username, access_token)
        elif ans == '4':
            print('Thanks for playing.')
            break
        else:
            print('Choose a valid option (1-4)')


if __name__ == '__main__':
    main()

