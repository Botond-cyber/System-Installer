import subprocess
from os import name

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Label, SelectionList, Header, Footer, Button, Static
from textual.containers import Vertical

from core.loader import getModules, getModulesFromProfile


class MainScreen(Screen):
    CSS_PATH = "assets/main.tcss"
    directory = "modules/"

    @property
    def ctx(self):
        return getattr(self.app, "ctx")
    @property
    def engine(self):
        return getattr(self.app, "engine")

    def compose(self) -> ComposeResult:
        yield Header()
        
        with Static(id="grid-container"):
            with Static(id="modules-pane"):
                yield Label(" Choose modules to install:", id="title")
                modules = getModules(self.directory, self.ctx.selected_profile)
                yield SelectionList[int](*modules)

            with Vertical(id="actions-pane"):
                yield Button("Select all")
                yield Button("Reset")
                yield Button("Install", id="install")

        yield Footer()

    def on_mount(self) -> None:
        print(self.ctx.selected_profile)
        self.title = f"{self.ctx.selected_profile} installer"
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "install":
            self.app.exit(str(event.button))
            subprocess.run('cls' if name == 'nt' else 'clear', shell=True)
            self.engine.install("vscode")

    
