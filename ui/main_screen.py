from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import (
    Label,
    SelectionList,
    Footer,
    Button,
    Static,
    TabbedContent,
    TabPane,
)
from textual.containers import Vertical

from core.loader import getModules



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
        with TabbedContent():
            with TabPane(title="Modules"):
                with Static(id="grid-container"):
                    with Static(classes="modules-pane"):
                        yield Label(" Choose modules to install:", classes="title")
                        modules = getModules(self.directory, self.ctx.selected_profile)
                        yield SelectionList[int](*modules)

                    with Vertical(id="actions-pane"):
                        yield Button("Select all")
                        yield Button("Deselect all")
                        yield Button("Reset")
                        yield Button("Next->", id="nexBtnModules")

            with TabPane(title="Scripts", id="scripts"):
                with Static(id="grid-container"):
                    with Static(classes="modules-pane"):
                        yield Label(" Choose modules to install:", classes="title")
                        modules = getModules(self.directory, self.ctx.selected_profile)
                        yield SelectionList[int](*modules)

                    with Vertical(id="actions-pane"):
                        yield Button("Select all")
                        yield Button("Deselect all")
                        yield Button("Reset")
                        yield Button("Next->", id="nextBtnScripts")
                        yield Button("<-Back", id="backBtnScripts")

            with TabPane(title="Overview", id="install"):
                with Static(id="grid-container"):
                    with Static(classes="modules-pane"):
                        yield Label(" Choose modules to install:", classes="title")
                        modules = getModules(self.directory, self.ctx.selected_profile)
                        yield SelectionList[int](*modules)

                    with Vertical(id="actions-pane"):
                        yield Button("Install", id="installBtn")
                        yield Button("<-Back", id="backBtnInstall")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "nexBtnModules":
                self.query_one("#nextBtnScripts").focus()
            case "nextBtnScripts":
                self.query_one("#installBtn").focus()
            case "backBtnScripts":
                self.query_one("#nexBtnModules").focus()
            case "backBtnInstall":
                self.query_one("#nextBtnScripts").focus()

        # if event.button.id == "install":
        #     self.app.exit(str(event.button))
        #     subprocess.run("cls" if name == "nt" else "clear", shell=True)
        #     self.engine.install("powertoys")