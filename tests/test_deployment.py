from automation.common.exceptions import InventoryError
from automation.deployment.deploy import Deployment


def main():
    deployment = Deployment()

    print("\nDeployment Object")
    print("----------------------------------------")
    print(deployment)

    print("\nGenerate Deployment Configuration")
    print("----------------------------------------")

    config = deployment.generate("RR1")

    print("Configuration generated successfully.")
    print("Configuration lines:", len(config.splitlines()))

    print("\nDeployment Dry Run")
    print("----------------------------------------")

    config = deployment.deploy(
        "RR1",
        dry_run=True,
    )

    print("Dry run completed successfully.")
    print("Configuration lines:", len(config.splitlines()))

    print("\nDeploy All Devices - Dry Run")
    print("----------------------------------------")

    configurations = deployment.deploy_all(
        dry_run=True,
    )

    print("Configuration Count:", len(configurations))
    print("Devices:", configurations.keys())

    print("\nLive Deployment Protection")
    print("----------------------------------------")

    try:
        deployment.deploy(
            "RR1",
            dry_run=False,
        )
    except InventoryError as exc:
        print(exc)


if __name__ == "__main__":
    main()