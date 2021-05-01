from flask import render_template
from flask import jsonify
from flask import Blueprint

from ..game.game import get_game_table


game_table_api = Blueprint('game_table_api', __name__)


@game_table_api.route("/game-table", methods=['GET'])
def game_table():
    # return whole game table object with all information
    return jsonify(get_game_table().get_all())


@game_table_api.route("/game-table/player", methods=['GET'])
def game_table_players():
    # return array of all players
    return jsonify(get_game_table().get_players())


@game_table_api.route("/game-table/active-player", methods=['GET'])
def game_table_active_players():
    # return array of active players
    return jsonify(get_game_table().get_active_players())


@game_table_api.route("/game-table/player/<id>", methods=['GET'])
def game_table_player(id):
    # return one player
    return jsonify(get_game_table().get_player(id))


@game_table_api.route("/game-table/press", methods=['POST'])
def game_table_press():
    # trigger big button press
    get_game_table().big_button_pressed()
    return "", 200


@game_table_api.route("/game-table/player/<id>/press", methods=['POST'])
def game_table_player_press(id):
    # trigger player button press
    get_game_table().player_button_pressed(id)
    return "", 200
