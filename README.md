# RBC Battle Snake

Hi, this is the repo for RBC's summer snake challenge. In this challenge we gotta
build a Battle snake, oooOOOooo, so much fun.

## Plan

No plan really, but I just finished my AI class at school and i'm thinking it'd
be cool to create a generic algorithm that will be able to compete against other
snakes. SO I'm going to do that. No planning, just plain trust AI that it will
win me the competition.

## TODO

| Done? | Description                                                                                                              |
| :---: | ------------------------------------------------------------------------------------------------------------------------ |
|  [x]  | Working neural network code                                                                                              |
|  [x]  | Training logic needed to train the snake                                                                                 |
|  [ ]  | Modify network to take categorical data instead of decimals                                                              |
|  [ ]  | Modify training to work with multiple snakes (should be already done)                                                    |
|  [ ]  | Get multi-threaded training working correctly                                                                            |
|  [ ]  | Add ability to run snake using saved network                                                                             |
|  [ ]  | Add ability to start training from an existing network                                                                   |
|  [ ]  | Remove all __"magic"__ numbers, convert them all to environment variables                                                |
|  [ ]  | Deployment strategy (training while live, playing games, cloud platform)                                                 |
|  [ ]  | Deployed                                                                                                                 |
|  [ ]  | Add your name somewhere on the project ;)                                                                                |
|  [ ]  | Allow a snake to __choose__ the network it is using depending on some settings (eg. Number of snakes, length of himself) |

## Development

I could re-code their server locally and stuff like that but that stuff takes
time and sadly I don't have a lot of that :( No worries though, they already
have a lot of stuff on their side to help you start off fast so lets go though
what we can do locally so we can move fast and break stuff.

### Local Development

Pre-requirements:

1. Go Programming Language
2. Python 3.x
3. Access to web browser

To get the project running locally:

1. Go to the [battlesnake cli repo](https://github.com/BattlesnakeOfficial/rules/blob/main/cli/README.md)
2. Update the code with the example below. We need this for our training
3. Follow the instructions in the project `README.md` and build the repo
4. Move the `battlesnake` executable to the root of this project directory
5. Download this repo
6. `python3 -m venv env`
7. `source ./env/bin/activate`
8. `python3 -m pip install -r requirements.txt`

Update the following code:

```go
// ... upper half of cli/commands/play.go in `run()` method
if GameType == "solo" { 
    log.Printf("[DONE]: Game completed after %v turns.", Turn) 
} else { 
// ... lower half of cli/commands/play.go
```

To match the following:

```go
// ... upper half of cli/commands/play.go in `run()` method
if GameType == "solo" { 
        log.Printf("[DONE]: Game completed after %v turns.", Turn) 
        for _, snake := range state.Snakes { 
                sendEndRequest(ruleset, state, Battlesnakes[snake.ID]) 
        } 
} else { 
// ... lower half of cli/commands/play.go
```

Once the project has successfully been installed, we can run it:

1. Start the server: `python3 server.py`

We need to be able to switch between testing and running the server. Look at the
`TODO` section to get a better understanding of what is required to make this
puppy __purrrr__.

### Production Development

TODO...

By someone else

## Deployment

TODO...

But I'm thinking just setup some server in AWS somewhere and push the code using
Github Hooks. I think someone else is going to need to do this.
