"""Text cleaner for CvLAC data."""

import html
import re


class Cleaner:
    """Limpia el texto crudo de las hojas de vida antes de su indexación."""

    def clean(self, text: str) -> str:
        """Elimina caracteres de control, entidades HTML y normaliza espacios.

        Args:
            text: Texto crudo a limpiar.

        Returns:
            Texto limpio en una sola línea.
        """
        text = html.unescape(text or "")
        text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
        text = text.replace('"', "")
        text = re.sub(r"\s+", " ", text).strip()
        return text
