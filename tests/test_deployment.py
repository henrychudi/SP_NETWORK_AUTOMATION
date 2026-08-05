#from automation.common.exceptions import InventoryError
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

    result = deployment.deploy(
        "RR1",
        dry_run=True,
    )

    print("Dry run completed successfully.")
    print("Hostname:", result.hostname)
    print("Status:", result.status)
    print("Commands:", result.commands)

    assert result.hostname == "RR1"
    assert result.status == "DRY_RUN"
    assert result.commands == 24
    assert result.error is None

    print("\nDeploy All Devices - Dry Run")
    print("----------------------------------------")

    results = deployment.deploy_all(
        dry_run=True,
    )

    print("Configuration Count:", len(results))
    print("Devices:", results.keys())

    assert len(results) == 13

    for hostname, result in results.items():
        assert result.hostname == hostname
        assert result.status == "DRY_RUN"
        assert result.commands == 24
        assert result.error is None

    print("All dry-run deployment results verified successfully.")

    print("\nLive Deployment Protection")
    print("----------------------------------------")

    print("\nLive Deployment")
    print("----------------------------------------")

    result = deployment.deploy(
        "RR1",
        dry_run=False,
    )

    print("Hostname:", result.hostname)
    print("Status:", result.status)
    print("Commands:", result.commands)
    print("Error:", result.error)

    assert result.hostname == "RR1"
    assert result.status == "SUCCESS"
    assert result.commands == 24
    assert result.error is None

    print("Live deployment result verified successfully.")


if __name__ == "__main__":
    main()
