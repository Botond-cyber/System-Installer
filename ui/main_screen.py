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

from core.loader import get_modules_or_scripts, get_modules_or_scrips_from_profile


class MainScreen(Screen):
    CSS_PATH = "assets/main.tcss"
    modules_directory = "modules/"
    scripts_directory = "scripts/"

    def __init__(
        self, name: str | None = None, id: str | None = None, classes: str | None = None
    ) -> None:
        self.modules = ()
        self.scripts = ()
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
        self.modules = get_modules_or_scripts(self.modules_directory)
        self.scripts = get_modules_or_scripts(self.scripts_directory)
        self.pre_selected_modules = get_modules_or_scrips_from_profile(
            self.ctx.selected_profile, "modules/"
        )
        self.pre_selected_scripts = get_modules_or_scrips_from_profile(
            self.ctx.selected_profile, "scripts"
        )
        with TabbedContent():
            with TabPane(title="Modules"):
                with Static(id="grid-container"):
                    with Static(classes="modules-pane"):
                        modules = self.construct_widgets("modules")
                        yield SelectionList[int](*modules, id="modulesSelect")

                    with Vertical(id="actions-pane"):
                        yield Button("Select all")
                        yield Button("Deselect all")
                        yield Button("Reset")
                        yield Button("Next->", id="nexBtnModules")

            with TabPane(title="Scripts", id="scripts"):
                with Static(id="grid-container"):
                    with Static(classes="modules-pane"):
                        modules = self.construct_widgets("scripts")
                        yield SelectionList[int](*modules,id="scriptsSelect")

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
        self.query_one("#scriptsSelect").border_title = "Choose scripts to install:"
        self.query_one(Pretty).border_title = "Selected modules and scripts:"

    @on(Mount)
    @on(SelectionList.SelectedChanged)
    def update_selected_view(self) -> None:
        self.query_one(Pretty).update(self.query_one(SelectionList).selected)
        self.query_one(Pretty).update([self.modules, self.scripts])

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

    def construct_widgets(self, widget_type):
        widgets = []
        for m in self.modules if widget_type == "modules" else self.scripts:
            widgets.append(
                (
                    m["content"]["name"].capitalize(),
                    m["filename"],
                    (
                        True
                        if m["filename"].removesuffix(".yaml")
                        in (
                            self.pre_selected_modules
                            if widget_type == "modules"
                            else self.pre_selected_scripts
                        )
                        else False
                    ),
                )
            )
        return tuple(widgets)
