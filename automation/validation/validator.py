"""
Device Validation Manager

Provides pre-deployment validation for network devices.
"""

from dataclasses import dataclass
from typing import Optional

from automation.common.connection import Connection
from automation.common.inventory import Inventory
from automation.common.logger import get_logger

__all__ = ["ValidationResult", "Validator"]
__version__ = "1.0.0"


@dataclass
class ValidationResult:
    """Result of a device validation operation."""

    hostname: str
    status: str
    reachable: bool
    hostname_verified: bool
    error: Optional[str] = None


class Validator:
    """
    Device Validation Manager.

    Performs pre-deployment checks before configuration
    is sent to a network device.
    """

    def __init__(self):
        self.logger = get_logger("validation")
        self.inventory = Inventory().load()

    def validate(self, hostname: str) -> ValidationResult:
        """
        Validate a network device.

        Checks:
            1. Device exists in inventory.
            2. Device is reachable.
            3. Actual device hostname matches inventory.
        """
        self.logger.info(
            "Starting validation: %s",
            hostname,
        )

        connection = None

        try:
            device = self.inventory.get_device(hostname)

            expected_hostname = device.get("hostname", "")

            if not expected_hostname:
                return ValidationResult(
                    hostname=hostname,
                    status="FAILED",
                    reachable=False,
                    hostname_verified=False,
                    error=(
                        "Expected hostname is not defined "
                        f"in inventory for '{hostname}'."
                    ),
                )

            connection = Connection.from_inventory(
                self.inventory,
                hostname,
            )

            connection.connect()

            output = connection.execute(
                "show running-config | include ^hostname"
            )

            actual_hostname = None

            for line in output.splitlines():
                line = line.strip()

                if line.startswith("hostname "):
                    actual_hostname = line.split(
                        None,
                        1,
                    )[1].strip()
                    break

            if actual_hostname is None:
                return ValidationResult(
                    hostname=hostname,
                    status="FAILED",
                    reachable=True,
                    hostname_verified=False,
                    error=(
                        "Unable to determine device hostname "
                        f"for '{hostname}'."
                    ),
                )

            hostname_verified = (
                actual_hostname == expected_hostname
            )

            if not hostname_verified:
                self.logger.error(
                    "Hostname mismatch: expected=%s actual=%s",
                    expected_hostname,
                    actual_hostname,
                )

                return ValidationResult(
                    hostname=hostname,
                    status="FAILED",
                    reachable=True,
                    hostname_verified=False,
                    error=(
                        "Hostname mismatch: "
                        f"expected '{expected_hostname}', "
                        f"got '{actual_hostname}'."
                    ),
                )

            self.logger.info(
                "Validation successful: %s",
                hostname,
            )

            return ValidationResult(
                hostname=hostname,
                status="VALID",
                reachable=True,
                hostname_verified=True,
            )

        except Exception as exc:
            self.logger.error(
                "Validation failed: %s - %s",
                hostname,
                exc,
            )

            return ValidationResult(
                hostname=hostname,
                status="FAILED",
                reachable=False,
                hostname_verified=False,
                error=str(exc),
            )

        finally:
            if connection is not None:
                connection.disconnect()
