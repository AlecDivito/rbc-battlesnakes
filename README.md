# RBC Battle Snake

Hi, this is the repo for RBC's summer snake challenge. In this challenge we gotta
build a Battle snake, oooOOOooo, so much fun.

## Plan

No plan really, but I just finished my AI class at school and i'm thinking it'd
be cool to create a generic algorithm that will be able to compete against other
snakes. SO I'm going to do that. No planning, just plain trust AI that it will
win me the competition.

## Development

I could re-code their server and stuff like that but that stuff takes time and
sadly I don't have a lot of that :( No worries though, they already have a lot
of stuff on their side to help you start off fast so lets go though what we can
do locally so we can move fast and break stuff.

### Local Development

Pre-requirements:

1. Go Programming Language
2. Python 3.x
3. Access to web browser

To get the project running locally:

1. Go to the [battlesnake cli repo](https://github.com/BattlesnakeOfficial/rules/blob/main/cli/README.md)
2. Follow the instructions and build the repo
3. Copy the cli somewhere safe on your $PATH and delete the repo
4. Download this repo
5. `python3 -m venv env`
6. `source ./env/bin/activate`
7. `python3 -m pip install -r requirements.txt`

Once the project has successfully been installed, we can run it:

1. Start the server: `python3 server.py`
2. Run a game of battlesnakes: `./battlesnake play --url localhost:8080 -g solo -v`

### Production Development

TODO...

## Deployment

TODO...

But I'm thinking just setup some server in AWS somewhere and push the code using
Github Hooks.