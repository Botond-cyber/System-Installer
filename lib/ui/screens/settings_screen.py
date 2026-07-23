from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Button, Footer, Label, Switch, TabPane, TabbedContent
from lib.core.context import Context
from lib.core.resources import resource_path


class SettingsScreen(Screen[None]):
    CSS_PATH = resource_path("ui/assets/settings.tcss")

    def __init__(self, name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        self.dry_run = False
        self.logs = True
        self.installer_file = True
        self.use_central_repo = False
        super().__init__(name, id, classes)

    @property
    def ctx(self) -> Context:
        return self.app.ctx  # type: ignore

    # Return UI
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("General"):
                yield Horizontal(
                    Label("Dry run:", classes="label"),
                    Switch(animate=True, value=self.dry_run, classes="switch"),
                    classes="setting-row",
                )
                yield Horizontal(
                    Label("Generate logs:", classes="label"),
                    Switch(animate=True, value=self.logs, classes="switch"),
                    classes="setting-row",
                )
                yield Horizontal(
                    Label("Generate .system-installer file:", classes="label"),
                    Switch(animate=True, value=self.installer_file, classes="switch"),
                    classes="setting-row",
                )
                yield Horizontal(
                    Label("Use packages form central repo:", classes="label", disabled=True),
                    Switch(animate=True, value=self.use_central_repo, classes="switch", disabled=True),
                    classes="setting-row",
                )

            with TabPane("Advanced"):
                yield Horizontal(
                    Label("Delete logs:", classes="label", disabled=True),
                    Button("Delete", classes="delete-btn"),
                    classes="setting-row",
                )
                yield Horizontal(
                    Label("Delete .system-installer file:", classes="label", disabled=True),
                    Button("Delete", classes="delete-btn"),
                    classes="setting-row",
                )
            with TabPane("Apply"):
                yield Horizontal(
                    Button("Apply", id="apply-btn"), Button("Cancel", id="cancel-btn"), classes="apply-container"
                )
        yield Footer()

    def on_mount(self) -> None:
        self.title = "Settings"

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case _:
                pass
