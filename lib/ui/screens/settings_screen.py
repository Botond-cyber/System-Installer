from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Label

from lib.core.context import Context
from lib.core.resources import resource_path


class SettingsScreen(Screen[None]):
    CSS_PATH = resource_path("ui/assets/settings.tcss")

    @property
    def ctx(self) -> Context:
        return self.app.ctx  # type: ignore

    # Return UI
    def compose(self) -> ComposeResult:
        yield Label("settings", id="logo")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case _:
                pass
