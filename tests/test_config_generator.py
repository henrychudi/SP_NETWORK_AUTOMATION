from automation.common.config_generator import ConfigGenerator
from automation.common.exceptions import InventoryError


def main():
    generator = ConfigGenerator()

    # Template existence
    print("\nTemplate Exists")
    print("----------------------------------------")
    print(
        "bootstrap.j2:",
        generator.template_exists("bootstrap.j2"),
    )

    # Render bootstrap configuration
    print("\nRender Bootstrap Configuration")
    print("----------------------------------------")

    config = generator.render(
        "bootstrap.j2",
        hostname="RR1",
        username="admin123",
        password="admin123",
        mgmt_ip="10.10.20.1",
        mgmt_mask="255.255.255.0",
        loopback="10.255.255.1",
        access_interfaces="GigabitEthernet1-10",
    )

    print(config)

    # Missing template
    print("\nMissing Template")
    print("----------------------------------------")

    try:
        generator.render("missing.j2")
    except InventoryError as exc:
        print(exc)


if __name__ == "__main__":
    main()