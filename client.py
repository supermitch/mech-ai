import json
import requests

USERNAME = 'mitch'
ACCESS_TOKEN = ''

host = 'http://mech-ai.appspot.com'
host = 'http://127.0.0.1:8080'


def join_game():
    """ Join an existing game. """
    path = '/games/join'
    url = host + path
    headers = {
        'username': USERNAME,
        'access_token': ACCESS_TOKEN
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)


def create_game():
    """ Create a new game. """
    headers = {
        'username': USERNAME,
        'access_token': ACCESS_TOKEN
    }
    data = {
        'players': ['zora', 'chris', 'mitch'],
        'duration': 1000,
    }
    path = '/games/create'
    url = host + path
    r = requests.post(url, data=json.dumps(data), headers=headers)
    if r.status_code == 200:
        print('Response {} ok!'.format(r.status_code))
        print(r.json())
    else:
        print('Bad response: {}'.format(r.status_code))
        print(r.text)


def register_user(username):
    """ Register a new username. """
    data = {'username': username}
    path = '/register'
    url = host + path
    r = requests.post(url, data=json.dumps(data))
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('Bad response: {}\n{}'.format(r.status_code, e.message))
        return None
    else:
        output = r.json()
        print(output['message'])
        if output['access_token'] is not None:
            print('Username: {}'.format(output['username']))
            print('Access token: {}'.format(output['access_token']))
        return access_token


def main():
    register_user('mitch')


if __name__ == '__main__':
    main()

