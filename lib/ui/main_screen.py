from typing import Any, cast

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
    Markdown,
)
from textual.containers import Vertical

from lib.core.context import Context
from lib.core.dependency_resolver import DependencyResolver
from lib.core.engine import Engine
from lib.core.resources import resource_path


class MainScreen(Screen[Any]):
    CSS_PATH = resource_path("ui/assets/main.tcss")

    def __init__(self, name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        self.selected_packages: list[str] = []
        self.dependencies: set[str] = set()
        super().__init__(name, id, classes)

    @property
    def app(self) -> Any:
        return super().app  # type: ignore

    @property
    def ctx(self) -> Context:
        return self.app.ctx  # type: ignore[attr-defined]

    @property
    def engine(self) -> Engine:
        return self.app.engine  # type: ignore[attr-defined]

    # Return UI
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane(title="Packages"):
                with Static(id="grid-container"):
                    with Static(classes="package-pane"):
                        packages = self._construct_widgets()
                        yield SelectionList[str](*packages, id="package-select")

                    with Vertical(id="actions-pane"):
                        yield Button("Select all", id="select-all-btn")
                        yield Button("Deselect all", id="deselect-all-btn")
                        yield Button("Reset", id="reset-btn")
                        yield Button("Next->", id="next-btn-packages")

            with TabPane(title="Overview", id="install"):
                with Static(id="grid-container"):
                    with Static(classes="package-pane"):
                        yield Markdown(id="overviewMarkdown")

                    with Vertical(id="actions-pane"):
                        yield Button("Install", id="install-btn")
                        yield Button("<-Back", id="back-btn-install")

        yield Footer()

    # Add border titles
    def on_mount(self) -> None:
        self.query_one("#package-select").border_title = "Choose modules to install:"
        self.query_one(Markdown).border_title = "Selected modules and scripts:"

    # Event listeners
    @on(Mount)
    @on(SelectionList.SelectedChanged)
    def update_selected_view(self, event: Mount | SelectionList.SelectedChanged[Any]) -> None:
        package_select = cast(SelectionList[str], self.query_one("#package-select", SelectionList))

        self.selected_packages = [str(v) for v in (package_select.selected or [])]
        self.get_selected_dependencies()
        self.query_one(Markdown).update(self._construct_markdown())

    # Button event handlers
    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "next-btn-packages":
                self.query_one("#install-btn").focus()
            case "next-btn-scripts":
                self.query_one("#install-btn").focus()
            case "back-btn-install":
                self.query_one("#next-btn-packages").focus()
            case "install-btn":
                self.ctx.packages_to_install = self.selected_packages
                self.app.exit(str(event.button))
            case "select-all-btn":
                self.query_one("#package-select", SelectionList).select_all()  # type: ignore
            case "deselect-all-btn":
                self.query_one("#package-select", SelectionList).deselect_all()  # type: ignore
            case "reset-btn":
                selection_list = self.query_one("#package-select", SelectionList)  # type: ignore
                for package_id in (package_id for _, package_id, _ in self._construct_widgets()):
                    if package_id in self.ctx.packages_from_profile:
                        selection_list.select(package_id)  # type: ignore
                    else:
                        selection_list.deselect(package_id)  # type: ignore
            case _:
                pass

    # Construct widgets for selection list
    def _construct_widgets(
        self,
    ) -> tuple[tuple[str, str, bool], ...]:
        widgets: list[tuple[str, str, bool]] = []
        selected_profile = self.ctx.selected_profile
        selected_packages = set(
            selected_profile.get_packages(self.ctx.os) if selected_profile else [],
        )
        for p in self.ctx.available_packages.values():
            if self.ctx.os not in p.supported_os:
                continue
            else:
                widgets.append((p.name, p.id, p.id in selected_packages))
                if p.id in selected_packages:
                    self.ctx.packages_from_profile.add(p.id)
        return tuple(widgets)

    # Get dependencies to show on second page
    def get_selected_dependencies(self):
        self.dependencies.clear()
        for s in self.selected_packages:
            deps = DependencyResolver.resolve(self.ctx, s)
            for d in deps:
                if d != s:
                    self.dependencies.add(d)

    # Construct markdown for the second page
    def _construct_markdown(self) -> str:
        packages_md = (
            "\n".join(
                f"- {self.ctx.available_packages[p].name}"
                for p in self.selected_packages
                if p in self.ctx.available_packages
            )
            or "None"
        )
        deps_md = (
            "\n".join(
                f"- {self.ctx.available_packages[d].name}"
                for d in self.dependencies
                if d in self.ctx.available_packages
            )
            or "None"
        )

        return "\n".join(
            [
                "## Packages:",
                packages_md,
                "",
                "## Dependencies:",
                deps_md,
            ]
        )
