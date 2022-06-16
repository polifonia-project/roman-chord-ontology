"""
Scripts for converting a Roman Numeral chord into RDF-based serialisation
as described in:
        https://github.com/polifonia-project/roman-chord-ontology

"""
from rdflib import Graph, URIRef, Literal, BNode, Namespace, exceptions
from rdflib.namespace import RDF, RDFS, OWL

from api.validation import ChordComponents


def generate_kg(decomposed_roman: ChordComponents):
    """
    Main function for generating a Knowledge Graph starting from a validated
    object (thought Pydantic Validator) which contains all the constituting
    elements of a Roman Numeral Chord.
    :param decomposed_roman : ChordComponent
        The input of this function is the Pydantic validated version of the
        output coming from the decompose_roman.analyse_roman function
        Example:
        {
            'chord': 'VII64[no3]',
            'quality': 'other',
            'inversion': 2,
            'plain_roman': 'VII',
            'root': 'Bb',
            'bass': ('doublesharp', '4'),
            'degrees': [('doublesharp', '4'), ('sharp', '7')],
            'missing': [(None, '3')]
       }
    :return: rdflib.serialize
        A serialized Knowledge Graph containing the constituting elements of
        the chord, modelled according to the roman-chord-ontology.
        More information about the ontological model at:
        https://github.com/polifonia-project/roman-chord-ontology
    """
    try:
        ROMAN = Namespace('http://w3id.org/polifonia/ontology/roman-chord/')
        CHORD = Namespace('http://purl.org/ontology/chord/')
        g = Graph()
        g.bind('roman', ROMAN)
        g.bind('chord', CHORD)

        roman_chord = URIRef(f'http://w3id.org/polifonia/resource/roman-chord/{decomposed_roman.chord}')
        quality = URIRef(f'http://w3id.org/polifonia/resource/roman-chord/{decomposed_roman.quality}')
        inversion = Literal(decomposed_roman.inversion)
        basic_function_name = Literal(decomposed_roman.plain_roman)
        root_note = decomposed_roman.root
        root_note_uri = URIRef(
            f'https://purl.org/ontology/chord/note/{root_note.replace("#", "s")}')
        bass_alteration, bass_degree = decomposed_roman.bass
        bass_degree = Literal(bass_degree)

        # roman chord
        g.add((roman_chord, RDF.type, ROMAN.Chord))
        g.add((roman_chord, ROMAN.hasQuality, quality))
        g.add((roman_chord, ROMAN.inversionType, inversion))
        root_node = BNode()
        g.add((roman_chord, ROMAN.hasRoot, root_node))
        g.add((root_node, RDF.type, ROMAN.Note))
        g.add((root_node, RDFS.label, Literal(root_note)))
        g.add((root_node, OWL.sameAs, root_note_uri))
        # basic function
        basic_node = BNode()
        g.add((roman_chord, ROMAN.hasBasicFunction, basic_node))
        g.add((basic_node, RDFS.label, basic_function_name))
        g.add((basic_node, RDF.type, ROMAN.BasicFunction))
        # bass interval
        bass = BNode()
        g.add((roman_chord, ROMAN.hasBass, bass))
        g.add((bass, RDF.type, ROMAN.Interval))
        g.add((bass, CHORD.degree, bass_degree))
        g.add((bass, OWL.sameAs,
               URIRef(
                   f'https://purl.org/ontology/scale_interval/{"".join([x if x is not None else "" for x in bass])}')))
        if bass_alteration is not None:
            bass_alteration = Literal(bass_alteration)
            g.add((bass, CHORD.modifier, bass_alteration))
        # intervals
        for interval in decomposed_roman.degrees:
            interval_node = BNode()
            interval_alteration, interval_degree = interval
            g.add((roman_chord, ROMAN.containsInterval, interval_node))
            g.add((interval_node, RDF.type, ROMAN.Interval))
            g.add((interval_node, OWL.sameAs, URIRef(
                f'https://purl.org/ontology/scale_interval/{"".join([x if x is not None else "" for x in interval])}')))
            g.add((interval_node, CHORD.degree, Literal(int(interval_degree))))
            if interval_alteration is not None:
                g.add((interval_node, CHORD.modifier, Literal(interval_alteration)))
        # missing intervals
        for missing_interval in decomposed_roman.missing:
            missing_node = BNode()
            missing_interval_alteration, missing_interval_degree = missing_interval
            g.add((roman_chord, ROMAN.missingInterval, missing_node))
            g.add((missing_node, RDF.type, ROMAN.Interval))
            g.add((missing_node, OWL.sameAs, URIRef(
                f'https://purl.org/ontology/scale_interval/{"".join([x if x is not None else "" for x in missing_interval])}')))
            g.add((missing_node, CHORD.degree, Literal(int(missing_interval_degree))))
            if missing_interval_alteration is not None:
                g.add((missing_node, CHORD.modifier, Literal(missing_interval_alteration)))
    except (TypeError, exceptions.TypeCheckError, exceptions.ParserError, exceptions.UniquenessError) as e:
        raise ValueError(f'The input dictionary cannot be converted into RDF. Error: {e}')

    return g.serialize()


if __name__ == '__main__':
    # test the script
    dummy_chord = {'chord': 'VII64[no3]', 'quality': 'other', 'inversion': 2, 'plain_roman': 'VII',
                   'root': 'Bb', 'bass': ('doublesharp', '4'),
                   'degrees': [('doublesharp', '4'), ('sharp', '7')], 'missing': [(None, '3')]}
    test_kg = generate_kg(ChordComponents(dummy_chord))
    print(test_kg)
