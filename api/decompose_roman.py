"""
Preprocessing utility functions that are the core backend of the APIs.
"""
import music21
from music21 import pitch, note, chord, roman


def analyse_roman(roman_chord: str) -> dict:
    """
    Utility function that analyses a roman chord by extracting
    its features, using the library music21
    :param roman_chord: a roman chord formatted as a string
    :return: a dictionary containing the chord features.
    """
    try:
        chord_object = roman.RomanNumeral(roman_chord)
    except music21.Music21Exception:
        raise ValueError('The chord given is not a valid Roman Chord.')
    else:
        root = str(chord_object.root())
        bass = str(chord_object.bass())
        quality = chord_object.quality
        inversion = chord_object.inversion()
        degree = chord_object.scaleDegree
        return {'chord': roman_chord,
                'quality': quality,
                'inversion': inversion,
                'degree': degree,
                'root': root,
                'bass': bass}


if __name__ == '__main__':
    abc = analyse_roman('VII64/ii')
    print(abc)
