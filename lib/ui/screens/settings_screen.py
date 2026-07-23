import copy

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
    BINDINGS = [
        ("escape", "switch_screen", "Back to main menu"),
        ("d", "next", "Next"),
        ("a", "back", "Back"),
        ("c", "cancel", "cancel"),
        ("s", "save", "save"),
    ]

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

    # Set title on mount
    def on_mount(self) -> None:
        self.logger.log_to_file("mount")
        self.title = "Settings"

    # Ensure UI refresh on reload
    def on_screen_resume(self) -> None:
        self.logger.log_to_file("mount")
        self.original_settings = copy.deepcopy(self.ctx.settings)
        self.refresh(recompose=True)

    # Switch event listeners
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

    # Button click handlers
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "delete-logs-btn":
                Logger.clear_logs()
                self.notify("All logs deleted")

            case "delete-installer-file-btn":
                Logger.delete_installed_packages_file()
                self.notify("Deleted .system-installer file")

            case "apply-btn":
                self.save_settings()

            case "cancel-btn":
                self.cancel_changes()

            case _:
                pass

    # Save function
    def save_settings(self):
        try:
            Settings.save_settings_to_file(self.ctx, self.logger)
        except:
            self.notify("Failed to save settings see logs for more details!")
        else:
            self.notify("Successfully saved the settings!")
            self.app.switch_screen("intro_screen")  # type: ignore

    # Discard function
    def cancel_changes(self):
        self.ctx.settings = self.original_settings
        self.app.switch_screen("intro_screen")  # type: ignore

    # Key bind actions
    def action_next(self):
        tabbed_content = self.query_one(TabbedContent)
        match tabbed_content.active[-1]:
            case "1":
                tabbed_content.active = "tab-2"
            case "2":
                tabbed_content.active = "tab-3"
            case "3":
                tabbed_content.active = "tab-1"
            case _:
                pass

    def action_back(self):
        tabbed_content = self.query_one(TabbedContent)
        match tabbed_content.active[-1]:
            case "1":
                tabbed_content.active = "tab-3"
            case "2":
                tabbed_content.active = "tab-1"
            case "3":
                tabbed_content.active = "tab-2"
            case _:
                pass

    def action_cancel(self):
        self.cancel_changes()

    def action_switch_screen(self):
        self.app.switch_screen("intro_screen")  # type: ignore

    def action_save(self):
        self.save_settings()
