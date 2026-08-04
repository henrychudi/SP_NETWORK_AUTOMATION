"""
Configuration Generator

Loads Jinja2 templates and renders network configurations.
"""

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from automation.common.exceptions import InventoryError
from automation.common.logger import get_logger

__all__ = ["ConfigGenerator"]
__version__ = "1.0.0"


class ConfigGenerator:
    """
    Configuration Generator.

    Responsible for loading Jinja2 templates and rendering
    network configuration from supplied variables.

    Example:
        generator = ConfigGenerator()
        config = generator.render(
            "bootstrap.j2",
            hostname="RR1",
            loopback="10.255.255.1",
        )

        print(config)
    """

    def __init__(self, template_dir: str = "templates"):
        self.template_dir = Path(template_dir)

        self.logger = get_logger("config_generator")

        self.environment = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def template_exists(self, template_name: str) -> bool:
        """
        Check whether a template exists.
        """
        template_path = self.template_dir / template_name
        return template_path.is_file()

    def load_template(self, template_name: str):
        """
        Load a Jinja2 template.

        Raises:
            InventoryError:
                If the template does not exist.
        """
        self.logger.debug(
            "Loading template: %s",
            template_name,
        )

        try:
            return self.environment.get_template(template_name)

        except TemplateNotFound as exc:
            self.logger.error(
                "Template not found: %s",
                template_name,
            )

            raise InventoryError(
                f"Template not found: {self.template_dir / template_name}"
            ) from exc

    def render(
        self,
        template_name: str,
        **variables: Any,
    ) -> str:
        """
        Render a Jinja2 template.

        Args:
            template_name:
                Name of the Jinja2 template.

            **variables:
                Variables passed to the template.

        Returns:
            Rendered configuration as a string.
        """
        self.logger.info(
            "Rendering template: %s",
            template_name,
        )

        template = self.load_template(template_name)

        config = template.render(**variables)

        self.logger.debug(
            "Template rendered successfully: %s",
            template_name,
        )

        return config