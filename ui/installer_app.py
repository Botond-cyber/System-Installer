from textual.app import App, ComposeResult
from textual.widgets import Welcome


class InstallerApp(App):
    def compose(self) -> ComposeResult:
        yield Welcome()
