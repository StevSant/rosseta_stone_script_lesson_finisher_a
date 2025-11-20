from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Protocol


class SupportsContent(Protocol):  # respuesta mínima usada por la app
    content: Any


class IChatLLM(ABC):
    """Contrato mínimo requerido por los casos de uso.

    Debe soportar:
    - invocación sin streaming (invoke)
    - streaming incremental (stream)
    - binding de herramientas (bind_tools) devolviendo otra instancia compatible
    - acceso al modelo subyacente para composición avanzada (as_langchain)
    """

    @abstractmethod
    def invoke(self, messages: list[Any]) -> SupportsContent:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def bind_tools(
        self, tools: list[Any], tool_choice: str = "auto"
    ) -> "IChatLLM":  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def as_langchain(self) -> Any:  # pragma: no cover
        """Retorna el objeto de modelo original (para componer pipes de LangChain)."""
        raise NotImplementedError

    @property  # type: ignore[override]
    @abstractmethod
    def model_name(self) -> str:  # pragma: no cover
        raise NotImplementedError


class IChatLLMFactory(ABC):
    """Fábrica de modelos Chat LLM.

    Permite crear instancias configuradas (modelo, temperatura) desacoplando
    la creación concreta de las capas superiores.
    """

    @abstractmethod
    def create(
        self, *, model: str, temperature: float | None = None
    ) -> IChatLLM:  # pragma: no cover
        raise NotImplementedError
