"""
Bootstrap Workflow

Builds and optionally deploys the initial device bootstrap configuration.
"""

from typing import Dict, Any

from automation.common.config_generator import ConfigGenerator
from automation.common.connection import Connection
from automation.common.exceptions import InventoryError
from automation.common.inventory import Inventory
from automation.common.logger import get_logger

__all__ = ["Bootstrap"]
__version__ = "1.0.0"


class Bootstrap:
    """
    Bootstrap Workflow.

    Coordinates inventory loading, configuration generation,
    device connection, and configuration deployment.

    Example:
        bootstrap = Bootstrap()

        config = bootstrap.generate("RR1")
        print(config)

        bootstrap.run("RR1", dry_run=True)
    """

    def __init__(
        self,
        inventory: Inventory = None,
        generator: ConfigGenerator = None,
    ):
        self.logger = get_logger("bootstrap")

        self.inventory = inventory or Inventory().load()
        self.generator = generator or ConfigGenerator()

    def _get_device_variables(self, hostname: str) -> Dict[str, Any]:
        """
        Build template variables for a device.
        """
        device = self.inventory.get_device(hostname)
        variables = self.inventory.get_variables()
        credentials = self.inventory.get_credentials()

        default_credentials = credentials.get("default", {})

        return {
            "hostname": device.get("hostname", hostname),
            "username": default_credentials.get("username", ""),
            "password": default_credentials.get("password", ""),
            "mgmt_ip": device.get("mgmt_ip", ""),
            "mgmt_mask": variables.get("mgmt_mask", ""),
            "loopback": device.get("loopback", ""),
            "access_interfaces": variables.get(
                "access_interfaces",
                "",
            ),
        }

    def generate(self, hostname: str) -> str:
        """
        Generate bootstrap configuration for a device.

        Args:
            hostname:
                Inventory hostname.

        Returns:
            Rendered bootstrap configuration.
        """
        self.logger.info(
            "Generating bootstrap configuration: %s",
            hostname,
        )

        if not self.inventory.device_exists(hostname):
            raise InventoryError(
                f"Device '{hostname}' not found."
            )

        variables = self._get_device_variables(hostname)

        return self.generator.render(
            "bootstrap.j2",
            **variables,
        )

    def generate_all(self) -> Dict[str, str]:
        """
        Generate bootstrap configurations for all devices.

        Returns:
            Dictionary containing hostname/configuration pairs.
        """
        self.logger.info(
            "Generating bootstrap configurations for all devices"
        )

        configurations = {}

        for hostname in self.inventory.hostnames:
            configurations[hostname] = self.generate(hostname)

        self.logger.info(
            "Generated bootstrap configurations: %d",
            len(configurations),
        )

        return configurations

    def run(
        self,
        hostname: str,
        dry_run: bool = True,
        device_type: str = "cisco_ios",
    ) -> str:
        """
        Generate and optionally deploy bootstrap configuration.

        Args:
            hostname:
                Inventory hostname.

            dry_run:
                If True, configuration is generated but not deployed.

            device_type:
                Netmiko device type.

        Returns:
            Generated configuration.

        Raises:
            InventoryError:
                If inventory or connection operations fail.
        """
        self.logger.info(
            "Starting bootstrap workflow: %s",
            hostname,
        )

        config = self.generate(hostname)

        if dry_run:
            self.logger.info(
                "Dry run enabled. Configuration not deployed: %s",
                hostname,
            )

            return config

        device = self.inventory.get_device(hostname)
        credentials = self.inventory.get_credentials()
        default_credentials = credentials.get("default", {})

        connection = Connection(
            hostname=hostname,
            device_type=device_type,
            host=device.get("mgmt_ip", ""),
            username=default_credentials.get("username", ""),
            password=default_credentials.get("password", ""),
        )

        try:
            connection.connect()

            commands = [
                line.strip()
                for line in config.splitlines()
                if line.strip()
            ]

            connection.configure(commands)

            self.logger.info(
                "Bootstrap configuration deployed: %s",
                hostname,
            )

        finally:
            connection.disconnect()

        return config
