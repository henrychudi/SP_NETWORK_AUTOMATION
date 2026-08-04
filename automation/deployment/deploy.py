"""
Deployment Manager

Provides a controlled workflow for deploying generated
network configurations to devices.
"""

from typing import Dict, Optional

from automation.common.exceptions import InventoryError
from automation.common.logger import get_logger
from automation.common.connection import Connection
from automation.bootstrap.bootstrap import Bootstrap

__all__ = ["Deployment"]
__version__ = "1.0.0"


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

        Args:
            hostname:
                Device hostname.

        Returns:
            Generated configuration.
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
    ) -> str:
        """
        Deploy configuration to a device.

        Args:
            hostname:
                Device hostname.

            dry_run:
                If True, configuration is generated but not
                sent to the device.

        Returns:
            Configuration that was generated or deployed.

        Raises:
            InventoryError:
                If the device does not exist or deployment fails.
        """
        self.logger.info(
            "Starting deployment: %s",
            hostname,
        )

        config = self.generate(hostname)

        if dry_run:
            self.logger.info(
                "Dry run enabled. Configuration not deployed: %s",
                hostname,
            )
            return config

        raise InventoryError(
            "Live deployment is not enabled yet."
        )

    def deploy_all(
        self,
        dry_run: bool = True,
    ) -> Dict[str, str]:
        """
        Deploy configuration to all inventory devices.

        Args:
            dry_run:
                If True, generate configurations without
                modifying devices.

        Returns:
            Dictionary mapping hostname to configuration.
        """
        self.logger.info(
            "Starting deployment for all devices"
        )

        configurations = {}

        for hostname in self.bootstrap.inventory.hostnames:
            configurations[hostname] = self.deploy(
                hostname,
                dry_run=dry_run,
            )

        self.logger.info(
            "Deployment preparation completed: %s devices",
            len(configurations),
        )

        return configurations
