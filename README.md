# RBC Battle Snake

Hi, this is the repo for RBC's summer snake challenge. In this challenge we gotta
build a Battle snake, oooOOOooo, so much fun.

## Plan

No plan really, but I just finished my AI class at school and i'm thinking it'd
be cool to create a generic algorithm that will be able to compete against other
snakes. SO I'm going to do that. No planning, just plain trust AI that it will
win me the competition.

## Best Snakes

The currently best trained snakes are the following:

- `best_battle_snake` for snakes that are used to 8 snakes battleing eachother
- `best_snake` for snakes that are just playing solo

Although, both should work :) just fyi if you are trying to run this (aka this is for my team <3)

## TODO

| Done? | Description                                                                                                                              |
| :---: | ---------------------------------------------------------------------------------------------------------------------------------------- |
|  [x]  | Working neural network code                                                                                                              |
|  [x]  | Training logic needed to train the snake                                                                                                 |
|  [x]  | Modify network to take categorical data instead of decimals (didn't do this, rather just gave values between 1 and -1 based on distance) |
|  [x]  | Modify training to work with multiple snakes (should be already done)                                                                    |
|  [ ]  | Get multi-threaded training working correctly                                                                                            |
|  [x]  | Add ability to run snake using saved network                                                                                             |
|  [x]  | Add ability to start training from an existing network                                                                                   |
|  [ ]  | Remove all __"magic"__ numbers, convert them all to environment variables                                                                |
|  [ ]  | Deployment strategy (training while live, playing games, cloud platform)                                                                 |
|  [ ]  | Deployed                                                                                                                                 |
|  [ ]  | Add your name somewhere on the project ;)                                                                                                |
|  [ ]  | Allow a snake to __choose__ the network it is using depending on some settings (eg. Number of snakes, length of himself)                 |

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

### MultiSnake Training

Although I tried to create a script called `train.sh` to train multiple snakes,
I believe it maybe easier to just run multiple snakes at a time and run a for
loop in bash to hit all of the snake servers locally. Although we could probably
have all of the networks share their best network, I dont think I have the time
for that. Anyways, how to train multiple snakes:

1. Set the following environment variables
   1. `MULTI_SNAKE_TRAINING`: can be anything (normally `True`)
   2. `SNAKE_NETWORK`: Start training with an initial snake network. `REQUIRED`
   3. `SAVE_FOLDER`: Save the best network to file. `REQUIRED`
   4. `ITERATIONS`: Number of games to play before evolving. `REQUIRED`
2. After setting those values run the follow code snippet
3. Note the `&` at the end. This tells the terminal to run the script in the background
4. After finishing testing, run `jobs` too see all of the background processes that are currently running
5. us `fg` and `CTRL + C` to cancel the programs

```bash
# Note, run this as one line
SNAKE=1
MULTI_SNAKE_TRAINING=True
SNAKE_NETWORK=./network/snake_1/gen:37-fitness:2065.0
SAVE_FOLDER="./network/snake_$SNAKE"
ITERATIONS=50
PORT="808$SNAKE" python3 ./server.py &
```

After the number of servers are setup that you want to run tests with, run the
following command:

```bash
for v in {1..50}
do
for i in {1..50}
do
        ./battlesnake play -W 11 -H 11 \
            --name snake_1 --url http://localhost:8081 \
            --name snake_2 --url http://localhost:8082 \
            --name snake_3 --url http://localhost:8083 \
            --name snake_4 --url http://localhost:8084 \
            --name snake_5 --url http://localhost:8085 \
            --name snake_6 --url http://localhost:8086 \
            --name snake_7 --url http://localhost:8087 \
            --name snake_8 --url http://localhost:8088 
done
sleep 10
done
```

### Production Development

TODO...

By someone else

## Deployment

TODO...

But I'm thinking just setup some server in AWS somewhere and push the code using
Github Hooks. I think someone else is going to need to do this.

## Appendix

### Make all the snakes quickly

```bash
SNAKE=1 MULTI_SNAKE_TRAINING=True SNAKE_NETWORK=./network/snake_1/gen:37-fitness:2065.0 SAVE_FOLDER="./network/snake_$SNAKE" ITERATIONS=50 PORT="808$SNAKE" python3 ./server.py &
SNAKE=2 MULTI_SNAKE_TRAINING=True SNAKE_NETWORK=./network/snake_1/gen:37-fitness:2065.0 SAVE_FOLDER="./network/snake_$SNAKE" ITERATIONS=50 PORT="808$SNAKE" python3 ./server.py &
SNAKE=3 MULTI_SNAKE_TRAINING=True SNAKE_NETWORK=./network/snake_1/gen:37-fitness:2065.0 SAVE_FOLDER="./network/snake_$SNAKE" ITERATIONS=50 PORT="808$SNAKE" python3 ./server.py &
SNAKE=4 MULTI_SNAKE_TRAINING=True SNAKE_NETWORK=./network/snake_1/gen:37-fitness:2065.0 SAVE_FOLDER="./network/snake_$SNAKE" ITERATIONS=50 PORT="808$SNAKE" python3 ./server.py &
SNAKE=5 MULTI_SNAKE_TRAINING=True SNAKE_NETWORK=./network/snake_1/gen:37-fitness:2065.0 SAVE_FOLDER="./network/snake_$SNAKE" ITERATIONS=50 PORT="808$SNAKE" python3 ./server.py &
SNAKE=6 MULTI_SNAKE_TRAINING=True SNAKE_NETWORK=./network/snake_1/gen:37-fitness:2065.0 SAVE_FOLDER="./network/snake_$SNAKE" ITERATIONS=50 PORT="808$SNAKE" python3 ./server.py &
SNAKE=7 MULTI_SNAKE_TRAINING=True SNAKE_NETWORK=./network/snake_1/gen:37-fitness:2065.0 SAVE_FOLDER="./network/snake_$SNAKE" ITERATIONS=50 PORT="808$SNAKE" python3 ./server.py &
SNAKE=8 MULTI_SNAKE_TRAINING=True SNAKE_NETWORK=./network/snake_1/gen:37-fitness:2065.0 SAVE_FOLDER="./network/snake_$SNAKE" ITERATIONS=50 PORT="808$SNAKE" python3 ./server.py &
```

### Kill all background jobs

[Taken from this stackoverflow answer](https://unix.stackexchange.com/questions/43527/kill-all-background-jobs)

```bash
jobs -p | grep -o -E '\s\d+\s' | xargs kill
```
