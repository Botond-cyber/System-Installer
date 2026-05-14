from textual import on
from textual.events import Mount
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import (
    SelectionList,
    Footer,
    Button,
    Static,
    TabbedContent,
    TabPane,
    Pretty,
)
from textual.containers import Vertical

from core.loader import getModules, getModulesFromProfile


class MainScreen(Screen):
    CSS_PATH = "assets/main.tcss"
    directory = "modules/"

    def __init__(
        self, name: str | None = None, id: str | None = None, classes: str | None = None
    ) -> None:
        self.modules = ()
        self.preSelectedModules = ()
        self.dependencies = []
        super().__init__(name, id, classes)

    @property
    def ctx(self):
        return getattr(self.app, "ctx")

    @property
    def engine(self):
        return getattr(self.app, "engine")

    def compose(self) -> ComposeResult:
        self.modules = getModules(self.directory)
        self.preSelectedModules = getModulesFromProfile(self.ctx.selected_profile)
        with TabbedContent():
            with TabPane(title="Modules"):
                with Static(id="grid-container"):
                    with Static(classes="modules-pane"):
                        modules = self.constructModuleWidgets()
                        yield SelectionList[int](*modules, id="modulesSelect")

                    with Vertical(id="actions-pane"):
                        yield Button("Select all")
                        yield Button("Deselect all")
                        yield Button("Reset")
                        yield Button("Next->", id="nexBtnModules")

            with TabPane(title="Scripts", id="scripts"):
                with Static(id="grid-container"):
                    # with Static(classes="modules-pane"):
                    #     modules = getModules(self.directory, self.ctx.selected_profile)
                    #     yield SelectionList[int](*modules,id="scriptsSelect")

                    with Vertical(id="actions-pane"):
                        yield Button("Select all")
                        yield Button("Deselect all")
                        yield Button("Reset")
                        yield Button("Next->", id="nextBtnScripts")
                        yield Button("<-Back", id="backBtnScripts")

            with TabPane(title="Overview", id="install"):
                with Static(id="grid-container"):
                    with Static(classes="modules-pane"):
                        yield Pretty([], id="overviewPretty")

                    with Vertical(id="actions-pane"):
                        yield Button("Install", id="installBtn")
                        yield Button("<-Back", id="backBtnInstall")

        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#modulesSelect").border_title = "Choose modules to install:"
        # self.query_one("#scriptsSelect").border_title = "Choose scripts to install:"
        self.query_one(Pretty).border_title = "Selected modules and scripts:"

    @on(Mount)
    @on(SelectionList.SelectedChanged)
    def update_selected_view(self) -> None:
        # self.query_one(Pretty).update(self.query_one(SelectionList).selected)
        self.query_one(Pretty).update(getModules(self.directory))

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

    def constructModuleWidgets(self):
        widgets = []
        for m in self.modules:
            widgets.append(
                (
                    m["content"]["name"].capitalize(),
                    m["filename"],
                    (
                        True
                        if m["filename"].removesuffix(".yaml") in self.preSelectedModules
                        else False
                    ),
                )
            )
        return tuple(widgets)
