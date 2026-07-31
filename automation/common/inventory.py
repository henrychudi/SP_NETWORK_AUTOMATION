"""
Inventory Manager

Loads and validates the automation inventory.
"""

from pathlib import Path
from typing import Any, Dict, Optional, List

import yaml

from automation.common.exceptions import InventoryError

__all__ = ["Inventory"]
__version__ = "1.1.0"


class Inventory:
    """
    Inventory Manager.

    Responsible for loading and validating
    the automation inventory.

    Example:
        inventory = Inventory().load()
        for host in inventory.hostnames:
            print(host)
    """

    def __init__(self, inventory_dir: str = "inventory"):
        self.inventory_dir = Path(inventory_dir)

        self.devices: Dict[str, Any] = {}
        self.variables: Dict[str, Any] = {}
        self.credentials: Dict[str, Any] = {}
        self.links: Dict[str, Any] = {}

    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        """Load a YAML file from the inventory directory."""
        filepath = self.inventory_dir / filename

        if not filepath.exists():
            raise InventoryError(f"Missing inventory file: {filepath}")

        with filepath.open("r", encoding="utf-8") as file:
            try:
                data = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                raise InventoryError(
                    f"Invalid YAML syntax in {filepath}"
                ) from exc

        return data or {}

    def load_devices(self) -> None:
        """Load devices from devices.yaml."""
        self.devices = self._load_yaml("devices.yaml")

    def load_variables(self) -> None:
        """Load variables from variables.yaml."""
        self.variables = self._load_yaml("variables.yaml")

    def load_credentials(self) -> None:
        """Load credentials from credentials.yaml."""
        self.credentials = self._load_yaml("credentials.yaml")

    def load_links(self) -> None:
        """Load links from links.yaml."""
        self.links = self._load_yaml("links.yaml")

    def load(self) -> "Inventory":
        """
        Load all inventory YAML files into memory.

        Returns:
            Inventory: the inventory object itself (for chaining).
        """
        self.load_devices()
        self.load_variables()
        self.load_credentials()
        self.load_links()
        return self

    def get_device(self, hostname: str) -> Dict[str, Any]:
        """Return a device by hostname."""
        try:
            return self.devices[hostname]
        except KeyError as exc:
            raise InventoryError(
                f"Device '{hostname}' not found."
            ) from exc

    def device_exists(self, hostname: str) -> bool:
        """Check whether a device exists."""
        return hostname in self.devices

    def link_exists(self, hostname: str) -> bool:
        """Check whether link information exists."""
        return hostname in self.links

    def get_devices(self) -> Dict[str, Any]:
        """Return all devices in the inventory."""
        return self.devices

    def get_devices_by_role(self, role: str) -> Dict[str, Any]:
        """Return all devices matching the given role."""
        return {
            hostname: device
            for hostname, device in self.devices.items()
            if device.get("role") == role
        }

    def get_neighbors(self, hostname: str) -> Dict[str, Any]:
        """Return all neighbors for a given device."""
        try:
            return self.links[hostname]
        except KeyError as exc:
            raise InventoryError(
                f"No link information found for '{hostname}'."
            ) from exc

    def get_credentials(self) -> Dict[str, Any]:
        """Return default credentials."""
        return self.credentials

    def get_variables(self) -> Dict[str, Any]:
        """Return global variables."""
        return self.variables

    def get_platform(self, hostname: str) -> str:
        """
        Return the platform for a given device.

        Note:
            Currently sourced from variables.yaml,
            since devices.yaml does not contain platform.
        """
        return self.variables.get("platform", "")

    def get_loopback(self, hostname: str) -> str:
        """Return the loopback address for a given device."""
        return self.get_device(hostname).get("loopback", "")

    def get_role(self, hostname: str) -> str:
        """Return the role for a given device."""
        return self.get_device(hostname).get("role", "")

    def get_node_id(self, hostname: str) -> Optional[int]:
        """Return the node ID for a given device."""
        return self.get_device(hostname).get("node_id")

    def get_management_ip(self, hostname: str) -> str:
        """Return the management IP for a given device."""
        return self.get_device(hostname).get("mgmt_ip", "")

    @property
    def hostnames(self) -> List[str]:
        """Return all hostnames."""
        return list(self.devices.keys())

    @property
    def device_count(self) -> int:
        """Return the number of devices in the inventory."""
        return len(self.devices)

    def __repr__(self) -> str:
        return (
            f"Inventory("
            f"devices={len(self.devices)}, "
            f"variables={len(self.variables)}, "
            f"credentials={len(self.credentials)}, "
            f"links={len(self.links)})"
        )
