from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Label, RadioButton, RadioSet

from lib.core.context import Context
from lib.core.resources import resource_path
from lib.ui.assets.title import title


class IntroScreen(Screen[None]):
    CSS_PATH = resource_path("ui/assets/intro.tcss")

    @property
    def ctx(self) -> Context:
        return self.app.ctx  # type: ignore

    async def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        self.ctx.selected_profile = next(
            (
                profile
                for profile in self.ctx.available_profiles
                if profile.name == event.pressed.label.plain
            ),
            None,
        )
        await self.app.switch_screen("main_screen")  # type: ignore

    # Return UI
    def compose(self) -> ComposeResult:
        yield Label(title)
        yield Label("Choose profile to install:")
        with RadioSet():
            for p in self.ctx.available_profiles:
                yield RadioButton(p.name)
            yield RadioButton("Custom")
