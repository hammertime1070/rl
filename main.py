import tcod
import copy

from engine import Engine
import entity_factories
from input_handlers import EventHandler
from procgen import generate_dungeon


def main() -> None:
    # Defining Variables for Screen Size
    screen_width = 80
    screen_height = 50

    # Defining variables for Map Size
    map_width = 80
    map_height = 45

    # Defining variables for procedural generation
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    # Defining variables for enemies
    max_monsters_per_room = 2

    # Telling TCOD which font to use
    tileset = tcod.tileset.load_tilesheet('tileset.png', 32,8, tcod.tileset.CHARMAP_TCOD)

    # creates an instance of the EventHandler class
    event_handler = EventHandler()

    # initializing a player and npc and creating a set to hold them
    player = copy.deepcopy(entity_factories.player)

    # initialize game map
    game_map = generate_dungeon(max_rooms=max_rooms,
                                room_min_size=room_min_size,
                                room_max_size=room_max_size,
                                map_width=map_width,
                                map_height=map_height,
                                max_monsters_per_room=max_monsters_per_room,
                                player=player)
    # initializing engine
    engine = Engine(event_handler=event_handler, game_map=game_map, player=player)

    # Creating the screen, giving it width and height and other variables
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Practice",
        vsync=True,
    ) as context:
        # Creates our console, which is what we are drawing to
        # The order argument affects the order of our x and y variables
        # setting order to "F" makes coordinates work as (x,y) instead of (y,x)
        root_console = tcod.Console(screen_width, screen_height, order="F")
        # Creates our game loop, This loop wont end until we close the game
        while True:
            # runs engine
            engine.render(console=root_console, context=context)
            events = tcod.event.wait()
            engine.handle_events(events)


if __name__ == "__main__":
    main()