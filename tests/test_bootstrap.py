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

    # Missing device
    print("\nMissing Device")
    print("----------------------------------------")

    try:
        bootstrap.generate("RR100")
    except InventoryError as exc:
        print(exc)


if __name__ == "__main__":
    main()