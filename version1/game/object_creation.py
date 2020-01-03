import pyglet
from . import resources, load, physicalobject, player

def create_objects():
    player_ship = player.Player(x=0, y=50, batch=main_batch)
    game_window.push_handlers(player_ship)
    game_window.push_handlers(player_ship.key_handler)

    game_objects = [player_ship]

    return player_ship, game_objects
