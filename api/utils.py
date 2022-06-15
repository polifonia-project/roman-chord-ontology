"""

"""

from music21 import note, interval

ALTERATION_MAP = {
    'b#': None,
    '#b': None,
    '': None,
    '#': 'sharp',
    '##': 'doublesharp',
    'b': 'flat',
    'bb': 'doubleflat',
}


def calculate_interval(note_1: str, note_2: str, simple: bool = True) -> str:
    """
    Utility function that given two music21 notes returns the interval calculated
    between the two.
    Parameters
    ----------
    note_1 : music21.note.Note
        The start note from which the interval has to be calculated.
    note_2 : music21.note.Note
        The end note to which the interval has to be calculated.
    simple : bool
        To mode in which to return the function. If true the interval is printed
        in the music21 "simpleName" mode, in the "name" mode if False.
    Returns
    -------
    interval : str
        An interval as convention in the Harte notation (i.e. b for flat and #
        for sharp).
    """
    note_1 = note.Note(note_1)
    note_2 = note.Note(note_2)

    mode = 'simpleName' if simple is True else 'name'
    computed_interval = getattr(interval.Interval(note_1, note_2), mode)
    return convert_intervals(computed_interval).replace('2', '9')


def convert_intervals(m21_interval: str) -> str:
    """
    Utility function that converts intervals from the music21 format to the Harte one.
    Parameters
    ----------
    m21_interval : str
        A string containing an interval as expressed by the music21 notation (e.g. 'P4').
    Returns
    -------
    harte:interval : str
        A string containing an interval as expressed by the Harte notation (e.g. 'b2').
    """
    substitutions = {
        'M': '',
        'm': 'b',
        'P': '',
        'd': 'b',
        'A': '#',
    }
    return m21_interval.translate(m21_interval.maketrans(substitutions))


def separate_alterations(note: str) -> tuple:
    """

    :param note:
    :return:
    """

    cleaned_note = ''
    alterations = ''
    for character in note:
        if character in ['b', '#']:
            alterations += character
        else:
            cleaned_note += character
    if alterations == 'b#' or alterations == '#b':
        alterations = ''
    return ALTERATION_MAP[alterations], cleaned_note


if __name__ == '__main__':
    test = separate_alterations('bbB')
    print(test)
