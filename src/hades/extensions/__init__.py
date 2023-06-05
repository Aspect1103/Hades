"""Contains all the extensions used by the game to speed up various features."""
from __future__ import annotations


class DummyImport:
    """Allow faking the import of un-compiled or non-functioning C extensions."""

    def __init__(self: DummyImport, target: str) -> None:  # pragma: no cover
        """Initialise the object.

        Args:
            target: The target to fake.
        """
        self.target: str = target

    def __call__(
        self: DummyImport,
        *args: str,
        **kwargs: str,
    ) -> None:  # pragma: no cover
        """Is called whenever the faked import is called/initialised."""
        raise NotImplementedError


# Check to see if the extensions are compiled or not. If so, import them normally,
# however, if they're not, replace the imports with a dummy function to fake the imports
try:
    from hades.extensions.vector_field.vector_field import VectorField
except ImportError:  # pragma: no cover
    VectorField = DummyImport("VectorField")  # type: ignore[assignment,misc]


__all__ = ("VectorField",)