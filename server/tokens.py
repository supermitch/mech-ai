import string
import random

from models import user_repo

def generate_token(n=8):
    """ Generates an alphanumeric token of length `n`. """
    chars = string.digits + string.ascii_lowercase
    return ''.join(random.choice(chars) for _ in range(n))

def generate_unique_token():
    """ Keep trying until we find an unused access token. """
    while True:
        token = generate_token()
        if user_repo.find_by_access_token(token) is None:
            return token

