"""

"""

from pydantic import BaseModel, StrictStr, StrictInt


class ChordComponents(BaseModel):
    """

    """
    chord: StrictStr
    quality: StrictStr
    inversion: StrictInt
    plain_roman: StrictStr
    root: StrictStr
    bass: tuple[StrictStr | None, StrictStr]
    degrees: list[tuple[StrictStr | None, StrictStr]]
    missing: list[tuple[StrictStr | None, StrictStr]]


class DecomposedChordModel(BaseModel):
    """

    """
    roman_chord: ChordComponents
