from pathlib import PurePath
from typing import List

from textual.app import App
from textual.driver import Driver

from lib.core.context import Context
from lib.core.engine import Engine
from lib.ui.intro_page import IntroScreen
from lib.ui.main_screen import MainScreen


class InstallerApp(App[None]):
    def __init__(
        self,
        ctx: Context,
        engine: Engine,
        driver_class: type[Driver] | None = None,
        css_path: str | PurePath | List[str | PurePath] | None = None,
        watch_css: bool = False,
        ansi_color: bool = False,
    ):
        super().__init__(driver_class, css_path, watch_css, ansi_color)
        self.ctx = ctx
        self.engine = engine

    SCREENS = {"intro_screen": IntroScreen, "main_screen": MainScreen}

    async def on_mount(self) -> None:
        await self.push_screen("intro_screen")
        self.theme = "tokyo-night"
