from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Welcome


class IntroScreen(Screen):
     def compose(self) -> ComposeResult:
        yield Welcome()