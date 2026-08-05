"""
Deployment Manager

Provides a controlled workflow for deploying generated
network configurations to devices.
"""

from dataclasses import dataclass
from typing import Dict, Optional

from automation.common.logger import get_logger
from automation.common.connection import Connection
from automation.bootstrap.bootstrap import Bootstrap

__all__ = ["Deployment"]
__version__ = "1.0.0"


@dataclass
class DeploymentResult:
    """Result of a deployment operation."""

    hostname: str
    status: str
    commands: int
    error: Optional[str] = None


class Deployment:
    """
    Deployment Manager.

    Responsible for coordinating configuration deployment
    to network devices.

    The initial implementation supports dry-run operation
    so deployment can be tested without modifying devices.
    """

    def __init__(self):
        self.logger = get_logger("deployment")
        self.bootstrap = Bootstrap()

    def generate(self, hostname: str) -> str:
        """
        Generate configuration for a device.
        """
        self.logger.info(
            "Preparing configuration for deployment: %s",
            hostname,
        )
        return self.bootstrap.generate(hostname)

    def deploy(
        self,
        hostname: str,
        dry_run: bool = True,
    ) -> DeploymentResult:
        """
        Deploy configuration to a device.
        """
        self.logger.info(
            "Starting deployment: %s",
            hostname,
        )

        config = self.generate(hostname)

        commands = [
            line.strip()
            for line in config.splitlines()
            if line.strip()
        ]

        if dry_run:
            self.logger.info(
                "Dry run enabled. Configuration not deployed: %s",
                hostname,
            )
            return DeploymentResult(
                hostname=hostname,
                status="DRY_RUN",
                commands=len(commands),
            )

        connection = Connection.from_inventory(
            self.bootstrap.inventory,
            hostname,
        )

        try:
            connection.connect()
            connection.configure(commands)

            self.logger.info(
                "Configuration deployed successfully: %s",
                hostname,
            )

            return DeploymentResult(
                hostname=hostname,
                status="SUCCESS",
                commands=len(commands),
            )

        except Exception as exc:
            self.logger.error(
                "Configuration deployment failed: %s - %s",
                hostname,
                exc,
            )

            return DeploymentResult(
                hostname=hostname,
                status="FAILED",
                commands=0,
                error=str(exc),
            )

        finally:
            connection.disconnect()

    def deploy_all(
        self,
        dry_run: bool = True,
    ) -> Dict[str, DeploymentResult]:
        """
        Deploy configuration to all inventory devices.
        """
        self.logger.info(
            "Starting deployment for all devices"
        )

        results: Dict[str, DeploymentResult] = {}

        for hostname in self.bootstrap.inventory.hostnames:
            results[hostname] = self.deploy(
                hostname,
                dry_run=dry_run,
            )

        self.logger.info(
            "Deployment preparation completed: %s devices",
            len(results),
        )

        return results
