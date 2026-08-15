import platform
import sys

from .snapshot import EnvironmentInfo, ReconSnapshot


class ReconEngine:
    def inspect(self) -> ReconSnapshot:
        environment = EnvironmentInfo(
            operating_system=platform.system(),
            architecture=platform.machine(),
            python_version=sys.version.split()[0],
        )

        return ReconSnapshot(
            environment=environment,
        )