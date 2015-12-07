# mech-ai

Program your AI to destroy other bots and take over the world.

## Google App Engine (GAE)

1. Install [Google App Engine SDK](https://cloud.google.com/appengine/downloads)
2. To deploy: `$ appcfg.py -A mech-ai update app.yaml`
3. See output at [http://mech-ai.appspot.com/](http://mech-ai.appspot.com/)

## GAE Documentation

https://cloud.google.com/appengine/docs/python/

## Development

### Server

The server must be written in Python 2.

1. Run development server: `$ dev_appserver.py helloworld/`
2. See output at [http://localhost:8080/](http://localhost:8080/)

### Client

The client is written in Python 3.

1. Activate virtual env: `$ source venv/bin/activate`
2. Run the client: `$ python client.py`
