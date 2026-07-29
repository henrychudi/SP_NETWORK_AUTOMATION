"""
Custom exceptions for the Service Provider Automation Framework.
"""


class InventoryError(Exception):
    """Raised when the inventory is invalid."""
    pass


class DeviceNotFoundError(InventoryError):
    """Raised when a requested device does not exist."""
    pass


class InventoryValidationError(InventoryError):
    """Raised when inventory validation fails."""
    pass
