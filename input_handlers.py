# Optional library allows things to be set to None
from typing import Optional
import tcod.event
from actions import Action, EscapeAction, BumpAction


# Subclass of tcods EventDispatch which allows us to send an event to its method based on event type
class EventHandler(tcod.event.EventDispatch[Action]):
    # overrides tcods EventDispatch.ev_quit to gracefully close the game when you X out
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit

    # receives key press events and returns an Action subclass of None if no valid key was pressed
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        # action variable will hold whatever subclass of Action we assign it to, if no input it will store None
        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.K_UP:
            action = BumpAction(dx=0, dy=-1)
        if key == tcod.event.K_DOWN:
            action = BumpAction(dx=0, dy=1)
        if key == tcod.event.K_LEFT:
            action = BumpAction(dx=-1, dy=0)
        if key == tcod.event.K_RIGHT:
            action = BumpAction(dx=1, dy=0)

        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()

        return action