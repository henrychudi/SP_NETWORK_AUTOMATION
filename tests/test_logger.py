from automation.common.logger import get_logger


def main():
    logger = get_logger("test")

    logger.debug("Debug message")
    logger.info("Inventory loaded")
    logger.warning("Configuration not saved")
    logger.error("Authentication failed")
    logger.critical("Router unreachable")


if __name__ == "__main__":
    main()