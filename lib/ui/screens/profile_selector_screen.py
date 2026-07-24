from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Label, RadioButton, RadioSet

from lib.core.context import Context
from lib.core.logger import Logger
from lib.core.resources import resource_path
from lib.ui.assets.title import title


class ProfileSelectorScreen(Screen[None]):

    def __init__(self, name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        self.refresh_times = 0
        super().__init__(name, id, classes)

    CSS_PATH = resource_path("ui/assets/profile_selector.tcss")
    BINDINGS = [
        ("escape", "switch_screen", "Back to main menu"),
    ]

    @property
    def ctx(self) -> Context:
        return self.app.ctx  # type: ignore

    @property
    def logger(self) -> Logger:
        return self.app.logger  # type: ignore

    # Return UI
    def compose(self) -> ComposeResult:
        yield Label(title)
        yield Label("Choose profile to install:")
        with RadioSet():
            for p in self.ctx.available_profiles:
                yield RadioButton(p.name, id=p.id)
            yield RadioButton("Custom")

    # Event listener for radio buttons
    async def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        self.ctx.selected_profile = next(
            (profile for profile in self.ctx.available_profiles if profile.name == event.pressed.label.plain),
            None,
        )
        await self.app.switch_screen("main_screen")  # type: ignore

    # Ensure UI refresh on reload
    async def on_screen_resume(self) -> None:
        if self.refresh_times > 0:
            await self.recompose()
        self.refresh_times += 1

    # Key bind actions
    def action_switch_screen(self):
        self.app.switch_screen("intro_screen")  # type: ignore
