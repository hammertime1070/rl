from __future__ import annotations
# Optional library allows things to be set to None
from typing import Optional, TYPE_CHECKING
import tcod.event
from actions import Action, EscapeAction, BumpAction

if TYPE_CHECKING:
    from engine import Engine

# Subclass of tcods EventDispatch which allows us to send an event to its method based on event type
class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue
            action.perform()

            self.engine.handle_enemy_turns()
            self.engine.update_fov()

    # overrides tcods EventDispatch.ev_quit to gracefully close the game when you X out
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit

    # receives key press events and returns an Action subclass of None if no valid key was pressed
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        # action variable will hold whatever subclass of Action we assign it to, if no input it will store None
        action: Optional[Action] = None

        key = event.sym

        player = self.engine.player

        if key == tcod.event.K_UP:
            action = BumpAction(player, dx=0, dy=-1)
        if key == tcod.event.K_DOWN:
            action = BumpAction(player, dx=0, dy=1)
        if key == tcod.event.K_LEFT:
            action = BumpAction(player, dx=-1, dy=0)
        if key == tcod.event.K_RIGHT:
            action = BumpAction(player, dx=1, dy=0)

        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction(player)

        return action