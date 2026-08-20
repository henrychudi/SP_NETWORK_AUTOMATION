"""
Validation Manager Tests
"""

from unittest.mock import MagicMock, patch

from automation.validation.validator import Validator


def main():
    print("\nValidation Object")
    print("----------------------------------------")

    validator = Validator()

    print(validator)

    print("\nMocked Validation Test")
    print("----------------------------------------")

    mock_connection = MagicMock()

    mock_connection.execute.return_value = (
        "hostname RR1\n"
    )

    with patch(
        "automation.validation.validator.Connection.from_inventory",
        return_value=mock_connection,
    ):
        result = validator.validate("RR1")

    print("Hostname:", result.hostname)
    print("Status:", result.status)
    print("Reachable:", result.reachable)
    print("Hostname Verified:", result.hostname_verified)
    print("Error:", result.error)

    assert result.hostname == "RR1"
    assert result.status == "VALID"
    assert result.reachable is True
    assert result.hostname_verified is True
    assert result.error is None

    assert mock_connection.connect.called
    assert mock_connection.execute.called
    assert mock_connection.disconnect.called

    print("\nHostname Mismatch Test")
    print("----------------------------------------")

    mock_connection = MagicMock()

    mock_connection.execute.return_value = (
        "hostname WRONG-RR1\n"
    )

    with patch(
        "automation.validation.validator.Connection.from_inventory",
        return_value=mock_connection,
    ):
        result = validator.validate("RR1")

    print("Hostname:", result.hostname)
    print("Status:", result.status)
    print("Reachable:", result.reachable)
    print("Hostname Verified:", result.hostname_verified)
    print("Error:", result.error)

    assert result.hostname == "RR1"
    assert result.status == "FAILED"
    assert result.reachable is True
    assert result.hostname_verified is False
    assert result.error is not None

    print("Hostname mismatch test completed successfully.")

    print("\nConnection Failure Test")
    print("----------------------------------------")

    mock_connection = MagicMock()

    mock_connection.connect.side_effect = Exception(
        "Connection refused"
    )

    with patch(
        "automation.validation.validator.Connection.from_inventory",
        return_value=mock_connection,
    ):
        result = validator.validate("RR1")

    print("Hostname:", result.hostname)
    print("Status:", result.status)
    print("Reachable:", result.reachable)
    print("Hostname Verified:", result.hostname_verified)
    print("Error:", result.error)

    assert result.hostname == "RR1"
    assert result.status == "FAILED"
    assert result.reachable is False
    assert result.hostname_verified is False
    assert result.error is not None

    print("Connection failure test completed successfully.")

    print("Validation test completed successfully.")


if __name__ == "__main__":
    main()
