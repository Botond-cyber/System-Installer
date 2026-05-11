from textual.app import App

from ui.intro_page import IntroScreen
from ui.main_screen import MainScreen


class InstallerApp(App):
    SCREENS = {"intro_screen": IntroScreen, "main_screen": MainScreen}

    async def on_mount(self) -> None:
        await self.push_screen("intro_screen")
        self.theme = "tokyo-night"
