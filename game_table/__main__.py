# imports
from flask import Flask

from game_table.game.game import initialize_game
from game_table.rest.api import game_table_api


app = Flask(__name__)

app.register_blueprint(game_table_api, url_prefix='/api')


if __name__ == '__main__':

    initialize_game()
    app.run(host='0.0.0.0', port= 8090, use_reloader=True)

