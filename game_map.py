from __future__ import annotations

from typing import Iterable, Optional, TYPE_CHECKING

import numpy as np # type: ignore
from tcod.console import Console

import tile_types

if TYPE_CHECKING:
    from entity import Entity


class GameMap:
    # initializer takes width and height and assigns them, as well as entities
    def __init__(self, width: int, height: int, entities: Iterable[Entity]=()):
        self.width, self.height = width, height
        self.entities = set(entities)
        # creates a 2d array and fills it with floor tiles
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

        self.visible = np.full((width, height), fill_value=False, order="F") # Tiles the player can currently see
        self.explored = np.full((width, height), fill_value=False, order="F") # Tiles the player has seen before

    def get_blocking_entity_at_location(self, location_x: int, location_y: int) -> Optional[Entity]:
        for entity in self.entities:
            if entity.blocks_movement and entity.x == location_x and entity.y == location_y:
                return entity
        return None

    def in_bounds(self, x: int, y: int) -> bool:
        """ Return True if x and y are inside of the bounds of this map. """
        return 0 <= x < self.width and 0 <= self.height

    # Uses the Console class method tiles_rgb  to render the map, faster than console.print
    def render(self, console: Console) -> None:
        """
       Renders the Map
       If a tile is in the visible array then draw it with the light colors
       If it isnt but its in the explored array then draw it with the dark colors
       otherwise the default is SHROUD
        """
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default = tile_types.SHROUD
        )

        for entity in self.entities:
            # Only print entities that are in FOV
            if self.visible[entity.x, entity.y]:
                console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)