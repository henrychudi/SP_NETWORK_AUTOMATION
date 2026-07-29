"""
Inventory Manager

Loads and validates the automation inventory.
"""

from pathlib import Path
from typing import Any, Dict

import yaml

from automation.common.exceptions import InventoryError

__all__ = ["Inventory"]
__version__ = "1.0.0"


class Inventory:
    """
    Inventory Manager.

    Responsible for loading and validating
    the automation inventory.

    Example:
        inventory = Inventory()
        inventory.load()

        print(inventory.devices)
    """

    def __init__(self, inventory_dir: str = "inventory"):
        self.inventory_dir = Path(inventory_dir)

        self.devices: Dict[str, Any] = {}
        self.variables: Dict[str, Any] = {}
        self.credentials: Dict[str, Any] = {}
        self.links: Dict[str, Any] = {}

    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        """
        Load a YAML file from the inventory directory.
        """
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
        """
        Load devices from devices.yaml.
        """
        self.devices = self._load_yaml("devices.yaml")

    def load_variables(self) -> None:
        """
        Load variables from variables.yaml.
        """
        self.variables = self._load_yaml("variables.yaml")

    def load_credentials(self) -> None:
        """
        Load credentials from credentials.yaml.
        """
        self.credentials = self._load_yaml("credentials.yaml")

    def load_links(self) -> None:
        """
        Load links from links.yaml.
        """
        self.links = self._load_yaml("links.yaml")

    def load(self) -> None:
        """
        Load all inventory YAML files into memory.

        This method loads:

        - devices.yaml
        - variables.yaml
        - credentials.yaml
        - links.yaml
        """
        self.load_devices()
        self.load_variables()
        self.load_credentials()
        self.load_links()

    @property
    def device_count(self) -> int:
        """
        Return the number of devices in the inventory.
        """
        return len(self.devices)

    def __repr__(self) -> str:
        return (
            f"Inventory("
            f"devices={len(self.devices)}, "
            f"variables={len(self.variables)}, "
            f"credentials={len(self.credentials)}, "
            f"links={len(self.links)})"
        )

