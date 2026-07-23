from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Button, Label

from lib.core.context import Context
from lib.core.resources import resource_path
from lib.ui.assets.title import title


class IntroScreen(Screen[None]):
    CSS_PATH = resource_path("ui/assets/intro.tcss")

    @property
    def ctx(self) -> Context:
        return self.app.ctx  # type: ignore

    # Return UI
    def compose(self) -> ComposeResult:
        yield Label(title, id="logo")
        yield Vertical(
            Button("Start installer", id="start_btn"),
            Button("Check installed packages", disabled=True),
            Button("Settings", id="settings_btn"),
            id="button-container",
        )

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "start_btn":
                await self.app.switch_screen("profile_selector_screen")  # type: ignore
            case "settings_btn":
                await self.app.switch_screen("settings_screen")  # type: ignore
            case _:
                pass
