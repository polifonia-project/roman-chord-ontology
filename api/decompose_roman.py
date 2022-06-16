"""
Preprocessing utility functions that are the core backend of the APIs.
"""
from music21 import note, roman, Music21Exception

from api.utils import calculate_interval, separate_alterations


def analyse_roman(roman_chord: str) -> dict:
    """
    Utility function that analyses a roman chord by extracting
    its features, using the library music21
    :param roman_chord: a roman chord formatted as a string
    :return: a dictionary containing the chord features.
    """
    key = None
    roman_chord = roman_chord.replace(':', '/')
    if '_' in roman_chord:
        roman_chord, key = roman_chord.split('_')
    key = key if key is not None else 'C4'
    try:
        chord_object = roman.RomanNumeral(roman_chord, keyOrScale=key)
    except Music21Exception:
        raise ValueError('The chord given is not a valid Roman Chord.')
    else:
        root = note.Note(chord_object.root()).name
        root = root
        bass = calculate_interval(str(chord_object.bass()), 'C4')
        quality = chord_object.quality
        inversion = chord_object.inversion()
        plain_roman = chord_object.romanNumeralAlone
        degrees = [calculate_interval(str(p), 'C4') for p in chord_object.pitches]
        missing = chord_object.omittedSteps
        return {'chord': roman_chord,
                'quality': quality,
                'inversion': inversion,
                'plain_roman': plain_roman,
                'root': root,
                'bass': separate_alterations(bass),
                'degrees': [separate_alterations(degree) for degree in degrees],
                'missing': [separate_alterations(str(m)) for m in missing]}


if __name__ == '__main__':
    abc = analyse_roman('ciao')
    print(abc)
