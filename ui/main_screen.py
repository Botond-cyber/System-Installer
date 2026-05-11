from os import listdir, path

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Label, SelectionList, Header, Footer, Markdown, Button, Static


class MainScreen(Screen):
    CSS_PATH = "assets/main.tcss"
    directory = "modules/"

    @property
    def ctx(self):
        return getattr(self.app, "ctx")

    def compose(self) -> ComposeResult:
        yield Header()
        modules = self.getModules(self.directory)
        yield SelectionList[int](*modules)
        yield Markdown()
        with Static():
            yield Button("Select all")
            yield Button("Reset")
            yield Button("Install", id="install")
        yield Footer()

    def on_mount(self) -> None:
        self.title = f"{self.ctx.selected_profile} installer"

    def getModules(self, directory):
        modules = []
        for idx, f in enumerate(listdir(directory)):
            if path.isfile(path.join(directory, f)):
                modules.append((f.removesuffix(".yaml").capitalize(), idx))
        return tuple(modules)
