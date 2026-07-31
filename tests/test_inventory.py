from automation.common.inventory import Inventory
from automation.common.exceptions import InventoryError


def main():
    inventory = Inventory().load()

    # Inventory Summary
    print("\nInventory Summary")
    print("----------------------------------------")
    print(inventory)
    print(f"Device Count : {inventory.device_count}")

    # General Inventory
    print("\nGeneral Inventory")
    print("----------------------------------------")
    print("Devices:", inventory.get_devices().keys())
    print("Variables:", inventory.get_variables().keys())
    print("Credentials:", inventory.get_credentials().keys())
    print("Links:", inventory.get_links().keys())

    # Device Queries
    print("\nDevice Queries")
    print("----------------------------------------")
    print("RR1:", inventory.get_device("RR1"))
    print("All Devices:", inventory.get_devices().keys())
    print("RR Devices:", inventory.get_devices_by_role("RR").keys())
    print("P Devices:", inventory.get_devices_by_role("P").keys())
    print("PE Devices:", inventory.get_devices_by_role("PE").keys())

    # Device Information
    print("\nDevice Information")
    print("----------------------------------------")
    print("Platform:", inventory.get_platform("RR1"))
    print("Role:", inventory.get_role("RR1"))
    print("Loopback:", inventory.get_loopback("RR1"))
    print("Management IP:", inventory.get_management_ip("RR1"))
    print("Node ID:", inventory.get_node_id("RR1"))

    # Topology
    print("\nTopology")
    print("----------------------------------------")
    print("RR1 Neighbors:", inventory.get_neighbors("RR1"))

    # Existence Checks
    print("\nExistence Checks")
    print("----------------------------------------")
    print("Hostnames:", inventory.hostnames)
    print("Device Exists RR1:", inventory.device_exists("RR1"))
    print("Device Exists RR100:", inventory.device_exists("RR100"))
    print("Link Exists RR1:", inventory.link_exists("RR1"))
    print("Link Exists RR100:", inventory.link_exists("RR100"))

    # Negative Tests
    print("\nNegative Tests")
    print("----------------------------------------")
    try:
        inventory.get_neighbors("RR100")
    except InventoryError as exc:
        print("Missing Neighbor:", exc)

    try:
        inventory.get_device("RR100")
    except InventoryError as exc:
        print("Missing Device:", exc)


if __name__ == "__main__":
    main()
