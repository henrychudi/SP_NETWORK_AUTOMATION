from automation.common.inventory import Inventory
from automation.common.exceptions import InventoryError


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

    # Positive test: existing device
    print("\nRR1")
    print("----------------------------------------")
    print(inventory.get_device("RR1"))

    # New test: all devices
    print("\nAll Devices")
    print("----------------------------------------")
    print(inventory.get_devices().keys())
    
    print("\nRR Devices")
    print("----------------------------------------")
    print(inventory.get_devices_by_role("RR").keys())

    print("\nP Devices")
    print("----------------------------------------")
    print(inventory.get_devices_by_role("P").keys())

    print("\nPE Devices")
    print("----------------------------------------")
    print(inventory.get_devices_by_role("PE").keys())
    
    print("\nRR1 Neighbors")
    print("----------------------------------------")
    print(inventory.get_neighbors("RR1"))
    
    print("\nCredentials")
    print("----------------------------------------")
    print(inventory.get_credentials())

    print("\nVariables")
    print("----------------------------------------")
    print(inventory.get_variables())

    print("\nPlatform for RR1")
    print("----------------------------------------")
    print(inventory.get_platform("RR1"))

    print("\nLoopback for RR1")
    print("----------------------------------------")
    print(inventory.get_loopback("RR1"))

    print("\nRole for RR1")
    print("----------------------------------------")
    print(inventory.get_role("RR1"))

    print("\nNode ID for RR1")
    print("----------------------------------------")
    print(inventory.get_node_id("RR1"))

    print("\nManagement IP for RR1")
    print("----------------------------------------")
    print(inventory.get_management_ip("RR1"))


    print("\nMissing Neighbor Information")
    print("----------------------------------------")

    try:
        inventory.get_neighbors("RR100")
    except InventoryError as exc:
        print(exc)

    # Negative test: missing device
    print("\nMissing Device")
    print("----------------------------------------")
    try:
        inventory.get_device("RR100")
    except Exception as exc:
        print(exc)


if __name__ == "__main__":
    main()

