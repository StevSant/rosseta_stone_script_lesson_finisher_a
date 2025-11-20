"""
Navigation-related patterns for common UI elements.
Uses anchored regex patterns for robust matching.
"""

from dataclasses import dataclass

from rosseta_stone_script_a.shared.utils.compile_case_insensitive import (
    compile_case_insensitive,
)

cci = compile_case_insensitive


@dataclass(frozen=True)
class NavigationPatterns:
    """Navigation patterns with anchored regex for robust matching."""

    CONTINUE = cci(r"^(continuar|continue|next|siguiente)$")
    BACK = cci(r"^(atr[áa]s|back|anterior|volver)$")
    CANCEL = cci(r"^(cancelar|cancel|annuler)$")
    CLOSE = cci(r"^(cerrar|close|dismiss|x)$")
    SAVE = cci(r"^(guardar|save|enregistrer)$")
    DELETE = cci(r"^(eliminar|delete|borrar|supprimer)$")
