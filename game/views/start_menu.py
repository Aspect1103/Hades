from __future__ import annotations

# Builtin
import logging
from typing import TYPE_CHECKING

# Pip
import arcade
import arcade.gui

# Custom
from constants.general import DEBUG_GAME
from views.game import Game

if TYPE_CHECKING:
    from window import Window

# Get the logger
logger = logging.getLogger(__name__)


class StartButton(arcade.gui.UIFlatButton):
    """A button which when clicked will start the game."""

    def on_click(self, event: arcade.gui.UIOnClickEvent) -> None:
        """Called when the button is clicked."""
        # Get the current window and view
        window: Window = arcade.get_window()
        current_view: StartMenu = window.current_view  # noqa

        # Deactivate the UI manager so the buttons can't be clicked
        current_view.manager.disable()

        # Set up the new game
        new_game = Game(DEBUG_GAME)
        window.views["Game"] = new_game
        new_game.setup(1)

        # Show the new game
        window.show_view(new_game)

    def __repr__(self) -> str:
        return (
            f"<StartButton (Position=({self.center_x}, {self.center_y}))"
            f" (Width={self.width}) (Height={self.height})>"
        )


class QuitButton(arcade.gui.UIFlatButton):
    """A button which when clicked will quit the game."""

    def on_click(self, event: arcade.gui.UIOnClickEvent) -> None:
        """Called when the button is clicked."""
        arcade.exit()

    def __repr__(self) -> str:
        return (
            f"<QuitButton (Position=({self.center_x}, {self.center_y}))"
            f" (Width={self.width}) (Height={self.height})>"
        )


class StartMenu(arcade.View):
    """
    Creates a start menu allowing the player to pick which game mode and options they
    want.

    Attributes
    ----------
    manager: arcade.gui.UIManager
        Manages all the different UI elements.
    """

    def __init__(self) -> None:
        super().__init__()
        self.manager: arcade.gui.UIManager = arcade.gui.UIManager()
        vertical_box: arcade.gui.UIBoxLayout = arcade.gui.UIBoxLayout()

        # Create the start button
        start_button = StartButton(text="Start Game", width=200)
        vertical_box.add(start_button.with_space_around(bottom=20))

        # Create the quit button
        quit_button = QuitButton(text="Quit Game", width=200)
        vertical_box.add(quit_button.with_space_around(bottom=20))

        # Register the UI elements
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=vertical_box
            )
        )

    def __repr__(self) -> str:
        return f"<StartMenu (Current window={self.window})>"

    def on_draw(self) -> None:
        """Render the screen."""
        # Clear the screen
        self.clear()

        # Draw the background colour
        self.window.background_color = arcade.color.OCEAN_BOAT_BLUE

        # Draw the UI elements
        self.manager.draw()
