# mech-ai

Program your AI to destroy other bots and take over the world.

This project is split into two separate core parts: **client** and **server**.

The server runs online and handles incoming messages from one or many clients.
The server is the board you play on, the referee, and the score keeper.

The clients manage games, make moves, and contain the AI code that makes
the decisions. The clients are the players.


## Server

### Google App Engine (GAE)

The server is written using Google App Engine. Which means the server is
written in Python 2.7.x!

GAE Documentation: https://cloud.google.com/appengine/docs/python/

#### Development:

1. Install [Google App Engine SDK](https://cloud.google.com/appengine/downloads)
2. Run development server in root folder: `$ dev_appserver.py .`
3. See dev output at [http://localhost:8080/](http://localhost:8080/)
4. You can view the dev GAE dashboard at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

#### Production:

4. To deploy into production: `$ appcfg.py -A mech-ai update app.yaml`
5. See output at [http://mech-ai.appspot.com/](http://mech-ai.appspot.com/)


## Client

The client is also written in Python 2.7.x, but this could change.

### Usage

1. Run the client: `$ python client.py`

#### Authentication:

All messages to the server (except to register a new username) must be accompanied
by authentication headers, so you need to provide your username and access token:

* Use command line args: `$ python client.py -u mitch -t 4hfg83bg`
* Use ENV vars: `$ USER=mitch TOKEN=a6javvi8 python client.py`
* Set `username` and `access_token` variables in `local_config.py`

Precedence: Arguments > local_config.py > Environment variables

After registering a new username you'll be given the option of loading
those settings for the session.

#### Environment

Use an `ENV` environment variable to specify whether you want to connect to
`dev`, i.e. localhost, or `prod` (production) environments. Default is `dev`!

    $ ENV=prod python client.py -u mitch -t 4hfg83bg

