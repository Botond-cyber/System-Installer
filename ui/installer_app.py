from textual.app import App, ComposeResult
from textual.widgets import Welcome

from ui.main_screen import MainScreen


class InstallerApp(App):
    SCREENS ={"main_screen": MainScreen}