from automation.common.inventory import Inventory


def main():
    inventory = Inventory()

    inventory.load()

    print(inventory)

    print(f"Device count : {inventory.device_count}")

    print()

    print("Devices")
    print("-" * 40)
    print(inventory.devices.keys())

    print()

    print("Variables")
    print("-" * 40)
    print(inventory.variables.keys())

    print()

    print("Credentials")
    print("-" * 40)
    print(inventory.credentials.keys())

    print()

    print("Links")
    print("-" * 40)
    print(inventory.links.keys())


if __name__ == "__main__":
    main()
