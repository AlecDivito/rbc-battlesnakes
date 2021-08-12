import logging
import os
import threading

from flask.helpers import make_response, send_file
from training.train import AtomicCounter, Trainer
from training.snake import Snake
import os

from flask import Flask
from flask import request

import server_logic


app = Flask(__name__)
state = server_logic.State(os.getenv("DEBUG", False))


@app.after_request
def after_request_func(response):
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    return response


@app.get("/")
def handle_info():
    """
    This function is called when you register your Battlesnake on play.battlesnake.com
    See https://docs.battlesnake.com/guides/getting-started#step-4-register-your-battlesnake

    It controls your Battlesnake appearance and author permissions.
    For customization options, see https://docs.battlesnake.com/references/personalization

    TIP: If you open your Battlesnake URL in browser you should see this data.
    """
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
    number_of_snakes = len(data['board']['snakes'])
    state.newGame(data["game"]["id"], number_of_snakes)
    return "ok"


@app.post("/move")
def handle_move():
    """
    This function is called on every turn of a game. It's how your snake decides where to move.
    Valid moves are "up", "down", "left", or "right".
    """
    data = request.get_json()
    return {"move": state.move(data["game"]["id"], data)}


@app.post("/end")
def end():
    """
    This function is called when a game your snake was in ends.
    It's purely for informational purposes, you don't have to make any decisions here.
    """
    data = request.get_json()
    state.endGame(data["game"]["id"], data)
    return "ok"


@app.get("/download")
def download():
    """
    This function is used to download training data that maybe stuck on a server
    that is training with live data (snakes).    
    """
    data_file_path = state.build_data_zip_file()
    return send_file(data_file_path, as_attachment=True)


if __name__ == "__main__":
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
    print("Starting Battlesnake Server...")
    port = int(os.environ.get("PORT", "8080"))
    print("Is this being deployed to productions? {}".format(
        "PRODUCATION_SNAKE" in os.environ))

    if "MULTI_SNAKE_TRAINING" in os.environ:
        state.set_training(True)
        state.set_initial_network(os.environ['SNAKE_NETWORK'])
        state.set_save_folder(os.environ['SAVE_FOLDER'])
        state.set_training_iterations(int(os.environ['ITERATIONS']))
        app.run(host="0.0.0.0", port=port, debug=False)
    elif bool(os.getenv("PRODUCATION_SNAKE", True)):
        # Load all of the script files
        is_training = bool(os.getenv("TRAIN", True))
        state.set_training(is_training)
        state.enable_download_training_data(is_training)
        print("This snake is Training? {}".format(is_training))
        initial_network = os.getenv(
            "SNAKE_NETWORK", "./best_snake/gen:6-fitness:37008")
        state.set_initial_network(initial_network)
        print("The snake is starting using {}".format(initial_network))
        iterations = int(os.getenv("ITERATIONS", 25))
        state.set_training_iterations(iterations)
        print("Starting training at {} iterations".format(iterations))
        state.set_save_folder(os.getenv('SAVE_FOLDER', './network'))
        app.run(host="0.0.0.0", port=port, debug=False)
    else:
        # Start running the training script
        print("Starting training network")
        print("This testing script will fork the battlesnake binary multiple times and test it on your snake")
        # logging.disabled = True
        # app.logger.disabled = True
        state.set_training(True)
        if "TRAIN_SNAKE_NETWORK" in os.environ:
            state.set_initial_network(os.environ["TRAIN_SNAKE_NETWORK"])
        # app.run(host="0.0.0.0", port=port, debug=False)

        kwargs = {'host': '0.0.0.0', 'port': port,
                  'threaded': True, 'use_reloader': False, 'debug': False}
        flask_thread = threading.Thread(
            target=app.run, daemon=True, kwargs=kwargs)
        flask_thread.start()
        command = "./battlesnake play --url http://localhost:8080 -g solo -v"
        for _ in range(500):
            counter = AtomicCounter()
            trainers = []
            for index in range(1):
                thread = Trainer(index, command, counter, 150, False)
                thread.start()
                trainers.append(thread)

            for thread in trainers:
                thread.join()
            state.evolve()

        print("Training finished")
        flask_thread.join()
