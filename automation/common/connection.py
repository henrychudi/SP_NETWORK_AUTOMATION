"""
Device Connection Manager

Provides a common interface for connecting to network devices
and executing operational and configuration commands.
"""

from typing import List, Optional

from netmiko import ConnectHandler
from netmiko.ssh_exception import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

from automation.common.exceptions import InventoryError
from automation.common.logger import get_logger

__all__ = ["Connection"]
__version__ = "1.0.0"


class Connection:
    """
    Device Connection Manager.

    Responsible for establishing a Netmiko connection,
    executing commands, sending configuration, and
    closing the connection.

    Example:
        connection = Connection(
            hostname="RR1",
            device_type="cisco_ios",
            host="10.10.20.1",
            username="admin",
            password="password",
        )

        connection.connect()

        output = connection.execute("show version")

        connection.disconnect()
    """

    def __init__(
        self,
        hostname: str,
        device_type: str,
        host: str,
        username: str,
        password: str,
        port: int = 22,
        timeout: int = 30,
    ):
        self.hostname = hostname
        self.device_type = device_type
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.timeout = timeout

        self.logger = get_logger("connection")

        self._connection = None

    @property
    def connected(self) -> bool:
        """
        Return whether the device is currently connected.
        """
        return self._connection is not None

    def connect(self) -> None:
        """
        Establish a connection to the network device.

        Raises:
            InventoryError:
                If authentication or connection fails.
        """
        self.logger.info(
            "Connecting to device: %s (%s)",
            self.hostname,
            self.host,
        )

        try:
            self._connection = ConnectHandler(
                device_type=self.device_type,
                host=self.host,
                username=self.username,
                password=self.password,
                port=self.port,
                timeout=self.timeout,
            )

        except NetmikoAuthenticationException as exc:
            self.logger.error(
                "Authentication failed: %s",
                self.hostname,
            )

            raise InventoryError(
                f"Authentication failed for '{self.hostname}'."
            ) from exc

        except NetmikoTimeoutException as exc:
            self.logger.error(
                "Connection timeout: %s",
                self.hostname,
            )

            raise InventoryError(
                f"Connection timeout for '{self.hostname}'."
            ) from exc

        except Exception as exc:
            self.logger.error(
                "Connection failed: %s - %s",
                self.hostname,
                exc,
            )

            raise InventoryError(
                f"Unable to connect to '{self.hostname}'."
            ) from exc

        self.logger.info(
            "Connected successfully: %s",
            self.hostname,
        )

    def execute(self, command: str) -> str:
        """
        Execute an operational command.

        Args:
            command:
                CLI command to execute.

        Returns:
            Command output.

        Raises:
            InventoryError:
                If no connection exists.
        """
        if not self.connected:
            raise InventoryError(
                f"Device '{self.hostname}' is not connected."
            )

        self.logger.debug(
            "Executing command on %s: %s",
            self.hostname,
            command,
        )

        try:
            output = self._connection.send_command(command)

        except Exception as exc:
            self.logger.error(
                "Command failed on %s: %s",
                self.hostname,
                exc,
            )

            raise InventoryError(
                f"Command execution failed on '{self.hostname}'."
            ) from exc

        return output

    def configure(self, commands: List[str]) -> str:
        """
        Send configuration commands.

        Args:
            commands:
                List of configuration commands.

        Returns:
            Device configuration output.

        Raises:
            InventoryError:
                If no connection exists.
        """
        if not self.connected:
            raise InventoryError(
                f"Device '{self.hostname}' is not connected."
            )

        self.logger.info(
            "Sending configuration to: %s",
            self.hostname,
        )

        try:
            output = self._connection.send_config_set(commands)

        except Exception as exc:
            self.logger.error(
                "Configuration failed on %s: %s",
                self.hostname,
                exc,
            )

            raise InventoryError(
                f"Configuration failed on '{self.hostname}'."
            ) from exc

        return output

    def disconnect(self) -> None:
        """
        Close the device connection.
        """
        if self._connection is None:
            return

        self.logger.info(
            "Disconnecting from: %s",
            self.hostname,
        )

        try:
            self._connection.disconnect()
        finally:
            self._connection = None
