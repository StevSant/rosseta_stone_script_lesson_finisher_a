from dataclasses import dataclass

from rosseta_stone_script_a.shared.utils.compile_case_insensitive import (
    compile_case_insensitive,
)

cci = compile_case_insensitive


@dataclass(frozen=True)
class ModalPatterns:
    """
    Modal patterns with anchored regex for robust matching.
    Uses cci() for case-insensitive patterns and anchors to avoid false matches.
    """

    # Anchored patterns to avoid confusing "Sign in" etc.
    ACCEPT = cci(r"^(aceptar|accept|ok(?:ay)?|agree|allow|consent|got it)$")
    DECLINE = cci(r"^(rechazar|reject|decline|no|cancel(?:ar)?|deny|not now)$")
    CONFIRM = cci(r"^(confirmar|confirm|confirmer|continue)$")
