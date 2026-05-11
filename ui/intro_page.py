from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Label, Button, RadioButton, RadioSet

from ui.assets.title import title
from os import listdir, path


class IntroScreen(Screen):
    CSS_PATH = "assets/intro.tcss"
    directory = "profiles/"

    def compose(self) -> ComposeResult:
        yield Label(title)
        yield Label("Choose profile to install:")
        profiles = self.getProfiles(self.directory)
        with RadioSet():
            for p in profiles:
                yield RadioButton(p.removesuffix(".yaml").capitalize())
            yield RadioButton("Custom")

    def getProfiles(self, directory):
        profiles = [
            f for f in listdir(directory) if path.isfile(path.join(directory, f))
        ]
        return profiles
