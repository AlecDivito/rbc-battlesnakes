import logging
import os
from training.train import AtomicCounter, Trainer
from training.snake import Snake
from os import environ

from flask import Flask
from flask import request

import server_logic


app = Flask(__name__)
state = server_logic.State()


@app.get("/")
def handle_info():
    """
    This function is called when you register your Battlesnake on play.battlesnake.com
    See https://docs.battlesnake.com/guides/getting-started#step-4-register-your-battlesnake

    It controls your Battlesnake appearance and author permissions.
    For customization options, see https://docs.battlesnake.com/references/personalization

    TIP: If you open your Battlesnake URL in browser you should see this data.
    """
    print("INFO")
    return {
        "apiversion": "1",
        "author": "alecdivito",
        "color": "#00FF00",  # TODO: Personalize
        "head": "default",  # TODO: Personalize
        "tail": "default",  # TODO: Personalize
    }


@app.post("/start")
def handle_start():
    """
    This function is called everytime your snake is entered into a game.
    request.json contains information about the game that's about to be played.
    """
    data = request.get_json()
    state.newGame(data["game"]["id"])
    return "ok"


@app.post("/move")
def handle_move():
    """
    This function is called on every turn of a game. It's how your snake decides where to move.
    Valid moves are "up", "down", "left", or "right".
    """
    data = request.get_json()
    return {"move": state.move(data["game"]["id"])}


@app.post("/end")
def end():
    """
    This function is called when a game your snake was in ends.
    It's purely for informational purposes, you don't have to make any decisions here.
    """
    data = request.get_json()
    state.endGame(data["game"]["id"])
    return "ok"


if __name__ == "__main__":
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
    print("Starting Battlesnake Server...")
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, debug=True)

    if "BUILD_SNAKE_NETWORK" in os.environ:
        # Start running the training script
        print("Starting training network")
        print("This testing script will fork the battlesnake binary multiple times and test it on your snake")
        state.set_training(True)
        command = "./battlesnake play --url localhost:8080 -g solo -v"
        counter = AtomicCounter()
        trainers = []
        for index in range(6):
            thread = Trainer(command, counter, 100)
            thread.start()
            trainers.append(thread)

        for thread in trainers:
            thread.join()
    else:
        # Load all of the script files
        print("This function is currently not supportted")
        print("TODO:")
        print("Make sure that the neural network is saved after each generation")
        print("Using a folder, open that up and use the best network there")
        print("Will be implemented later")
        state.set_training(False)
