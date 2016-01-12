# mech-ai

Program your AI to destroy other bots and take over the world.

## Google App Engine (GAE)

## GAE Documentation

https://cloud.google.com/appengine/docs/python/

1. Install [Google App Engine SDK](https://cloud.google.com/appengine/downloads)


## Server

The server must be written in Python 2.7.x

1. Run development server in root folder: `$ dev_appserver.py .`
2. See output at [http://localhost:8080/](http://localhost:8080/)
3. You can view the dev GAE dashboard at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

4. To deploy: `$ appcfg.py -A mech-ai update app.yaml`
5. See output at [http://mech-ai.appspot.com/](http://mech-ai.appspot.com/)


## Client

The client is also written in Python 2.7.x.

1. Run the client: `$ python client.py`

### Authentication:

All messages to the server (except to register a new username) must be accompanied
by authentication headers, so you need to provide your username and access token:

* Use command line args: `$ python client.py -u mitch -t 4hfg83bg`
* Use ENV vars: `$ USER=mitch TOKEN=a6javvi8 python client.py`
* Set `username` and `access_token` variables in `local_config.py`

Precedence: Arguments > local_config.py > Environment variables

After registering a new username you'll need to restart your client with those
settings.

