from flask import render_template
from flask import jsonify

from ..game.game import get_game_table

def index():
    return render_template('index.html')

def other():
    return render_template('other.html')


def test():
    d = {'test': 3}
    return jsonify(d)


def test2():
    d = {'huhu': get_game_table().get_test()}
    return jsonify(d)