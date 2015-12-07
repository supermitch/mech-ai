import os

host_env = {
    'prod': 'http://mech-ai.appspot.com',
    'dev': 'http://127.0.0.1:8080',
}

environment = os.getenv('ENV', 'dev')
host = host_env.get(environment)

username = os.getenv('USER')
access_token = os.getenv('TOKEN')

try:
    from local_config import *  # Override with local settings if exists
except ImportError:
    pass

