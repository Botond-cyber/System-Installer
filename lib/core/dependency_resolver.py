from lib.core.context import Context


class DependencyResolver:

    @staticmethod
    def resolve(
        ctx: Context,
        package_id: str,
    ) -> list[str]:
        result: list[str] = []
        visited: set[str] = set()

        def dfs(current_id: str) -> None:
            if current_id in visited:
                return
            visited.add(current_id)
            package = ctx.available_packages.get(current_id)
            if package is None:
                raise ValueError(f"Unknown package: {current_id}")
            for dependency in package.dependencies.get(ctx.os, []):
                dfs(dependency)
            result.append(current_id)

        dfs(package_id)
        return result
