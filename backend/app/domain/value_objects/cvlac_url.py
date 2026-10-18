"""CvLAC URL value object with validation (HU-03)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CvLACUrl:
    """Enlace directo a la hoja de vida de un investigador en CvLAC.

    Attributes:
        value: URL completa con protocolo https.
    """

    value: str

    def __post_init__(self) -> None:
        if not self.value.startswith("https://"):
            raise ValueError(f"URL must use HTTPS: {self.value!r}")
