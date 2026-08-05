from unittest.mock import MagicMock, patch

from automation.bootstrap.bootstrap import Bootstrap
from automation.common.exceptions import InventoryError


def main():
    bootstrap = Bootstrap()

    # Bootstrap object
    print("\nBootstrap Object")
    print("----------------------------------------")
    print(bootstrap)

    # Generate configuration
    print("\nGenerate RR1 Bootstrap Configuration")
    print("----------------------------------------")

    config = bootstrap.generate("RR1")

    print("Configuration generated successfully.")
    print("Configuration lines:", len(config.splitlines()))

    # Dry-run
    print("\nBootstrap Dry Run")
    print("----------------------------------------")

    dry_run_config = bootstrap.run(
        "RR1",
        dry_run=True,
    )

    print("Dry run completed successfully.")
    print("Configuration lines:", len(dry_run_config.splitlines()))

    # Generate all configurations
    print("\nGenerate All Bootstrap Configurations")
    print("----------------------------------------")

    configurations = bootstrap.generate_all()

    print("Configuration Count:", len(configurations))
    print("Devices:", configurations.keys())

    print("\nBootstrap Live Deployment - Mocked")
    print("----------------------------------------")

    mock_connection = MagicMock()

    with patch(
        "automation.bootstrap.bootstrap.Connection.from_inventory",
        return_value=mock_connection,
    ) as mock_factory:

        live_config = bootstrap.run(
            "RR1",
            dry_run=False,
        )

    mock_factory.assert_called_once_with(
        bootstrap.inventory,
        "RR1",
    )

    mock_connection.connect.assert_called_once()

    expected_commands = [
        line.strip()
        for line in live_config.splitlines()
        if line.strip()
    ]

    mock_connection.configure.assert_called_once_with(
        expected_commands,
    )

    mock_connection.disconnect.assert_called_once()

    print("Mocked live deployment completed successfully.")
    print("Connection factory called:", mock_factory.call_count)
    print("Connect called:", mock_connection.connect.call_count)
    print("Configure called:", mock_connection.configure.call_count)
    print("Disconnect called:", mock_connection.disconnect.call_count)

    # Missing device
    print("\nMissing Device")
    print("----------------------------------------")

    try:
        bootstrap.generate("RR100")
    except InventoryError as exc:
        print(exc)


if __name__ == "__main__":
    main()
