from os import listdir, path

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Label, RadioButton, RadioSet

from core.resources import resource_path
from ui.assets.title import title


class IntroScreen(Screen):
    CSS_PATH = resource_path("ui/assets/intro.tcss")
    directory = "profiles/"

    @property
    def ctx(self):
        return getattr(self.app, "ctx")
    def compose(self) -> ComposeResult:
        yield Label(title)
        yield Label("Choose profile to install:")
        profiles = self.getProfiles(self.directory)
        with RadioSet():
            for p in profiles:
                yield RadioButton(p.removesuffix(".yaml").capitalize())
            yield RadioButton("Custom")

    async def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        self.ctx.selected_profile = event.pressed.label.plain
        await self.app.switch_screen("main_screen")

    def getProfiles(self, directory):
        dir_path = resource_path(directory)
        profiles = [f for f in listdir(dir_path) if path.isfile(path.join(dir_path, f))]
        return profiles
