"""
Pydantic validator for validating the input/output of
the FastAPIs scripts
"""

from pydantic import BaseModel, StrictStr, StrictInt


class ChordComponents(BaseModel):
    """
    Validator of the inner elements of the decomposed
    Roman Chord, i.e. the internal elements returned
    from the dictionary that is the output of
    decompose_roman.analyse_roman
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
    Validator of the general container of the decomposed
    Roman Chord, i.e. the external element returned
    from the dictionary that is the output of
    decompose_roman.analyse_roman
    """
    roman_chord: ChordComponents
