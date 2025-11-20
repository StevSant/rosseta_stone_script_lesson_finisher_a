from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Union

from rosseta_stone_script_a.shared.mixins import LoggingMixin


class UnitCatalogPagePort(ABC, LoggingMixin):
    """
    Port for the unit catalog/listing page.
    Handles browsing and selecting units.
    """

    @abstractmethod
    async def select_unit(self, unit_name_or_pattern: Union[str, object]) -> None:
        """Select a unit from the catalog by name or pattern."""
        ...
