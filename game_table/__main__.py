# imports
from flask import Flask

from game_table.game.game import initialize_game
from game_table.rest.api import index, other, test, test2


app = Flask(__name__)

app.add_url_rule('/', view_func=index)
app.add_url_rule('/other', view_func=other)
app.add_url_rule('/test', view_func=test)
app.add_url_rule('/test2', view_func=test2)


if __name__ == '__main__':

    initialize_game()
    app.run(host='0.0.0.0', port= 8090, use_reloader=True)

