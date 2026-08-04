from unittest.mock import MagicMock, patch

from automation.common.connection import Connection
from automation.common.exceptions import InventoryError
from automation.common.inventory import Inventory


def main():
    inventory = Inventory().load()

    print("\nInventory Connection Test")
    print("----------------------------------------")

    inventory_connection = Connection.from_inventory(
        inventory,
        "RR1",
    )

    print("Hostname:", inventory_connection.hostname)
    print("Host:", inventory_connection.host)
    print("Device Type:", inventory_connection.device_type)
    print("Username:", inventory_connection.username)
    print("Connected:", inventory_connection.connected)

    connection = Connection(
        hostname="RR1",
        device_type="cisco_ios",
        host="10.10.20.1",
        username="admin123",
        password="admin123",
    )

    print("\nConnection Object")
    print("----------------------------------------")
    print("Hostname:", connection.hostname)
    print("Host:", connection.host)
    print("Connected:", connection.connected)

    print("\nExecute Before Connect")
    print("----------------------------------------")

    try:
        connection.execute("show version")
    except InventoryError as exc:
        print(exc)

    print("\nMock Connection Test")
    print("----------------------------------------")

    mock_device = MagicMock()

    mock_device.send_command.return_value = (
        "Cisco IOS XE Software\n"
        "Hostname: RR1\n"
    )

    mock_device.send_config_set.return_value = (
        "interface Loopback0\n"
        "description TEST\n"
    )

    mock_device.disconnect.return_value = None

    with patch(
        "automation.common.connection.ConnectHandler",
        return_value=mock_device,
    ):
        connection.connect()

        print("Connected:", connection.connected)

        output = connection.execute("show version")

        print("\nCommand Output")
        print("----------------------------------------")
        print(output)

        config_output = connection.configure(
            [
                "interface Loopback0",
                "description TEST",
            ]
        )

        print("\nConfiguration Output")
        print("----------------------------------------")
        print(config_output)

        connection.disconnect()

        print("\nDisconnected")
        print("----------------------------------------")
        print("Connected:", connection.connected)


if __name__ == "__main__":
    main()
