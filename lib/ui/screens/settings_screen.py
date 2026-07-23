from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Button, Footer, Label, Switch, TabPane, TabbedContent
from lib.core.context import Context
from lib.core.logger import Logger
from lib.core.resources import resource_path
from lib.core.settings import Settings


class SettingsScreen(Screen[None]):
    CSS_PATH = resource_path("ui/assets/settings.tcss")

    @property
    def ctx(self) -> Context:
        return self.app.ctx  # type: ignore

    @property
    def settings(self):
        return self.ctx.settings

    @property
    def logger(self) -> Logger:
        return self.app.logger  # type: ignore

    # Return UI
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("General"):
                yield Horizontal(
                    Label("Dry run:", classes="label"),
                    Switch(animate=True, value=self.settings.enable_dry_run, classes="switch", id="enable-dry-run"),
                    classes="setting-row",
                )
                yield Horizontal(
                    Label("Generate logs:", classes="label"),
                    Switch(animate=True, value=self.settings.enable_logging, classes="switch", id="enable-logging"),
                    classes="setting-row",
                )
                yield Horizontal(
                    Label("Generate .system-installer file:", classes="label"),
                    Switch(
                        animate=True,
                        value=self.settings.use_installer_file,
                        classes="switch",
                        id="use-installer-file",
                    ),
                    classes="setting-row",
                )
                yield Horizontal(
                    Label("Use packages form central repo:", classes="label", disabled=True),
                    Switch(
                        animate=True,
                        value=self.settings.use_central_repo,
                        classes="switch",
                        disabled=True,
                        id="use-central-repo",
                    ),
                    classes="setting-row",
                )

            with TabPane("Advanced"):
                yield Horizontal(
                    Label("Delete logs:", classes="label"),
                    Button("Delete", classes="delete-btn", id="delete-logs-btn"),
                    classes="setting-row",
                )
                yield Horizontal(
                    Label(
                        "Delete .system-installer file:",
                        classes="label",
                    ),
                    Button("Delete", classes="delete-btn", id="delete-installer-file-btn"),
                    classes="setting-row",
                )
            with TabPane("Apply"):
                yield Horizontal(
                    Button("Apply", id="apply-btn"), Button("Cancel", id="cancel-btn"), classes="apply-container"
                )
        yield Footer()

    def on_mount(self) -> None:
        self.title = "Settings"

    @on(Switch.Changed)
    def on_switch_changed(self, event: Switch.Changed) -> None:
        if event.switch.id == "enable-dry-run":
            self.settings.enable_dry_run = event.value
        elif event.switch.id == "enable-logging":
            self.settings.enable_logging = event.value
        elif event.switch.id == "use-installer-file":
            self.settings.use_installer_file = event.value
        elif event.switch.id == "use-central-repo":
            self.settings.use_central_repo = event.value

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "delete-logs-btn":
                Logger.clear_logs()
                self.notify("All logs deleted")

            case "delete-installer-file-btn":
                Logger.delete_installed_packages_file()
                self.notify("Deleted .system-installer file")

            case "apply-btn":
                try:
                    Settings.save_settings_to_file(self.ctx, self.logger)
                except:
                    self.notify("Failed to save settings see logs for more details!")
                else:
                    self.notify("Successfully saved the settings!")

            case _:
                pass
